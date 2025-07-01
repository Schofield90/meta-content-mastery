#!/usr/bin/env python3
"""
Meta (Facebook/Instagram) MCP Server

This server provides tools for interacting with Meta's platforms including:
- Posting content to Facebook pages
- Posting content to Instagram
- Getting analytics from both platforms
- Content creation helpers
"""

import asyncio
import json
import os
from typing import Any, Sequence
from urllib.parse import urlencode
import aiohttp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetaMCPServer:
    def __init__(self):
        self.app_id = os.getenv('META_APP_ID', '1667446050583846')
        self.access_token = os.getenv('META_ACCESS_TOKEN', '')
        self.base_url = 'https://graph.facebook.com/v18.0'
        self.session = None
        
    async def initialize_session(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def make_api_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        """Make a request to Meta Graph API"""
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
                    logger.error(f"API Error: {result}")
                    raise Exception(f"Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}")
                return result
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

# Initialize the MCP server
server = Server("meta-mcp-server")
meta_server = MetaMCPServer()

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="post_to_facebook_page",
            description="Post content to a Facebook page",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "Facebook page ID"
                    },
                    "message": {
                        "type": "string",
                        "description": "Text content to post"
                    },
                    "link": {
                        "type": "string",
                        "description": "Optional URL to include in post"
                    }
                },
                "required": ["page_id", "message"]
            }
        ),
        Tool(
            name="post_to_instagram",
            description="Post content to Instagram (requires Instagram Business Account)",
            inputSchema={
                "type": "object",
                "properties": {
                    "instagram_account_id": {
                        "type": "string",
                        "description": "Instagram Business Account ID"
                    },
                    "image_url": {
                        "type": "string",
                        "description": "URL of image to post"
                    },
                    "caption": {
                        "type": "string",
                        "description": "Caption for the Instagram post"
                    }
                },
                "required": ["instagram_account_id", "image_url"]
            }
        ),
        Tool(
            name="get_facebook_page_insights",
            description="Get analytics/insights for a Facebook page",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "Facebook page ID"
                    },
                    "metric": {
                        "type": "string",
                        "description": "Metric to retrieve (e.g., page_views, page_fans, page_impressions)",
                        "default": "page_views"
                    },
                    "period": {
                        "type": "string",
                        "description": "Time period (day, week, days_28)",
                        "default": "day"
                    }
                },
                "required": ["page_id"]
            }
        ),
        Tool(
            name="get_instagram_insights",
            description="Get analytics/insights for Instagram posts",
            inputSchema={
                "type": "object",
                "properties": {
                    "instagram_account_id": {
                        "type": "string",
                        "description": "Instagram Business Account ID"
                    },
                    "metric": {
                        "type": "string",
                        "description": "Metric to retrieve (e.g., impressions, reach, engagement)",
                        "default": "impressions"
                    }
                },
                "required": ["instagram_account_id"]
            }
        ),
        Tool(
            name="generate_content_ideas",
            description="Generate content ideas based on a topic or theme",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic or theme for content ideas"
                    },
                    "platform": {
                        "type": "string",
                        "description": "Platform to optimize for (facebook, instagram, both)",
                        "default": "both"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of ideas to generate",
                        "default": 5
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="get_pages",
            description="Get list of Facebook pages managed by the user",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool execution"""
    if not arguments:
        arguments = {}
    
    try:
        if name == "post_to_facebook_page":
            return await post_to_facebook_page(arguments)
        elif name == "post_to_instagram":
            return await post_to_instagram(arguments)
        elif name == "get_facebook_page_insights":
            return await get_facebook_page_insights(arguments)
        elif name == "get_instagram_insights":
            return await get_instagram_insights(arguments)
        elif name == "generate_content_ideas":
            return await generate_content_ideas(arguments)
        elif name == "get_pages":
            return await get_pages(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def post_to_facebook_page(args: dict) -> list[TextContent]:
    """Post content to a Facebook page"""
    page_id = args.get("page_id")
    message = args.get("message")
    link = args.get("link")
    
    data = {"message": message}
    if link:
        data["link"] = link
    
    result = await meta_server.make_api_request(f"{page_id}/feed", "POST", data)
    
    return [TextContent(
        type="text", 
        text=f"Successfully posted to Facebook page. Post ID: {result.get('id', 'Unknown')}"
    )]

async def post_to_instagram(args: dict) -> list[TextContent]:
    """Post content to Instagram"""
    instagram_account_id = args.get("instagram_account_id")
    image_url = args.get("image_url")
    caption = args.get("caption", "")
    
    # First, create the media container
    container_data = {
        "image_url": image_url,
        "caption": caption
    }
    
    container_result = await meta_server.make_api_request(
        f"{instagram_account_id}/media", "POST", container_data
    )
    
    creation_id = container_result.get("id")
    
    # Then publish the media
    publish_data = {"creation_id": creation_id}
    publish_result = await meta_server.make_api_request(
        f"{instagram_account_id}/media_publish", "POST", publish_data
    )
    
    return [TextContent(
        type="text", 
        text=f"Successfully posted to Instagram. Media ID: {publish_result.get('id', 'Unknown')}"
    )]

async def get_facebook_page_insights(args: dict) -> list[TextContent]:
    """Get Facebook page insights"""
    page_id = args.get("page_id")
    metric = args.get("metric", "page_views")
    period = args.get("period", "day")
    
    params = {
        "metric": metric,
        "period": period
    }
    
    result = await meta_server.make_api_request(f"{page_id}/insights", "GET", params)
    
    insights_text = f"Facebook Page Insights for {page_id}:\n"
    for data_point in result.get("data", []):
        insights_text += f"- {data_point.get('name', 'Unknown')}: {data_point.get('values', [{}])[0].get('value', 'N/A')}\n"
    
    return [TextContent(type="text", text=insights_text)]

async def get_instagram_insights(args: dict) -> list[TextContent]:
    """Get Instagram insights"""
    instagram_account_id = args.get("instagram_account_id")
    metric = args.get("metric", "impressions")
    
    params = {
        "metric": metric
    }
    
    result = await meta_server.make_api_request(f"{instagram_account_id}/insights", "GET", params)
    
    insights_text = f"Instagram Insights for {instagram_account_id}:\n"
    for data_point in result.get("data", []):
        insights_text += f"- {data_point.get('name', 'Unknown')}: {data_point.get('values', [{}])[0].get('value', 'N/A')}\n"
    
    return [TextContent(type="text", text=insights_text)]

async def generate_content_ideas(args: dict) -> list[TextContent]:
    """Generate content ideas"""
    topic = args.get("topic")
    platform = args.get("platform", "both")
    count = args.get("count", 5)
    
    # Simple content idea generator
    ideas = []
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
    
    for i in range(min(count, len(base_ideas))):
        ideas.append(base_ideas[i] + platform_specific[platform])
    
    ideas_text = f"Content Ideas for '{topic}' ({platform}):\n"
    for i, idea in enumerate(ideas, 1):
        ideas_text += f"{i}. {idea}\n"
    
    return [TextContent(type="text", text=ideas_text)]

async def get_pages(args: dict) -> list[TextContent]:
    """Get list of Facebook pages"""
    result = await meta_server.make_api_request("me/accounts", "GET")
    
    pages_text = "Your Facebook Pages:\n"
    for page in result.get("data", []):
        pages_text += f"- {page.get('name', 'Unknown')} (ID: {page.get('id', 'Unknown')})\n"
    
    return [TextContent(type="text", text=pages_text)]

async def main():
    """Main function to run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="meta-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())