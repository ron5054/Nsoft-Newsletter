# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Start development server**: `npm run dev`
  - Launches live server on port 8080 with auto-compilation
  - Watches for changes in .js, .html, and .hbs files
  - Opens http://localhost:8080/index.html
  - Auto-recompiles newsletter on file changes

- **Manual compilation**: `node compileNewsletter.js`
  - Compiles hardcoded newsletter-23 using Handlebars template
  - Watches for changes in article files and recompiles automatically
  - Updates index.html with newsletter entries
  - Note: compileNewsletter.js is hardcoded to newsletter-23, while dev-server.js auto-detects the latest newsletter folder

## Architecture

### Newsletter System
- **Template-based**: Uses Handlebars (template-2.hbs) to generate newsletter HTML
- **Content structure**: Each newsletter has its own folder (e.g., newsletter-23/) containing:
  - `data.js`: Exports function that builds newsletter data from HTML files
  - `intro.html`, `article-1.html` through `article-4.html`: Article content
  - `output.html`: Generated final newsletter
- **Live server**: Built-in development server with file watching and auto-reload

### File Structure
- `dev-server.js`: Development server with live reload and compilation
- `compileNewsletter.js`: Standalone compilation script with file watching
- `template-2.hbs`: Handlebars email template with RTL Hebrew support
- `index.html`: Newsletter management interface for viewing different newsletters
- `images/`: Newsletter assets and graphics
- `newsletter-{number}/`: Individual newsletter folders with content and data files

### Data Flow
1. HTML content files → `data.js` → Handlebars compilation → `output.html`
2. Newsletter data includes intro, 4 articles with titles/content/images/URLs
3. Template supports email-specific formatting with responsive design
4. Index page auto-updates with new newsletters via JavaScript array (compileNewsletter.js only)

### Key Implementation Details
- **Auto-detection**: dev-server.js automatically detects and compiles the latest newsletter folder
- **File watching**: Both scripts watch for changes but with different scopes:
  - compileNewsletter.js: watches specific article files in hardcoded newsletter-23
  - dev-server.js: watches all .js, .html, .hbs files (excluding node_modules and output.html)
- **Cache clearing**: dev-server.js clears require cache for data.js to ensure fresh compilation

### Email Template Features
- RTL Hebrew language support
- Responsive design for mobile/desktop
- Email client compatibility
- Handlebars templating with article iteration
- nSoft branding and styling

## LinkedIn MCP Integration

### MCP Configuration
This project includes a LinkedIn Post Text Extractor MCP (Model Context Protocol) server for extracting content from LinkedIn posts. The MCP config file is available at `claude_mcp_config.json`.

**To use with Claude Code:**
1. Copy the MCP configuration from `claude_mcp_config.json`
2. Add to your Claude Code MCP settings
3. The LinkedIn extractor will be available as a tool

### LinkedIn MCP Features
- **Smart extraction**: Extracts text, links, and images from LinkedIn posts
- **Dual-method approach**: Uses requests+BeautifulSoup (fast) with Playwright fallback (JS-heavy content)
- **Link resolution**: Handles `lnkd.in` shortened URLs and extracts YouTube video IDs
- **Multi-language support**: Works with Hebrew, English, and other languages
- **YouTube integration**: Auto-generates thumbnails for YouTube links

### Supported LinkedIn URLs
- `https://www.linkedin.com/posts/username_activity-*`
- `https://www.linkedin.com/pulse/*`

### MCP Commands
- **Setup**: `pip install -r "linkedin mcp/requirements.txt"`
- **Install browsers**: `playwright install chromium`
- **Test extraction**: `python "linkedin mcp/cli.py" [LinkedIn URL]`
- **Server location**: `linkedin mcp/mcp_stdio_server.py`

## Newsletter Creation Workflow

**IMPORTANT**: Before creating any newsletter, always read the comprehensive guide at `NEWSLETTER_CREATION_GUIDE.md` for detailed instructions and troubleshooting.

### Expected User Workflow
When a user requests a new newsletter, Claude Code should automatically:

