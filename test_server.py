#!/usr/bin/env python3
"""Test script for the Meta MCP Server"""

import json
import asyncio
from simple_server import SimpleMCPServer

async def test_server():
    """Test the MCP server functionality"""
    server = SimpleMCPServer()
    
    # Test initialize
    print("Testing initialize...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    response = await server.handle_request(init_request)
    print(f"Initialize response: {json.dumps(response, indent=2)}")
    
    # Test tools/list
    print("\nTesting tools/list...")
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    response = await server.handle_request(list_request)
    print(f"Tools list response: {json.dumps(response, indent=2)}")
    
    # Test generate_content_ideas
    print("\nTesting generate_content_ideas...")
    content_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "generate_content_ideas",
            "arguments": {
                "topic": "artificial intelligence",
                "platform": "both",
                "count": 3
            }
        }
    }
    
    response = await server.handle_request(content_request)
    print(f"Content ideas response: {json.dumps(response, indent=2)}")
    
    await server.meta_api.close_session()

if __name__ == "__main__":
    asyncio.run(test_server())