#!/usr/bin/env python3
"""
Meta (Facebook/Instagram) MCP Server - Simplified Version
Compatible with Python 3.9+
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MetaAPI:
    def __init__(self):
        self.app_id = os.getenv('META_APP_ID', '1667446050583846')
        self.access_token = os.getenv('META_ACCESS_TOKEN', '')
        self.base_url = 'https://graph.facebook.com/v18.0'
        self.session = None
        
    async def initialize_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    async def make_api_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        await self.initialize_session()
        
        url = f"{self.base_url}/{endpoint}"
        params = {'access_token': self.access_token}
        
        if method == 'GET' and data:
            params.update(data)
            data = None
        
        try:
            async with self.session.request(method, url, params=params, data=data) as response:
                result = await response.json()
                if response.status >= 400:
                    raise Exception(f"Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}")
                return result
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

class SimpleMCPServer:
    def __init__(self):
        self.meta_api = MetaAPI()
        self.tools = {
            "post_to_facebook_page": {
                "description": "Post content to a Facebook page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "Facebook page ID"},
                        "message": {"type": "string", "description": "Text content to post"},
                        "link": {"type": "string", "description": "Optional URL to include in post"}
                    },
                    "required": ["page_id", "message"]
                }
            },
            "post_to_instagram": {
                "description": "Post content to Instagram (requires Instagram Business Account)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "instagram_account_id": {"type": "string", "description": "Instagram Business Account ID"},
                        "image_url": {"type": "string", "description": "URL of image to post"},
                        "caption": {"type": "string", "description": "Caption for the Instagram post"}
                    },
                    "required": ["instagram_account_id", "image_url"]
                }
            },
            "get_facebook_page_insights": {
                "description": "Get analytics/insights for a Facebook page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "Facebook page ID"},
                        "metric": {"type": "string", "description": "Metric to retrieve", "default": "page_views"},
                        "period": {"type": "string", "description": "Time period", "default": "day"}
                    },
                    "required": ["page_id"]
                }
            },
            "get_instagram_insights": {
                "description": "Get analytics/insights for Instagram posts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "instagram_account_id": {"type": "string", "description": "Instagram Business Account ID"},
                        "metric": {"type": "string", "description": "Metric to retrieve", "default": "impressions"}
                    },
                    "required": ["instagram_account_id"]
                }
            },
            "generate_content_ideas": {
                "description": "Generate content ideas based on a topic or theme",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Topic or theme for content ideas"},
                        "platform": {"type": "string", "description": "Platform to optimize for", "default": "both"},
                        "count": {"type": "integer", "description": "Number of ideas to generate", "default": 5}
                    },
                    "required": ["topic"]
                }
            },
            "get_pages": {
                "description": "Get list of Facebook pages managed by the user",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC request"""
        try:
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            if method == 'initialize':
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "meta-mcp-server",
                            "version": "0.1.0"
                        }
                    }
                }
            
            elif method == 'tools/list':
                tools_list = []
                for name, tool_info in self.tools.items():
                    tools_list.append({
                        "name": name,
                        "description": tool_info["description"],
                        "inputSchema": tool_info["inputSchema"]
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tools_list
                    }
                }
            
            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})
                
                if tool_name not in self.tools:
                    raise Exception(f"Unknown tool: {tool_name}")
                
                result = await self.execute_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }
                }
            
            else:
                raise Exception(f"Unknown method: {method}")
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool and return the result"""
        
        if tool_name == "post_to_facebook_page":
            page_id = arguments.get("page_id")
            message = arguments.get("message")
            link = arguments.get("link")
            
            data = {"message": message}
            if link:
                data["link"] = link
            
            result = await self.meta_api.make_api_request(f"{page_id}/feed", "POST", data)
            return f"Successfully posted to Facebook page. Post ID: {result.get('id', 'Unknown')}"
        
        elif tool_name == "post_to_instagram":
            instagram_account_id = arguments.get("instagram_account_id")
            image_url = arguments.get("image_url")
            caption = arguments.get("caption", "")
            
            # Create media container
            container_data = {
                "image_url": image_url,
                "caption": caption
            }
            
            container_result = await self.meta_api.make_api_request(
                f"{instagram_account_id}/media", "POST", container_data
            )
            
            creation_id = container_result.get("id")
            
            # Publish media
            publish_data = {"creation_id": creation_id}
            publish_result = await self.meta_api.make_api_request(
                f"{instagram_account_id}/media_publish", "POST", publish_data
            )
            
            return f"Successfully posted to Instagram. Media ID: {publish_result.get('id', 'Unknown')}"
        
        elif tool_name == "get_facebook_page_insights":
            page_id = arguments.get("page_id")
            metric = arguments.get("metric", "page_views")
            period = arguments.get("period", "day")
            
            params = {
                "metric": metric,
                "period": period
            }
            
            result = await self.meta_api.make_api_request(f"{page_id}/insights", "GET", params)
            
            insights_text = f"Facebook Page Insights for {page_id}:\n"
            for data_point in result.get("data", []):
                insights_text += f"- {data_point.get('name', 'Unknown')}: {data_point.get('values', [{}])[0].get('value', 'N/A')}\n"
            
            return insights_text
        
        elif tool_name == "get_instagram_insights":
            instagram_account_id = arguments.get("instagram_account_id")
            metric = arguments.get("metric", "impressions")
            
            params = {"metric": metric}
            
            result = await self.meta_api.make_api_request(f"{instagram_account_id}/insights", "GET", params)
            
            insights_text = f"Instagram Insights for {instagram_account_id}:\n"
            for data_point in result.get("data", []):
                insights_text += f"- {data_point.get('name', 'Unknown')}: {data_point.get('values', [{}])[0].get('value', 'N/A')}\n"
            
            return insights_text
        
        elif tool_name == "generate_content_ideas":
            topic = arguments.get("topic")
            platform = arguments.get("platform", "both")
            count = arguments.get("count", 5)
            
            base_ideas = [
                f"Share a behind-the-scenes look at {topic}",
                f"Create a tutorial about {topic}",
                f"Ask your audience a question about {topic}",
                f"Share tips and tricks related to {topic}",
                f"Post inspirational quotes about {topic}",
                f"Share user-generated content about {topic}",
                f"Create a poll about {topic}",
                f"Share industry news related to {topic}",
                f"Post a carousel of {topic} facts",
                f"Create a before/after post about {topic}"
            ]
            
            platform_specific = {
                "facebook": " (optimize with longer text and links)",
                "instagram": " (use high-quality visuals and hashtags)",
                "both": " (adapt format for each platform)"
            }
            
            ideas = []
            for i in range(min(count, len(base_ideas))):
                ideas.append(base_ideas[i] + platform_specific[platform])
            
            ideas_text = f"Content Ideas for '{topic}' ({platform}):\n"
            for i, idea in enumerate(ideas, 1):
                ideas_text += f"{i}. {idea}\n"
            
            return ideas_text
        
        elif tool_name == "get_pages":
            result = await self.meta_api.make_api_request("me/accounts", "GET")
            
            pages_text = "Your Facebook Pages:\n"
            for page in result.get("data", []):
                pages_text += f"- {page.get('name', 'Unknown')} (ID: {page.get('id', 'Unknown')})\n"
            
            return pages_text
        
        else:
            raise Exception(f"Tool not implemented: {tool_name}")

async def main():
    """Main function to run the simplified MCP server"""
    server = SimpleMCPServer()
    
    # Read from stdin and write to stdout (MCP protocol)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)
    
    await server.meta_api.close_session()

if __name__ == "__main__":
    asyncio.run(main())