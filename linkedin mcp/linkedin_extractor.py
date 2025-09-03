"""
LinkedIn post text extraction module.
Handles both public posts (via requests + BeautifulSoup) and JavaScript-heavy posts (via Playwright).
"""

import re
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs, unquote

import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInExtractor:
    """Extracts text content from LinkedIn posts."""
    
    def __init__(self):
        self.session = requests.Session()
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def _is_valid_linkedin_url(self, url: str) -> bool:
        """Validate if the URL is a valid LinkedIn post URL."""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc in ['linkedin.com', 'www.linkedin.com'] and
                '/posts/' in parsed.path or '/pulse/' in parsed.path
            )
        except Exception:
            return False

    def _extract_text_from_soup(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract post text from BeautifulSoup object."""
        # Common selectors for LinkedIn post content
        selectors = [
            '[data-test-id="main-feed-activity-card"] .feed-shared-text',
            '.feed-shared-text',
            '.feed-shared-update-v2__commentary',
            '.attributed-text-segment-list__content',
            '.break-words span[dir="ltr"]',
            'div[data-test-id="main-feed-activity-card"] div.break-words',
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                # Extract text from all matching elements and join
                text_parts = []
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 10:  # Filter out very short text snippets
                        text_parts.append(text)
                
                if text_parts:
                    full_text = ' '.join(text_parts)
                    # Clean up extra whitespace
                    full_text = re.sub(r'\s+', ' ', full_text).strip()
                    return full_text
        
        return None

    def _resolve_linkedin_redirect(self, url: str) -> str:
        """Resolve LinkedIn redirect URLs to their final destinations, following the complete redirect chain."""
        try:
            current_url = url
            max_redirects = 5  # Prevent infinite redirect loops
            redirects_followed = 0
            
            while redirects_followed < max_redirects:
                original_url = current_url
                
                # Step 1: Handle lnkd.in URLs specially (they serve content directly, not HTTP redirects)
                if 'lnkd.in' in current_url:
                    try:
                        response = self.session.get(current_url, timeout=15)
                        response.raise_for_status()
                        
                        # Parse HTML to find YouTube video ID
                        soup = BeautifulSoup(response.content, 'html.parser')
                        content = str(soup)
                        
                        # Look for YouTube video IDs in the content
                        youtube_patterns = [
                            r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
                            r'https?://youtu\.be/([a-zA-Z0-9_-]{11})',
                            r'["\']v["\']:\s*["\']([a-zA-Z0-9_-]{11})["\']',  # JSON format
                            r'videoId["\']?\s*:\s*["\']([a-zA-Z0-9_-]{11})["\']'  # videoId property
                        ]
                        
                        for pattern in youtube_patterns:
                            matches = re.findall(pattern, content)
                            if matches:
                                video_id = matches[0]  # Take the first match
                                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                                logger.debug(f"Resolved lnkd.in URL: {current_url} -> {youtube_url} (video ID: {video_id})")
                                redirects_followed += 1
                                current_url = youtube_url
                                break
                        
                        # If we found a YouTube URL, break the loop
                        if 'youtube.com' in current_url or 'youtu.be' in current_url:
                            break
                            
                    except Exception as e:
                        logger.debug(f"Failed to resolve lnkd.in URL {current_url}: {e}")
                        # Fall back to returning the original URL
                        break
                
                # Step 2: Check if it's a LinkedIn redirect URL
                elif 'linkedin.com/redir/redirect' in current_url:
                    parsed = urlparse(current_url)
                    query_params = parse_qs(parsed.query)
                    
                    # Extract the actual URL from the 'url' parameter
                    if 'url' in query_params:
                        current_url = unquote(query_params['url'][0])
                        logger.debug(f"Resolved LinkedIn redirect: {original_url} -> {current_url}")
                        redirects_followed += 1
                        continue
                
                # Step 3: For any other URL, follow HTTP redirects
                elif current_url.startswith('http'):
                    try:
                        # Make a HEAD request to follow redirects without downloading content
                        response = self.session.head(current_url, allow_redirects=True, timeout=15)
                        if response.url != current_url and response.url != original_url:
                            logger.debug(f"Followed HTTP redirect: {current_url} -> {response.url}")
                            current_url = response.url
                            redirects_followed += 1
                            continue
                    except Exception as e:
                        logger.debug(f"Could not follow HTTP redirect for {current_url}: {e}")
                        # Try with GET request if HEAD fails (some servers don't support HEAD)
                        try:
                            response = self.session.get(current_url, allow_redirects=True, timeout=15, stream=True)
                            # Close the response immediately to avoid downloading large content
                            response.close()
                            if response.url != current_url and response.url != original_url:
                                logger.debug(f"Followed HTTP redirect via GET: {current_url} -> {response.url}")
                                current_url = response.url
                                redirects_followed += 1
                                continue
                        except Exception as e2:
                            logger.debug(f"Could not follow HTTP redirect via GET for {current_url}: {e2}")
                
                # No more redirects found, break the loop
                break
            
            if redirects_followed > 0:
                logger.info(f"Final URL after {redirects_followed} redirects: {current_url}")
            
            return current_url
            
        except Exception as e:
            logger.error(f"Error resolving redirect chain for {url}: {e}")
            return url

    def _extract_youtube_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from various YouTube URL formats."""
        if not url or 'youtube.com' not in url and 'youtu.be' not in url:
            return None
        
        try:
            # Handle different YouTube URL formats
            patterns = [
                r'(?:youtube\.com/watch\?.*[?&]v=|youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
                r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
                r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
                    
            return None
        except Exception as e:
            logger.debug(f"Error extracting YouTube video ID from {url}: {e}")
            return None

    def _generate_youtube_thumbnail_url(self, video_id: str) -> str:
        """Generate YouTube thumbnail URL from video ID."""
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    def _extract_post_images_from_soup(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the first image from LinkedIn post content."""
        # Look for images in post content areas
        image_selectors = [
            '[data-test-id="main-feed-activity-card"] img[src]',
            '.feed-shared-image img[src]',
            '.feed-shared-update-v2__content img[src]',
            '.attributed-text-segment-list__content img[src]',
            'div.break-words img[src]',
            'img[src*="media-exp"]',  # LinkedIn media images
            'img[src*="licdn.com"]',  # LinkedIn CDN images
        ]
        
        for selector in image_selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('src')
                if src and src.startswith('http'):
                    # Skip profile pictures, icons, and very small images
                    skip_patterns = [
                        'profile-displayphoto',
                        'company-logo',
                        'icon',
                        'avatar',
                        'emoji'
                    ]
                    
                    if not any(pattern in src.lower() for pattern in skip_patterns):
                        # Check if image has reasonable dimensions (avoid tiny icons)
                        width = img.get('width')
                        height = img.get('height')
                        
                        # Skip if we can determine it's too small
                        if width and height:
                            try:
                                if int(width) < 100 or int(height) < 100:
                                    continue
                            except (ValueError, TypeError):
                                pass
                        
                        logger.debug(f"Found post image: {src}")
                        return src
                        
        return None

    def _extract_links_from_soup(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the first external link from BeautifulSoup object."""
        found_links = []
        
        # Look for links in post content areas
        link_selectors = [
            '[data-test-id="main-feed-activity-card"] a[href]',
            '.feed-shared-text a[href]',
            '.feed-shared-update-v2__commentary a[href]',
            '.attributed-text-segment-list__content a[href]',
            'div.break-words a[href]',
            'a[href*="lnkd.in"]',  # LinkedIn shortened links (highest priority)
            'a[href^="http"]',     # External links
        ]
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Clean up the link
                    href = href.strip()
                    
                    # Skip LinkedIn internal links (profiles, companies, etc.)
                    skip_patterns = [
                        '/in/', '/company/', '/school/',
                        '/feed/', '/mynetwork/', '/jobs/',
                        'linkedin.com/posts/', 'linkedin.com/pulse/',
                        'linkedin.com/signup/', 'linkedin.com/login/',
                        'linkedin.com/uas/', 'linkedin.com/reg/',
                        'session_redirect', 'cold-join'
                    ]
                    
                    # Prioritize LinkedIn shortened links (lnkd.in)
                    if 'lnkd.in' in href:
                        resolved_url = self._resolve_linkedin_redirect(href)
                        return resolved_url
                    
                    # Otherwise collect external links
                    if (href.startswith('http') and 
                        not any(pattern in href for pattern in skip_patterns)):
                        found_links.append(href)
        
        # Return first external link if no lnkd.in link found, resolve if it's a LinkedIn redirect
        if found_links:
            first_link = found_links[0]
            return self._resolve_linkedin_redirect(first_link)
        
        return None

    async def _extract_with_playwright(self, url: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract post text, links, and images using Playwright for JavaScript-heavy content."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                page = await context.new_page()
                
                # Navigate to the page
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait for potential content to load
                await page.wait_for_timeout(3000)
                
                text_result = None
                link_result = None
                image_result = None
                
                # Try multiple selectors to find the post content
                text_selectors = [
                    '[data-test-id="main-feed-activity-card"] .feed-shared-text',
                    '.feed-shared-text',
                    '.feed-shared-update-v2__commentary',
                    '.attributed-text-segment-list__content',
                    '.break-words span[dir="ltr"]',
                ]
                
                for selector in text_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            text_parts = []
                            for element in elements:
                                text = await element.inner_text()
                                if text and len(text.strip()) > 10:
                                    text_parts.append(text.strip())
                            
                            if text_parts:
                                full_text = ' '.join(text_parts)
                                text_result = re.sub(r'\s+', ' ', full_text).strip()
                                break
                    except Exception as e:
                        logger.debug(f"Text selector {selector} failed: {e}")
                        continue
                
                # Extract links
                try:
                    found_links = []
                    links = await page.query_selector_all('a[href]')
                    for link in links:
                        href = await link.get_attribute('href')
                        if href:
                            href = href.strip()
                            skip_patterns = [
                                '/in/', '/company/', '/school/',
                                '/feed/', '/mynetwork/', '/jobs/',
                                'linkedin.com/posts/', 'linkedin.com/pulse/',
                                'linkedin.com/signup/', 'linkedin.com/login/',
                                'linkedin.com/uas/', 'linkedin.com/reg/',
                                'session_redirect', 'cold-join'
                            ]
                            
                            # Prioritize LinkedIn shortened links (lnkd.in)
                            if 'lnkd.in' in href:
                                link_result = self._resolve_linkedin_redirect(href)
                                break
                                
                            # Otherwise collect external links
                            if (href.startswith('http') and 
                                not any(pattern in href for pattern in skip_patterns)):
                                found_links.append(href)
                    
                    # Use first external link if no lnkd.in link found, resolve if it's a LinkedIn redirect
                    if not link_result and found_links:
                        link_result = self._resolve_linkedin_redirect(found_links[0])
                        
                except Exception as e:
                    logger.debug(f"Link extraction failed: {e}")

                # Extract images
                try:
                    image_selectors = [
                        '[data-test-id="main-feed-activity-card"] img[src]',
                        '.feed-shared-image img[src]',
                        '.feed-shared-update-v2__content img[src]',
                        'img[src*="media-exp"]',
                        'img[src*="licdn.com"]',
                    ]
                    
                    for selector in image_selectors:
                        images = await page.query_selector_all(selector)
                        for img in images:
                            src = await img.get_attribute('src')
                            if src and src.startswith('http'):
                                skip_patterns = [
                                    'profile-displayphoto', 'company-logo', 'icon', 'avatar', 'emoji'
                                ]
                                if not any(pattern in src.lower() for pattern in skip_patterns):
                                    image_result = src
                                    break
                        if image_result:
                            break
                            
                except Exception as e:
                    logger.debug(f"Image extraction failed: {e}")
                
                await browser.close()
                return text_result, link_result, image_result
                
        except Exception as e:
            logger.error(f"Playwright extraction failed: {e}")
            return None, None, None

    def _extract_with_requests(self, url: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract post text, links, and images using requests and BeautifulSoup."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text = self._extract_text_from_soup(soup)
            link = self._extract_links_from_soup(soup)
            image = self._extract_post_images_from_soup(soup)
            return text, link, image
            
        except Exception as e:
            logger.error(f"Requests extraction failed: {e}")
            return None, None, None

    def _generate_link_img(self, link: Optional[str], post_image: Optional[str]) -> Optional[str]:
        """Generate link_img based on the rules: YouTube thumbnail > proper post image > default images."""
        # Rule 1: If there's a YouTube link, generate thumbnail URL
        if link:
            video_id = self._extract_youtube_video_id(link)
            if video_id:
                return self._generate_youtube_thumbnail_url(video_id)
        
        # Rule 2: If no YouTube link but there's a post image, check if it's proper
        if post_image:
            # Filter out LinkedIn profile/background images that aren't proper article images
            improper_image_patterns = [
                'profile-displaybackgroundimage',  # LinkedIn background images
                'profile-displayphoto',           # LinkedIn profile photos
                '/profile/',                      # General profile images
                'headshot',                       # Profile headshots
            ]
            
            # If it's an improper image type, treat as no image
            if any(pattern in post_image for pattern in improper_image_patterns):
                logger.debug(f"Filtering out improper image: {post_image}")
                return None
            
            return post_image
        
        # Rule 3: If none of the above, return null (newsletter creation will handle default)
        return None

    async def extract_post_text(self, url: str) -> Dict[str, Any]:
        """
        Extract text, links, and images from a LinkedIn post URL.
        
        Args:
            url: LinkedIn post URL
            
        Returns:
            Dictionary with 'url', 'text', 'link', 'link_img', and 'success' keys
        """
        # Validate URL
        if not self._is_valid_linkedin_url(url):
            return {
                "url": url,
                "text": None,
                "link": None,
                "link_img": None,
                "error": "Invalid LinkedIn post URL",
                "success": False
            }
        
        logger.info(f"Extracting text, links, and images from: {url}")
        
        # Try requests first (faster for public posts)
        text, link, post_image = self._extract_with_requests(url)
        
        if text:
            logger.info("Successfully extracted content using requests")
            link_img = self._generate_link_img(link, post_image)
            
            result = {
                "url": url,
                "text": text,
                "success": True
            }
            result["link"] = link
            result["link_img"] = link_img
            return result
        
        # Fall back to Playwright for JavaScript-heavy content
        logger.info("Falling back to Playwright extraction")
        text, link, post_image = await self._extract_with_playwright(url)
        
        if text:
            logger.info("Successfully extracted content using Playwright")
            link_img = self._generate_link_img(link, post_image)
            
            result = {
                "url": url,
                "text": text,
                "success": True
            }
            result["link"] = link
            result["link_img"] = link_img
            return result
        
        # No text found
        return {
            "url": url,
            "text": None,
            "link": None,
            "link_img": None,
            "error": "Could not extract text from post. Post may be private or unavailable.",
            "success": False
        }