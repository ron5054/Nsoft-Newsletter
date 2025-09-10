# Newsletter Creation Guide

## Overview
Create a new newsletter with 4 articles and Hebrew content, following the same structure as newsletter-23.

## Automated Process with LinkedIn MCP - Expected Workflow

### Expected User Workflow
When a user requests a new newsletter, Claude Code should perform the following process **automatically**:

1. **Request 4 LinkedIn post URLs** from the user
2. **Check for duplicate URLs** - Read `linkedin_urls_registry.json` and compare user URLs against all previous newsletters
   - If any URL was used before → **STOP** and tell user which newsletter used it
   - If all URLs are unique → Continue with creation
3. **Detect the next newsletter number** (check the highest existing number and increment by 1)
4. **Extract content using MCP** from all 4 links
5. **Summarize each post** into a short Hebrew article (3-4 paragraphs)
6. **Create compelling intro** summarizing newsletter topics
7. **Build complete newsletter structure** with all required files
8. **Update linkedin_urls_registry.json** with the new newsletter URLs
9. **Update index.html** with the new newsletter
10. **Launch npm run dev** for preview

### Using Claude Code with LinkedIn MCP

#### Example Usage
```
User: "Create a new newsletter with these 4 links:
1. https://www.linkedin.com/posts/...
2. https://www.linkedin.com/posts/...
3. https://www.linkedin.com/posts/...
4. https://www.linkedin.com/posts/..."
```

#### MCP Field Mapping to Newsletter Data - **CRITICAL TO READ!**

**⚠️ Common Error: Using the Wrong Link!**

When MCP returns data, use the correct fields:

```json
// MCP Response
{
  "url": "https://www.linkedin.com/posts/...",          // ❌ This is the LinkedIn post link
  "text": "Post content in Hebrew...",
  "link": "https://lnkd.in/shortlink",                  // ✅ This is the link to use!
  "link_img": "https://media.linkedin.com/...",
  "success": true
}
```

**Correct Mapping to Newsletter Data:**
- `MCP.text` → `article content` (after summarization)
- `MCP.link` → `article.url` ✅ **BUT must resolve redirects to final URL!**
- `MCP.link_img` → `article.img` (or default if null/improper)
- **Never** `MCP.url` → `article.url` ❌

**⚠️ CRITICAL: Always Resolve Redirect URLs to Final Destination**
- If `MCP.link` contains `lnkd.in` or other redirect URLs, use WebFetch to get the final destination
- Example: `https://lnkd.in/d_ATe_KB` → `https://x.com/akshay_pachaar/status/1954158220727263311`
- Never use redirect URLs in the newsletter - always use the final destination

**Default Image Handling:**
- If `MCP.link_img` is `null` or contains improper images (LinkedIn profile/background), use rotating default images:
  1. `https://www.21kschool.com/ua/wp-content/uploads/sites/6/2023/11/15-Facts-About-Coding-Every-Kid-Should-Know.png`
  2. `https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg`
  3. `https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png`
  4. `https://blog-cdn.codefinity.com/images/84cf0089-4483-4124-8388-a52baff28a6e_8fcdc9988f47418092f5013c41d6f358.png.png`
- **Important**: Never repeat the same default image within a single newsletter (4 articles max)
- MCP automatically filters out LinkedIn profile and background images
- YouTube thumbnails are always preferred when available

#### Claude Code Should Execute:
- Extract content from all links using LinkedIn MCP
- Create newsletter-XX (XX = next sequential number)
- Write all files (intro.html, article-1.html through article-4.html)
- **Create data.js with extracted data**
- **Use `link` field from MCP, not `url` field** ⚠️
- **CRITICAL: Resolve any redirect URLs (lnkd.in, etc.) to final destination using WebFetch** ⚠️
- **Use rotating default images when MCP returns null/improper image** (never repeat within same newsletter)
- Create compelling intro summarizing newsletter topics
- Update index.html and add new newsletter to `availableNewsletters` list
- Launch `npm run dev` for preview

## Important Troubleshooting Points

