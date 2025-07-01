# Meta MCP Server

A Model Context Protocol (MCP) server for integrating with Meta's platforms (Facebook and Instagram).

## Features

- **Web Interface**: Easy-to-use browser-based interface for content management
- Post content to Facebook pages
- Post content to Instagram Business accounts
- Get analytics and insights from both platforms
- Generate content ideas with AI assistance
- Manage Facebook pages
- Real-time content preview
- Character counters and validation
- Responsive design for mobile and desktop

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Meta app credentials
```

3. Run the application:

**Option A: Web Interface (Recommended)**
```bash
python3 web_app.py
```
Then open your browser to http://localhost:5000

**Option B: MCP Server (for integration with Claude/other MCP clients)**
```bash
python3 simple_server.py
```

**Option C: Full MCP Server (Python 3.10+ required)**
```bash
python3 server.py
```

4. Test the MCP server:
```bash
python3 test_server.py
```

## Configuration

Set the following environment variables:

- `META_APP_ID`: Your Meta app ID (default: 1667446050583846)
- `META_ACCESS_TOKEN`: Your Meta access token

## Tools Available

### post_to_facebook_page
Post content to a Facebook page.

**Parameters:**
- `page_id` (required): Facebook page ID
- `message` (required): Text content to post
- `link` (optional): URL to include in post

### post_to_instagram
Post content to Instagram (requires Instagram Business Account).

**Parameters:**
- `instagram_account_id` (required): Instagram Business Account ID
- `image_url` (required): URL of image to post
- `caption` (optional): Caption for the Instagram post

### get_facebook_page_insights
Get analytics/insights for a Facebook page.

**Parameters:**
- `page_id` (required): Facebook page ID
- `metric` (optional): Metric to retrieve (default: "page_views")
- `period` (optional): Time period (default: "day")

### get_instagram_insights
Get analytics/insights for Instagram posts.

**Parameters:**
- `instagram_account_id` (required): Instagram Business Account ID
- `metric` (optional): Metric to retrieve (default: "impressions")

### generate_content_ideas
Generate content ideas based on a topic or theme.

**Parameters:**
- `topic` (required): Topic or theme for content ideas
- `platform` (optional): Platform to optimize for (default: "both")
- `count` (optional): Number of ideas to generate (default: 5)

### get_pages
Get list of Facebook pages managed by the user.

**Parameters:** None

## Requirements

- Python 3.8+
- Meta app with appropriate permissions
- Facebook pages and/or Instagram Business accounts

## License

MIT