1. **Request 4 LinkedIn post URLs** from the user
2. **Auto-detect the next newsletter number** (check highest existing number and increment by 1)
3. **Extract content using LinkedIn MCP** from all 4 links
4. **🚨 CRITICAL: Resolve ALL redirect URLs to final destinations** - Use WebFetch to resolve any `lnkd.in` or redirect URLs
5. **Create newsletter folder** (e.g., newsletter-25)
6. **CRITICAL: Create data.js with correct structure FIRST** - This must match the expected pattern: `function buildJson(directoryName)` that exports this function
7. **Create engaging intro** summarizing newsletter topics (intro.html)
8. **Verify intro compilation** - Check that intro content appears in output.html immediately after creating intro.html
9. **Summarize each post** into Hebrew articles (article-1.html through article-4.html)
10. **✅ VERIFY: Check all article URLs are final destinations (NOT redirect links)**
11. **Update linkedin_urls_registry.json** with new newsletter URLs  
12. **Update index.html** with new newsletter entry
13. **Launch npm run dev** for preview

### Critical MCP Field Mapping
**⚠️ Second Most Common Error: Using Redirect URLs Without Resolution!**

When MCP returns data, use the correct fields AND resolve redirects:
```
MCP Output → Newsletter Data:
- MCP.text → article content (after summarization)
- MCP.link → ⚠️ MUST RESOLVE REDIRECTS → article.url
- MCP.link_img → article.img
- MCP.url = LinkedIn post URL ❌ (Never use for article.url)
```

**🚨 CRITICAL URL Resolution Process:**
```javascript
// Example: MCP returns lnkd.in redirect URL
const mcpLink = "https://lnkd.in/dYMXUjwW";

// WRONG: Using redirect URL directly
article.url = mcpLink; // ❌ DON'T DO THIS!

// CORRECT: Resolve redirect to final destination
const finalUrl = await WebFetch(mcpLink, "What is the final destination URL?");
article.url = finalUrl; // ✅ Use final destination
// Result: "https://tkdodo.eu/blog/react-query-selectors-supercharged"
```

### Critical data.js Structure (MUST READ!)
**⚠️ Most Common Compilation Error: Wrong data.js Structure**

The dev-server expects this EXACT structure in data.js:

```javascript
const fs = require('fs');

function buildJson(directoryName) {
    const introContent = fs.readFileSync(`./${directoryName}/intro.html`, 'utf8');
    const article1Content = fs.readFileSync(`./${directoryName}/article-1.html`, 'utf8');
    // ... more articles

    return {
        intro: {
            title: "Newsletter Title",
            content: introContent,
        },
        articles: [
            // articles array
        ],
        unsubscribe_url: "{{unsubscribe_url}}",
        message_content: "{{message_content}}",
        subscriber: { first_name: "{{subscriber.first_name}}" }
    };
}

module.exports = buildJson; // Must export the function
```

**WRONG patterns that will cause compilation failure:**
- ❌ `module.exports = buildNewsletterData` (wrong function name)
- ❌ Using `__dirname` instead of `directoryName` parameter
- ❌ Not exporting a function that takes directoryName parameter

### Implementation Notes
- **🚨 CRITICAL: ALWAYS resolve redirect URLs to final destinations** - Use WebFetch for any `lnkd.in`, `bit.ly`, etc.
- **Always use `MCP.link` for article URLs**, never `MCP.url` (LinkedIn post URL)
- **CRITICAL: Create data.js with correct structure BEFORE creating content files**
- **Verify intro compilation immediately** after creating intro.html - intro should appear in output.html
- **✅ VERIFY: All article URLs must be final destinations, NOT redirect links**
- Use rotating default images when MCP returns null: Never repeat same image within a newsletter
- Auto-detect latest newsletter folder for sequential numbering
- Create Hebrew RTL content with proper `<div dir="rtl">` wrapping
- Generate compelling intro that connects all 4 article topics
- Update `availableNewsletters` array in index.html with extracted title/description
- **IMPORTANT**: When editing existing newsletter articles with new LinkedIn URLs, always update `linkedin_urls_registry.json` to reflect the changes

**Common URL Resolution Examples:**
- `https://lnkd.in/dYMXUjwW` → `https://tkdodo.eu/blog/react-query-selectors-supercharged`
- `https://lnkd.in/eTBnzM_h` → `https://tkdodo.eu/blog/deriving-client-state-from-server-state`
- `https://lnkd.in/dYzrk_rJ` → `https://tkdodo.eu/blog/the-useless-use-callback`

### Default Images Array
```javascript
const DEFAULT_IMAGES = [
  "https://www.21kschool.com/ua/wp-content/uploads/sites/6/2023/11/15-Facts-About-Coding-Every-Kid-Should-Know.png",
  "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg", 
  "https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png",
  "https://blog-cdn.codefinity.com/images/84cf0089-4483-4124-8388-a52baff28a6e_8fcdc9988f47418092f5013c41d6f358.png.png"
];
```