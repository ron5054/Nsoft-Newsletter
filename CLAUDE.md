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
4. **Summarize each post** into a Hebrew article (3-4 paragraphs)
5. **Create engaging intro** summarizing newsletter topics
6. **Build complete newsletter structure** with all required files
7. **Update index.html** with new newsletter entry
8. **Launch npm run dev** for preview

### Critical MCP Field Mapping
**⚠️ Common Error: Using Wrong Link Field!**

When MCP returns data, use the correct fields:
```
MCP Output → Newsletter Data:
- MCP.text → article content (after summarization)
- MCP.link → article.url ✅ (Use this, not MCP.url!)
- MCP.link_img → article.img
- MCP.url = LinkedIn post URL ❌ (Never use for article.url)
```

### Implementation Notes
- **Always use `MCP.link` for article URLs**, never `MCP.url` (LinkedIn post URL)
- **Use rotating default images when MCP returns null**: Never repeat same image within a newsletter
- Auto-detect latest newsletter folder for sequential numbering
- Create Hebrew RTL content with proper `<div dir="rtl">` wrapping
- Generate compelling intro that connects all 4 article topics
- Update `availableNewsletters` array in index.html with extracted title/description

### Default Images Array
```javascript
const DEFAULT_IMAGES = [
  "https://www.21kschool.com/ua/wp-content/uploads/sites/6/2023/11/15-Facts-About-Coding-Every-Kid-Should-Know.png",
  "https://www.goodcore.co.uk/blog/wp-content/uploads/2019/08/coding-vs-programming-2.jpg", 
  "https://www.milesweb.com/blog/wp-content/uploads/2023/10/learn-code-online-for-free.png",
  "https://blog-cdn.codefinity.com/images/84cf0089-4483-4124-8388-a52baff28a6e_8fcdc9988f47418092f5013c41d6f358.png.png"
];
```