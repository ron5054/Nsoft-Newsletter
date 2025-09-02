#!/usr/bin/env python3
"""
MCP Server stdio launcher for LinkedIn post text extraction.
This version communicates via stdin/stdout for IDE integration.
"""

import asyncio
import sys
import json
import logging
from typing import Any, Dict

from linkedin_extractor import LinkedInExtractor

# Configure logging to stderr so it doesn't interfere with stdio communication
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


class LinkedInMCPStdioServer:
    """MCP Server for LinkedIn post text extraction via stdio."""
    
    def __init__(self):
        self.extractor = LinkedInExtractor()
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests."""
        try:
            logger.info(f"Received MCP request: {request.get('method', 'unknown')}")
            
            if request.get("method") == "initialize":
                return await self._handle_initialize(request)
            elif request.get("method") == "get_linkedin_post_text":
                return await self._handle_get_post_text(request)
            elif request.get("method") == "list_tools":
                return await self._handle_list_tools(request)
            elif request.get("method") == "call_tool":
                return await self._handle_call_tool(request)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {request.get('method', 'unknown')}"
                    }
                }
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
    
    async def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "linkedin-post-extractor",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }
    
    async def _handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_tools request."""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
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
        }
    
    async def _handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call_tool request."""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_linkedin_post_text":
            return await self._handle_get_post_text_tool(request.get("id"), arguments)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                }
            }
    
    async def _handle_get_post_text_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the get_linkedin_post_text tool call."""
        url = arguments.get("url")
        if not url:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            }
        
        try:
            result = await self.extractor.extract_post_text(url)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Error extracting post text: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Failed to extract post text",
                    "data": str(e)
                }
            }
    
    async def _handle_get_post_text(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle direct get_linkedin_post_text method call (legacy support)."""
        params = request.get("params", {})
        url = params.get("url")
        if not url:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            }
        
        try:
            result = await self.extractor.extract_post_text(url)
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": result
            }
        except Exception as e:
            logger.error(f"Error extracting post text: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Failed to extract post text",
                    "data": str(e)
                }
            }
    
    async def run_stdio(self):
        """Run the MCP server using stdio communication."""
        logger.info("Starting LinkedIn MCP Server in stdio mode")
        
        # Use a thread executor for stdin reading on Windows
        import concurrent.futures
        import threading
        
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
                    request = json.loads(line)
                    
                    # Handle request
                    response = await self.handle_request(request)
                    
                    # Send response to stdout
                    print(json.dumps(response), flush=True)
                    
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


async def main():
    """Main entry point."""
    server = LinkedInMCPStdioServer()
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())