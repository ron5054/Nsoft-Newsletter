#!/usr/bin/env python3
"""
DEBUG MCP Server for LinkedIn post text extraction.
This version logs everything to debug Cursor integration issues.
"""

import asyncio
import sys
import json
import logging
import os
import datetime
from typing import Any, Dict
import traceback
import concurrent.futures

from linkedin_extractor import LinkedInExtractor

# Setup detailed file logging
log_file = os.path.join(os.path.dirname(__file__), 'mcp_debug.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

class DebugLinkedInMCPServer:
    """DEBUG MCP Server for LinkedIn post text extraction via stdio."""
    
    def __init__(self):
        logger.info("="*80)
        logger.info(f"DEBUG MCP SERVER STARTING - {datetime.datetime.now()}")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Script path: {__file__}")
        logger.info(f"Log file: {log_file}")
        logger.info(f"Process ID: {os.getpid()}")
        logger.info(f"Arguments: {sys.argv}")
        logger.info(f"Environment PATH: {os.environ.get('PATH', 'NOT SET')}")
        logger.info(f"Environment PYTHONPATH: {os.environ.get('PYTHONPATH', 'NOT SET')}")
        logger.info(f"stdin.isatty(): {sys.stdin.isatty()}")
        logger.info(f"stdout.isatty(): {sys.stdout.isatty()}")
        logger.info("="*80)
        
        try:
            self.extractor = LinkedInExtractor()
            logger.info("LinkedIn extractor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LinkedIn extractor: {e}")
            logger.error(traceback.format_exc())
            raise
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests with detailed logging."""
        logger.info("-" * 60)
        logger.info(f"INCOMING REQUEST: {json.dumps(request, indent=2)}")
        
        try:
            method = request.get('method', 'unknown')
            request_id = request.get('id', 'no-id')
            
            logger.info(f"Processing method: {method} (ID: {request_id})")
            
            if method == "initialize":
                response = await self._handle_initialize(request)
            elif method == "get_linkedin_post_text":
                response = await self._handle_get_post_text(request)
            elif method == "list_tools":
                response = await self._handle_list_tools(request)
            elif method == "call_tool":
                response = await self._handle_call_tool(request)
            else:
                logger.warning(f"Unknown method: {method}")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            logger.info(f"OUTGOING RESPONSE: {json.dumps(response, indent=2)}")
            logger.info("-" * 60)
            return response
            
        except Exception as e:
            logger.error(f"ERROR handling request: {e}")
            logger.error(traceback.format_exc())
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
            logger.info(f"OUTGOING ERROR RESPONSE: {json.dumps(error_response, indent=2)}")
            return error_response
    
    async def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        logger.info("Handling initialize request")
        params = request.get("params", {})
        logger.info(f"Initialize params: {json.dumps(params, indent=2)}")
        
        response = {
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
        logger.info("Initialize response prepared")
        return response
    
    async def _handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_tools request."""
        logger.info("Handling list_tools request")
        
        response = {
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
        logger.info(f"Returning {len(response['result']['tools'])} tools")
        return response
    
    async def _handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call_tool request."""
        logger.info("Handling call_tool request")
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Tool: {tool_name}, Arguments: {json.dumps(arguments)}")
        
        if tool_name == "get_linkedin_post_text":
            return await self._handle_get_post_text_tool(request.get("id"), arguments)
        else:
            logger.warning(f"Unknown tool: {tool_name}")
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
        logger.info(f"Extracting post text with arguments: {json.dumps(arguments)}")
        
        url = arguments.get("url")
        if not url:
            logger.error("No URL provided in arguments")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            }
        
        try:
            logger.info(f"Extracting from URL: {url}")
            result = await self.extractor.extract_post_text(url)
            logger.info(f"Extraction successful: {json.dumps(result)}")
            
            response = {
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
            return response
            
        except Exception as e:
            logger.error(f"Error extracting post text: {e}")
            logger.error(traceback.format_exc())
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
        logger.info("Handling direct get_post_text request")
        params = request.get("params", {})
        url = params.get("url")
        
        if not url:
            logger.error("No URL provided in params")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32602,
                    "message": "Invalid params: url required"
                }
            }
        
        try:
            logger.info(f"Extracting from URL (direct): {url}")
            result = await self.extractor.extract_post_text(url)
            logger.info(f"Direct extraction successful: {json.dumps(result)}")
            
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error in direct extraction: {e}")
            logger.error(traceback.format_exc())
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
        logger.info("STARTING STDIO COMMUNICATION LOOP")
        
        # Use a thread executor for stdin reading on Windows
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        
        def read_line():
            """Read a line from stdin in a thread."""
            try:
                logger.debug("Waiting for stdin input...")
                line = sys.stdin.readline()
                logger.debug(f"Read from stdin: {repr(line)}")
                return line
            except EOFError:
                logger.info("EOF received from stdin")
                return None
            except Exception as e:
                logger.error(f"Error reading from stdin: {e}")
                return None
        
        request_count = 0
        try:
            while True:
                try:
                    logger.debug("Awaiting next request...")
                    
                    # Read request from stdin asynchronously using thread executor
                    line = await loop.run_in_executor(executor, read_line)
                    if not line:
                        logger.info("No more input, shutting down")
                        break
                    
                    line = line.strip()
                    if not line:
                        logger.debug("Empty line, continuing...")
                        continue
                    
                    request_count += 1
                    logger.info(f"REQUEST #{request_count}: Received {len(line)} characters")
                    
                    # Parse JSON request
                    try:
                        request = json.loads(line)
                        logger.info(f"REQUEST #{request_count}: JSON parsed successfully")
                    except json.JSONDecodeError as e:
                        logger.error(f"REQUEST #{request_count}: JSON decode error: {e}")
                        logger.error(f"Raw input: {repr(line)}")
                        error_response = {
                            "jsonrpc": "2.0",
                            "id": None,
                            "error": {
                                "code": -32700,
                                "message": "Parse error"
                            }
                        }
                        output = json.dumps(error_response)
                        print(output, flush=True)
                        logger.info(f"REQUEST #{request_count}: Sent parse error response")
                        continue
                    
                    # Handle request
                    logger.info(f"REQUEST #{request_count}: Processing request")
                    response = await self.handle_request(request)
                    
                    # Send response to stdout
                    output = json.dumps(response)
                    print(output, flush=True)
                    logger.info(f"REQUEST #{request_count}: Response sent to stdout ({len(output)} chars)")
                    
                except Exception as e:
                    logger.error(f"REQUEST #{request_count}: Unexpected error in main loop: {e}")
                    logger.error(traceback.format_exc())
                    break
                    
        finally:
            executor.shutdown(wait=True)
            logger.info(f"STDIO COMMUNICATION ENDED - Processed {request_count} requests")


async def main():
    """Main entry point."""
    try:
        server = DebugLinkedInMCPServer()
        await server.run_stdio()
    except Exception as e:
        logger.error(f"FATAL ERROR in main: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("DEBUG MCP SERVER SHUTTING DOWN")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, shutting down")
    except Exception as e:
        logger.error(f"FATAL ERROR: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)