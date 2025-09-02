# LinkedIn Post Text Extractor MCP Server

A Model Context Protocol (MCP) server that extracts text content from LinkedIn posts. This server provides a standardized interface for AI tools to fetch and analyze LinkedIn post content.

## Features

- **Dual Extraction Methods**: Uses requests + BeautifulSoup for public posts, falls back to Playwright for JavaScript-heavy content
- **MCP Protocol Compliance**: Full implementation of the MCP specification for seamless integration with AI tools
- **Error Handling**: Comprehensive error handling for invalid URLs, private posts, and network issues
- **CLI Support**: Command-line interface for testing and standalone usage
- **Production Ready**: Clean separation of concerns, logging, and robust error handling

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd linkedin-mcp
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (required for JavaScript-heavy posts)
   ```bash
   playwright install chromium
   ```

## Usage

### Running the MCP Server

Start the MCP server on the default port (8000):

```bash
python mcp_server.py
```

Or specify a custom host and port:

```bash
python -c "from mcp_server import LinkedInMCPServer; LinkedInMCPServer().run(host='127.0.0.1', port=8080)"
```

The server will be available at `http://localhost:8000` with the following endpoints:

- `POST /mcp` - MCP protocol endpoint
- `GET /health` - Health check endpoint

### Using the CLI Tool

Test the extractor directly from the command line:

```bash
# Basic usage
python cli.py "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"

# Save output to file
python cli.py -o output.json "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"

# Enable verbose logging
python cli.py -v "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"
```

### MCP Protocol Integration

The server implements the following MCP methods:

- `initialize` - Initialize the MCP session
- `list_tools` - List available tools
- `call_tool` - Execute the `get_linkedin_post_text` tool
- `get_linkedin_post_text` - Legacy direct method call

#### Tool Schema

```json
{
  "name": "get_linkedin_post_text",
  "description": "Extract text content from a LinkedIn post URL",
  "inputSchema": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "description": "The LinkedIn post URL to extract text from"
      }
    },
    "required": ["url"]
  }
}
```

### Integration with Cursor IDE

To connect this MCP server to Cursor IDE, add the following configuration to your MCP settings:

#### Option 1: Using the server directly

Add to your `mcp.json` or MCP configuration:

```json
{
  "mcpServers": {
    "linkedin-extractor": {
      "command": "python",
      "args": ["/path/to/linkedin-mcp/mcp_server.py"],
      "env": {}
    }
  }
}
```

#### Option 2: Using uvicorn (recommended for production)

```json
{
  "mcpServers": {
    "linkedin-extractor": {
      "command": "uvicorn",
      "args": [
        "mcp_server:LinkedInMCPServer().app",
        "--host", "127.0.0.1",
        "--port", "8000"
      ],
      "env": {},
      "cwd": "/path/to/linkedin-mcp"
    }
  }
}
```

#### Option 3: HTTP transport (if using external server)

```json
{
  "mcpServers": {
    "linkedin-extractor": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp"
      }
    }
  }
}
```

### Example Output

When successfully extracting text from a LinkedIn post, the server returns:

```json
{
  "url": "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd",
  "text": "This is the extracted text content from the LinkedIn post. It includes the main post text and any relevant content that was successfully parsed from the page.",
  "link": "https://lnkd.in/dW8J32mt",
  "success": true
}
```

When extraction fails:

```json
{
  "url": "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd",
  "text": null,
  "link": null,
  "error": "Could not extract text from post. Post may be private or unavailable.",
  "success": false
}
```

**Note**: The `link` field contains the first external link found in the post content (if any). LinkedIn shortened links (`lnkd.in`) are prioritized over other external links.

## How It Works

### Extraction Strategy

1. **URL Validation**: Validates that the provided URL is a valid LinkedIn post URL
2. **Primary Method**: Attempts to fetch the page using `requests` and parse with `BeautifulSoup`
3. **Fallback Method**: If the primary method fails, uses `Playwright` to handle JavaScript-rendered content
4. **Text Extraction**: Uses multiple CSS selectors to find post content across different LinkedIn layouts
5. **Text Cleaning**: Removes extra whitespace and formats the extracted text

### Supported URL Formats

- `https://www.linkedin.com/posts/username_activity-*`
- `https://linkedin.com/posts/username_activity-*`
- `https://www.linkedin.com/pulse/*`
- `https://linkedin.com/pulse/*`

## Limitations

- **Private Posts**: Cannot access private posts or posts that require authentication
- **Rate Limiting**: LinkedIn may rate limit requests; consider adding delays for bulk operations
- **Dynamic Content**: Some posts with heavy JavaScript may not be fully extracted
- **Legal Compliance**: Ensure your usage complies with LinkedIn's Terms of Service and robots.txt

## Development

### Project Structure

```
linkedin-mcp/
├── linkedin_extractor.py  # Core extraction logic
├── mcp_server.py         # MCP server implementation
├── exceptions.py         # Custom exceptions
├── cli.py               # Command-line interface
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Testing

Test the extractor with various LinkedIn post URLs:

```bash
# Test with a public post
python cli.py "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"

# Test error handling with invalid URL
python cli.py "https://invalid-url.com"

# Test with verbose logging
python cli.py -v "https://www.linkedin.com/posts/username_activity-1234567890123456789-abcd"
```

### Logging

The application uses Python's built-in logging module. Set the logging level to see detailed extraction information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with LinkedIn's Terms of Service when using this tool.

## Troubleshooting

### Common Issues

1. **"Could not extract text from post"**
   - The post may be private or deleted
   - LinkedIn's layout may have changed
   - Try enabling verbose logging to see more details

2. **Playwright installation issues**
   - Run `playwright install chromium` to install the required browser
   - Ensure you have sufficient disk space

3. **Network timeouts**
   - Some posts may take longer to load
   - The tool includes a 30-second timeout by default

4. **MCP connection issues**
   - Verify the server is running on the correct port
   - Check your MCP configuration file syntax
   - Ensure the Python path is correct in your configuration

### Getting Help

- Check the logs for detailed error information
- Use the CLI tool to test extraction before integrating with MCP
- Ensure all dependencies are properly installed
- Verify that the LinkedIn URL is accessible in your browser

## Security Notes

- This tool does not store or cache any LinkedIn content
- No authentication credentials are required or stored
- All network requests use standard HTTP headers
- Consider running the server behind a firewall in production environments