# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **LinkedIn Post Text Extractor MCP Server** that implements the Model Context Protocol (MCP) specification. It extracts text content, links, and images from LinkedIn posts using a dual-extraction approach:

1. **Primary method**: `requests` + `BeautifulSoup` for public posts
2. **Fallback method**: `Playwright` for JavaScript-heavy content

## Key Architecture

### Core Components

- **linkedin_extractor.py**: Core extraction engine with dual-method extraction strategy
- **mcp_server.py**: Dual-mode MCP server (HTTP + stdio) with auto-detection for IDE integration
- **mcp_stdio_server.py**: Standalone stdio-only version for MCP clients
- **cli.py**: Command-line interface for testing and standalone usage
- **exceptions.py**: Custom exception classes (if needed)

### Extraction Strategy Flow

1. URL validation (LinkedIn post/pulse URLs only)
2. Attempt extraction with `requests` + `BeautifulSoup` (faster)
3. If fails, fallback to `Playwright` (handles JavaScript)
4. Extract text using multiple CSS selectors for different LinkedIn layouts
5. Extract first external link (prioritizes `lnkd.in` shortened links)
6. Extract first relevant image (skips profile pics, icons)
7. Generate `link_img` field (YouTube thumbnail > post image > null)

### MCP Protocol Implementation

**Dual Communication Modes:**
- **HTTP Mode**: FastAPI server on port 8000 for manual testing and web clients
- **Stdio Mode**: JSON-RPC via stdin/stdout for IDE integration (auto-detected)

**Implemented MCP Methods:**
- `initialize` - MCP session initialization with protocol version 2024-11-05
- `list_tools` - Returns available tools with proper schema
- `call_tool` - Executes the `get_linkedin_post_text` tool
- `get_linkedin_post_text` - Legacy direct method call support

## Common Development Commands

### Setup and Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required)
playwright install chromium
```

### Running the Server
```bash
# Start MCP server (HTTP mode for manual testing)
python mcp_server.py

# Test stdio mode (for MCP client integration)
echo '{"jsonrpc":"2.0","id":"1","method":"list_tools"}' | python mcp_server.py

# Alternative: Use dedicated stdio server
python mcp_stdio_server.py
```

### Testing
```bash
# Run all tests
python test_server.py

# Test extraction via CLI
python cli.py "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"

# Test with verbose logging
python cli.py -v "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"

# Save output to file
python cli.py -o output.json "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"
```

## Supported URL Formats

- `https://www.linkedin.com/posts/username_activity-*`
- `https://linkedin.com/posts/username_activity-*`
- `https://www.linkedin.com/pulse/*`
- `https://linkedin.com/pulse/*`

## Important Development Notes

### Link Resolution Strategy
The extractor intelligently resolves different types of LinkedIn links:
1. **`lnkd.in` URLs**: Fetches HTML content and extracts YouTube video IDs using regex patterns
2. **LinkedIn redirect URLs** (`/redir/redirect?url=...`): Parses URL parameters
3. **HTTP redirects**: Follows redirect chains (HEAD then GET fallback)
4. **YouTube Detection**: Handles multiple URL formats and query parameter orders

### CSS Selector Strategy
Uses multiple fallback selectors to handle different LinkedIn layouts:
- `[data-test-id="main-feed-activity-card"] .feed-shared-text`
- `.feed-shared-text`
- `.attributed-text-segment-list__content`
- `.break-words span[dir="ltr"]`

### Error Handling Patterns
- Graceful degradation (requests → Playwright → failure)
- Comprehensive URL validation
- Proper JSON-RPC error responses for MCP protocol
- Logging at appropriate levels (INFO for success, ERROR for failures, DEBUG for traces)

### Security Considerations
- No authentication credentials stored
- Standard HTTP headers to mimic real browsers
- 30-second timeout limits
- No content caching or storage
- Rate limiting considerations for bulk operations

## Integration

### IDE Integration (Cursor, Claude Desktop, etc.)
Add to your MCP configuration file (`~/.cursor/mcp.json` or similar):

```json
{
  "mcpServers": {
    "linkedin-extractor": {
      "command": "python",
      "args": ["C:\\path\\to\\linkedin-mcp\\mcp_server.py"],
      "env": {}
    }
  }
}
```

**Important Notes:**
- The server auto-detects stdio mode when launched by IDE
- Restart your IDE after updating MCP configuration
- Logs go to stderr to avoid interfering with stdio communication

### Manual HTTP Testing
```bash
# Start HTTP server for manual testing
python mcp_server.py

# Test health endpoint
curl http://localhost:8000/health
```

### Expected Output Format
```json
{
  "url": "https://www.linkedin.com/posts/username_activity-123...",
  "text": "Full extracted post content in original language",
  "link": "https://www.youtube.com/watch?v=kPL-6-9MVyA",
  "link_img": "https://img.youtube.com/vi/kPL-6-9MVyA/maxresdefault.jpg",
  "success": true
}
```

**Key Features:**
- **Multi-language support**: Handles Hebrew, English, and other languages
- **Smart link resolution**: `lnkd.in/shortcode` → Full YouTube URL
- **Auto-thumbnail generation**: YouTube thumbnails preferred over post images
- **Comprehensive extraction**: Text, links, and images in one request

## Troubleshooting

### Common Issues

**MCP Integration Problems:**
- Ensure absolute paths in MCP configuration
- Restart IDE completely after config changes
- Check that Python and dependencies are accessible from IDE context

**Extraction Failures:**
- Private/deleted posts return `success: false`
- JavaScript-heavy posts may need Playwright fallback
- Rate limiting: add delays between bulk requests

**Link Resolution Issues:**
- `lnkd.in` URLs require HTML parsing (not HTTP redirects)
- YouTube video ID extraction supports multiple URL formats
- Some LinkedIn layouts may use different CSS selectors

### Performance Notes
- Primary extraction (requests + BeautifulSoup) is faster
- Playwright fallback adds ~3-5 seconds but handles JS content
- YouTube thumbnail generation is instant once video ID is extracted

## Limitations
- Cannot access private posts or posts requiring authentication
- LinkedIn may rate limit requests (consider delays for bulk operations)
- Some heavily JavaScript-dependent posts may require Playwright fallback
- Must comply with LinkedIn's Terms of Service and robots.txt
- `lnkd.in` redirect resolution requires fetching full HTML content