### MCP Error - Wrong Link (Most Common Problem!)
- ✅ **Correct**: Use `MCP.link` for `article.url` BUT resolve redirects to final URL
- ❌ **Wrong**: Use `MCP.url` for `article.url` 
- ❌ **Wrong**: Use redirect URLs like `lnkd.in` directly
- **Reason**: `MCP.url` is the LinkedIn post link, `MCP.link` is the actual article link, but must be resolved to final destination

### Redirect Resolution Process
1. Get `MCP.link` from extraction
2. If it contains `lnkd.in`, `bit.ly`, or other redirect domains:
   ```javascript
   // Use WebFetch to resolve redirect
   const finalUrl = await WebFetch(MCP.link, "What is the final destination URL?");
   article.url = finalUrl; // Use the final destination
   ```
3. Examples of correct resolution:
   - `https://lnkd.in/d_ATe_KB` → `https://x.com/akshay_pachaar/status/1954158220727263311`
   - `https://lnkd.in/eTBnzM_h` → `https://tkdodo.eu/blog/deriving-client-state-from-server-state`

### Default Image Implementation
When `MCP.link_img` is `null`, use this rotation logic:

```javascript
const DEFAULT_IMAGES = [
  "https://www.21kschool.com/ua/wp-content/uploads/sites/6/2023/11/15-Facts-About-Coding-Every-Kid-Should-Know.png",
  "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg", 
  "https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png",
  "https://blog-cdn.codefinity.com/images/84cf0089-4483-4124-8388-a52baff28a6e_8fcdc9988f47418092f5013c41d6f358.png.png"
];

// For each article needing default image, use next unused image from array
let usedDefaults = [];
articles.forEach((article, index) => {
  if (!article.img || article.img === null) {
    article.img = DEFAULT_IMAGES[usedDefaults.length];
    usedDefaults.push(usedDefaults.length);
  }
});
```

## Manual Step-by-Step Process

### 1. Create Folder Structure
```bash
mkdir -p packages/html-emails/newsletter/newsletter-XX
```

### 2. Create Content Files
Create these files in the newsletter-XX directory:

#### intro.html
- Write compelling intro title (2-3 words maximum)
- 2-3 paragraphs explaining the newsletter topic
- Keep content concise and engaging

#### article-1.html through article-4.html
- Each article should be 3-4 paragraphs
- Use `<div dir="rtl">` as wrapper
- **IMPORTANT**: Do NOT include `<h3>` titles in article files - titles come from data.js only
- Write in Hebrew with proper RTL format
- Keep content concise but informative
- Start directly with `<p>` tags inside the `<div dir="rtl">` wrapper

### 3. Create data.js
**Important**: Create the `data.js` file before compilation. Use `newsletter-23/data.js` as example:

```javascript
const fs = require("fs");

function buildJson(directoryName) {
  const introContent = fs.readFileSync(`./${directoryName}/intro.html`, "utf8");
  const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, "utf8");
  const article2Content = fs.readFileSync(`./${directoryName}/article-2.html`, "utf8");
  const article3Content = fs.readFileSync(`./${directoryName}/article-3.html`, "utf8");
  const article4Content = fs.readFileSync(`./${directoryName}/article-4.html`, "utf8");

  return {
    intro: {
      title: "Your Intro Title", // Extract from intro.html
      content: introContent,
    },
    articles: [
      {
        title: "Article 1 Title", // Extract from HTML comments or content
        content: article1Content,
        img: "IMAGE_URL_1 || DEFAULT_IMAGE_1", // YouTube > proper LinkedIn image > rotating default
        url: "RESOLVED_LINK_1", // Use MCP.link, not MCP.url!
      },
      {
        title: "Article 2 Title", 
        content: article2Content,
        img: "IMAGE_URL_2",
        url: "LINKEDIN_URL_2",
      },
      {
        title: "Article 3 Title",
        content: article3Content,
        img: "IMAGE_URL_3", 
        url: "LINKEDIN_URL_3",
      },
      {
        title: "Article 4 Title",
        content: article4Content,
        img: "IMAGE_URL_4",
        url: "LINKEDIN_URL_4",
      },
    ],
    unsubscribe_url: "{{unsubscribe_url}}",
    message_content: "{{message_content}}",
    subscriber: { first_name: "{{subscriber.first_name}}" },
  };
}

module.exports = buildJson;
```

