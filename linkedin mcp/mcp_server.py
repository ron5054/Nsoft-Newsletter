"""
MCP Server implementation for LinkedIn post text extraction.
Implements the Model Context Protocol specification with FastAPI.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from linkedin_extractor import LinkedInExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPRequest(BaseModel):
    """MCP request model."""
    jsonrpc: str = Field(default="2.0")
    id: Optional[str] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""
    jsonrpc: str = Field(default="2.0")
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class MCPError(BaseModel):
    """MCP error model."""
    code: int
    message: str
    data: Optional[Any] = None


class LinkedInMCPServer:
    """MCP Server for LinkedIn post text extraction."""
    
    def __init__(self):
        self.app = FastAPI(
            title="LinkedIn Post Text Extractor MCP Server",
            description="MCP server for extracting text content from LinkedIn posts",
            version="1.0.0"
        )
        self.extractor = LinkedInExtractor()
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up FastAPI routes for MCP protocol."""
        
        @self.app.post("/mcp", response_model=MCPResponse)
        async def handle_mcp_request(request: MCPRequest) -> MCPResponse:
            """Handle incoming MCP requests."""
            try:
                logger.info(f"Received MCP request: {request.method}")
                
                if request.method == "initialize":
                    return await self._handle_initialize(request)
                elif request.method == "get_linkedin_post_text":
                    return await self._handle_get_post_text(request)
                elif request.method == "list_tools":
                    return await self._handle_list_tools(request)
                elif request.method == "call_tool":
                    return await self._handle_call_tool(request)
                else:
                    return MCPResponse(
                        id=request.id,
                        error={
                            "code": -32601,
                            "message": f"Method not found: {request.method}"
                        }
                    )
                    
            except Exception as e:
                logger.error(f"Error handling MCP request: {e}")
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    }
                )
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "linkedin-mcp-server"}
    
    async def _handle_initialize(self, request: MCPRequest) -> MCPResponse:
        """Handle MCP initialize request."""
        return MCPResponse(
            id=request.id,
            result={
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "linkedin-post-extractor",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        )
    
    async def _handle_list_tools(self, request: MCPRequest) -> MCPResponse:
        """Handle list_tools request."""
        return MCPResponse(
            id=request.id,
            result={
                "tools": [
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
                ]
            }
        )
    
    async def _handle_call_tool(self, request: MCPRequest) -> MCPResponse:
        """Handle call_tool request."""
        if not request.params:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": "Invalid params: params required"
                }
            )
        
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        if tool_name == "get_linkedin_post_text":
            return await self._handle_get_post_text_tool(request.id, arguments)
        else:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            )
    
    async def _handle_get_post_text_tool(self, request_id: Optional[str], arguments: Dict[str, Any]) -> MCPResponse:
        """Handle the get_linkedin_post_text tool call."""
        url = arguments.get("url")
        if not url:
            return MCPResponse(
                id=request_id,
                error={
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            )
        
        try:
            result = await self.extractor.extract_post_text(url)
            return MCPResponse(
                id=request_id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            )
        except Exception as e:
            logger.error(f"Error extracting post text: {e}")
            return MCPResponse(
                id=request_id,
                error={
                    "code": -32603,
                    "message": "Failed to extract post text",
                    "data": str(e)
                }
            )
    
    async def _handle_get_post_text(self, request: MCPRequest) -> MCPResponse:
        """Handle direct get_linkedin_post_text method call (legacy support)."""
        if not request.params:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            )
        
        url = request.params.get("url")
        if not url:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            )
        
        try:
            result = await self.extractor.extract_post_text(url)
            return MCPResponse(
                id=request.id,
                result=result
            )
        except Exception as e:
            logger.error(f"Error extracting post text: {e}")
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32603,
                    "message": "Failed to extract post text",
                    "data": str(e)
                }
            )
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the MCP server."""
        logger.info(f"Starting LinkedIn MCP Server on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


async def run_stdio():
    """Run the MCP server using stdio communication for IDE integration."""
    import sys
    import concurrent.futures
    
    # Configure logging to stderr so it doesn't interfere with stdio communication
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    logger = logging.getLogger(__name__)
    
    server = LinkedInMCPServer()
    logger.info("Starting LinkedIn MCP Server in stdio mode")
    
    # Use a thread executor for stdin reading on Windows
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    
    def read_line():
        """Read a line from stdin in a thread."""
        try:
            return sys.stdin.readline()
        except EOFError:
            return None
    
    try:
        while True:
            try:
                # Read request from stdin asynchronously using thread executor
                line = await loop.run_in_executor(executor, read_line)
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON request
                request_data = json.loads(line)
                
                # Create MCPRequest object
                request = MCPRequest(**request_data)
                
                # Handle request using existing FastAPI handler logic
                if request.method == "initialize":
                    response = await server._handle_initialize(request)
                elif request.method == "get_linkedin_post_text":
                    response = await server._handle_get_post_text(request)
                elif request.method == "list_tools":
                    response = await server._handle_list_tools(request)
                elif request.method == "call_tool":
                    response = await server._handle_call_tool(request)
                else:
                    response = MCPResponse(
                        id=request.id,
                        error={
                            "code": -32601,
                            "message": f"Method not found: {request.method}"
                        }
                    )
                
                # Convert response to dict and send to stdout
                if hasattr(response, 'dict'):
                    response_dict = response.dict(exclude_none=True)
                else:
                    response_dict = response
                
                print(json.dumps(response_dict), flush=True)
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON request: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                break
    finally:
        executor.shutdown(wait=True)


def main():
    """Main entry point - detects if running in stdio or HTTP mode."""
    import sys
    
    # Check if stdin is available (IDE integration) or if we should run HTTP server
    if sys.stdin.isatty():
        # Running interactively, start HTTP server
        server = LinkedInMCPServer()
        server.run()
    else:
        # Running via IDE/MCP client, use stdio
        asyncio.run(run_stdio())


if __name__ == "__main__":
    main()