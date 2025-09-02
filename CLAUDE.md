# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Start development server**: `npm run dev`
  - Launches live server on port 8080 with auto-compilation
  - Watches for changes in .js, .html, and .hbs files
  - Opens http://localhost:8080/index.html
  - Auto-recompiles newsletter on file changes

- **Manual compilation**: `node compileNewsletter.js`
  - Compiles current newsletter (newsletter-23) using Handlebars template
  - Watches for changes in article files and recompiles automatically
  - Updates index.html with newsletter entries

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
4. Index page auto-updates with new newsletters via JavaScript array

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