**Note**: If the newsletter uses `utils/genericData` (like newsletter-24), use that instead of the code above.

### 4. Update Development Script
Edit `dev-server.js`:
```javascript
const newsletterFolder = "newsletter-XX"; // Change this line
```

### 5. Update index.html
Update `index.html` and add the new newsletter to the `availableNewsletters` list:

**Important**: Read the newsletter content to extract accurate title and description:

1. **Read `intro.html`** - Extract title from `<h2>` and description from paragraphs
2. **Read `article-1.html`** - Check title in HTML comments (if present)
3. **Add to list** with correct data:

```javascript
const availableNewsletters = [
    {
        folder: 'newsletter-23',
        title: 'AI Agents - From Lab to Field',
        description: 'This week we move from theory to practice - how AI Agents become real work tools'
    },
    {
        folder: 'newsletter-XX', // Change to appropriate XX
        title: 'New Newsletter Title', // Extract from intro.html
        description: 'Brief description of new newsletter' // Extract from intro.html
    }
    // Add more newsletters here as they are created
];
```

**Example Data Extraction**:
- **Title**: Extract from `<h2>` in `intro.html`
- **Description**: Extract from first paragraph in `intro.html` or create summary from content

### 6. Launch Development Environment
**Important**: Ensure you created `data.js` before running the script!

```bash
npm run dev
```

The script will:
- Initial compilation of the newsletter
- Watch for file changes (auto-recompile)
- Launch live server at http://localhost:8080/output.html
- Auto-refresh browser when files change

### 7. Manual Compilation (Optional)
If you only need to compile without live server:
```bash
node compileNewsletter.js
```

## Content Guidelines

### Article Structure
- **Title**: 3-7 words, engaging
- **Content**: 3-4 paragraphs, Hebrew RTL
- **Image**: LinkedIn or YouTube image
- **URL**: LinkedIn post address

### Writing Style
- Use Hebrew with proper RTL format
- Keep paragraphs short (2-3 sentences)
- Create engaging and informative content
- Include technical insights when appropriate

### Required Information per Article
1. **Title** (Hebrew)
2. **Content** (Hebrew, 3-4 paragraphs)
3. **Image URL** (LinkedIn or YouTube image)
4. **LinkedIn URL** (full post address)

## File Structure
```
newsletter-XX/
├── intro.html
├── article-1.html
├── article-2.html
├── article-3.html
├── article-4.html
├── data.js
└── output.html (generated automatically)
```

## Important Notes
- Always use `<div dir="rtl">` for Hebrew content
- Ensure all LinkedIn addresses are complete and working
- **Required**: Create `data.js` before compilation
- **Required**: Update `index.html` and add each new newsletter to `availableNewsletters` list
- **Required**: Read newsletter content (intro.html) to extract accurate title and description
- **CRITICAL**: When editing existing newsletter articles with new LinkedIn URLs, always update `linkedin_urls_registry.json` to reflect the changes
- Use `npm run dev` for development with live reload
- Browser opens automatically at http://localhost:8080/output.html
- File changes trigger automatic compilation and refresh
- Keep content concise but valuable
- Maintain consistent format across all articles

## Content Structure Examples
### intro.html
```html
<div dir="rtl">
  <h2>Intro Title</h2>
  <p>
    First paragraph - explanation of newsletter topic
  </p>
  <p>
    Second paragraph - what readers will learn
  </p>
</div>
```

### article-X.html
**IMPORTANT**: Do NOT include `<h3>` headings - titles come from data.js only!

```html
<div dir="rtl">
  <p>
    First paragraph - article introduction (start directly with content)
  </p>
  <p>
    Second paragraph - main content
  </p>
  <p>
    Third paragraph - summary or important point
  </p>
</div>
```