"""
Test script for the LinkedIn MCP server.
"""

import asyncio
import json
import logging
from linkedin_extractor import LinkedInExtractor

# Configure logging for testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_url_validation():
    """Test URL validation functionality."""
    extractor = LinkedInExtractor()
    
    # Valid URLs
    valid_urls = [
        "https://www.linkedin.com/posts/john-doe_activity-1234567890123456789-abcd",
        "https://linkedin.com/posts/jane-smith_something-9876543210987654321-xyz1",
        "https://www.linkedin.com/pulse/some-article-title-author-name"
    ]
    
    # Invalid URLs
    invalid_urls = [
        "https://twitter.com/user/status/123",
        "https://www.linkedin.com/in/someone",
        "https://www.linkedin.com/company/microsoft",
        "not-a-url",
        "https://linkedin.com/feed/"
    ]
    
    print("Testing URL validation...")
    
    for url in valid_urls:
        is_valid = extractor._is_valid_linkedin_url(url)
        print(f"✓ {url}: {'Valid' if is_valid else 'INVALID (ERROR)'}")
        assert is_valid, f"Should be valid: {url}"
    
    for url in invalid_urls:
        is_valid = extractor._is_valid_linkedin_url(url)
        print(f"✗ {url}: {'VALID (ERROR)' if is_valid else 'Invalid'}")
        assert not is_valid, f"Should be invalid: {url}"
    
    print("URL validation tests passed!\n")


async def test_extraction_with_invalid_url():
    """Test extraction with invalid URL."""
    extractor = LinkedInExtractor()
    
    print("Testing extraction with invalid URL...")
    
    result = await extractor.extract_post_text("https://invalid-url.com")
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    assert not result['success']
    assert result['error'] == "Invalid LinkedIn post URL"
    assert result['text'] is None
    
    print("Invalid URL test passed!\n")


async def test_extraction_with_nonexistent_post():
    """Test extraction with a valid LinkedIn URL format but nonexistent post."""
    extractor = LinkedInExtractor()
    
    # This is a valid URL format but likely doesn't exist
    test_url = "https://www.linkedin.com/posts/nonexistentuser_activity-1111111111111111111-aaaa"
    
    print(f"Testing extraction with nonexistent post: {test_url}")
    
    result = await extractor.extract_post_text(test_url)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Should fail gracefully
    assert not result['success']
    assert result['text'] is None
    assert 'error' in result
    
    print("Nonexistent post test passed!\n")


async def test_mcp_server_import():
    """Test that the MCP server can be imported and initialized."""
    try:
        from mcp_server import LinkedInMCPServer
        server = LinkedInMCPServer()
        print("✓ MCP server can be imported and initialized")
        print(f"✓ FastAPI app created: {server.app.title}")
        print("MCP server import test passed!\n")
    except Exception as e:
        print(f"✗ MCP server import failed: {e}")
        raise


async def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("LINKEDIN MCP SERVER TESTS")
    print("=" * 60)
    
    try:
        await test_url_validation()
        await test_extraction_with_invalid_url()
        await test_extraction_with_nonexistent_post()
        await test_mcp_server_import()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✅")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install Playwright: playwright install chromium")
        print("3. Run the server: python mcp_server.py")
        print("4. Test with CLI: python cli.py <linkedin-post-url>")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    asyncio.run(run_all_tests())