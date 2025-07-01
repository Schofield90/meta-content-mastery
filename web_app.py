#!/usr/bin/env python3
"""
Meta MCP Server Web Interface
A Flask-based web application for easy content creation and posting
"""

import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

class MetaAPI:
    def __init__(self):
        self.app_id = os.getenv('META_APP_ID', '1667446050583846')
        self.access_token = os.getenv('META_ACCESS_TOKEN', '')
        self.base_url = 'https://graph.facebook.com/v18.0'
    
    def make_api_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        """Make a request to Meta Graph API"""
        url = f"{self.base_url}/{endpoint}"
        params = {'access_token': self.access_token}
        
        if method == 'GET' and data:
            params.update(data)
            data = None
        
        try:
            response = requests.request(method, url, params=params, data=data)
            result = response.json()
            if response.status_code >= 400:
                raise Exception(f"Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}")
            return result
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

# Initialize Meta API
meta_api = MetaAPI()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/pages')
def pages():
    """Get user's Facebook pages"""
    try:
        result = meta_api.make_api_request("me/accounts", "GET")
        pages = result.get("data", [])
        return render_template('pages.html', pages=pages)
    except Exception as e:
        flash(f"Error fetching pages: {str(e)}", 'error')
        return render_template('pages.html', pages=[])

@app.route('/create-content')
def create_content():
    """Content creation page"""
    return render_template('create_content.html')

@app.route('/generate-ideas', methods=['POST'])
def generate_ideas():
    """Generate content ideas"""
    topic = request.form.get('topic', '')
    platform = request.form.get('platform', 'both')
    count = int(request.form.get('count', 5))
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Simple content idea generator
    base_ideas = [
        f"Share a behind-the-scenes look at {topic}",
        f"Create a tutorial or how-to about {topic}",
        f"Ask your audience a question about {topic}",
        f"Share tips and tricks related to {topic}",
        f"Post inspirational quotes about {topic}",
        f"Share user-generated content about {topic}",
        f"Create a poll or survey about {topic}",
        f"Share industry news related to {topic}",
        f"Post a carousel of {topic} facts",
        f"Create a before/after post about {topic}",
        f"Share a success story related to {topic}",
        f"Post a funny meme about {topic}",
        f"Create a step-by-step guide for {topic}",
        f"Share your personal experience with {topic}",
        f"Post a comparison related to {topic}"
    ]
    
    platform_specific = {
        "facebook": " (optimize with longer text and links)",
        "instagram": " (use high-quality visuals and hashtags)",
        "both": " (adapt format for each platform)"
    }
    
    ideas = []
    for i in range(min(count, len(base_ideas))):
        ideas.append({
            'text': base_ideas[i] + platform_specific[platform],
            'platform': platform
        })
    
    return jsonify({'ideas': ideas})

@app.route('/post-facebook', methods=['GET', 'POST'])
def post_facebook():
    """Post to Facebook page"""
    if request.method == 'GET':
        # Get user's pages for the form
        try:
            result = meta_api.make_api_request("me/accounts", "GET")
            pages = result.get("data", [])
            return render_template('post_facebook.html', pages=pages)
        except Exception as e:
            flash(f"Error fetching pages: {str(e)}", 'error')
            return render_template('post_facebook.html', pages=[])
    
    # Handle POST request
    page_id = request.form.get('page_id')
    message = request.form.get('message')
    link = request.form.get('link', '')
    
    if not page_id or not message:
        flash('Page and message are required', 'error')
        return redirect(url_for('post_facebook'))
    
    try:
        data = {"message": message}
        if link:
            data["link"] = link
        
        result = meta_api.make_api_request(f"{page_id}/feed", "POST", data)
        flash(f"Successfully posted to Facebook! Post ID: {result.get('id', 'Unknown')}", 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f"Error posting to Facebook: {str(e)}", 'error')
        return redirect(url_for('post_facebook'))

@app.route('/post-instagram', methods=['GET', 'POST'])
def post_instagram():
    """Post to Instagram"""
    if request.method == 'GET':
        return render_template('post_instagram.html')
    
    # Handle POST request
    instagram_account_id = request.form.get('instagram_account_id')
    image_url = request.form.get('image_url')
    caption = request.form.get('caption', '')
    
    if not instagram_account_id or not image_url:
        flash('Instagram account ID and image URL are required', 'error')
        return redirect(url_for('post_instagram'))
    
    try:
        # Create media container
        container_data = {
            "image_url": image_url,
            "caption": caption
        }
        
        container_result = meta_api.make_api_request(
            f"{instagram_account_id}/media", "POST", container_data
        )
        
        creation_id = container_result.get("id")
        
        # Publish media
        publish_data = {"creation_id": creation_id}
        publish_result = meta_api.make_api_request(
            f"{instagram_account_id}/media_publish", "POST", publish_data
        )
        
        flash(f"Successfully posted to Instagram! Media ID: {publish_result.get('id', 'Unknown')}", 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f"Error posting to Instagram: {str(e)}", 'error')
        return redirect(url_for('post_instagram'))

@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    return render_template('analytics.html')

@app.route('/facebook-insights', methods=['POST'])
def facebook_insights():
    """Get Facebook page insights"""
    page_id = request.form.get('page_id')
    metric = request.form.get('metric', 'page_views')
    period = request.form.get('period', 'day')
    
    if not page_id:
        return jsonify({'error': 'Page ID is required'}), 400
    
    try:
        params = {
            "metric": metric,
            "period": period
        }
        
        result = meta_api.make_api_request(f"{page_id}/insights", "GET", params)
        
        insights = []
        for data_point in result.get("data", []):
            insights.append({
                'name': data_point.get('name', 'Unknown'),
                'value': data_point.get('values', [{}])[0].get('value', 'N/A'),
                'period': data_point.get('period', 'Unknown')
            })
        
        return jsonify({'insights': insights})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instagram-insights', methods=['POST'])
def instagram_insights():
    """Get Instagram insights"""
    instagram_account_id = request.form.get('instagram_account_id')
    metric = request.form.get('metric', 'impressions')
    
    if not instagram_account_id:
        return jsonify({'error': 'Instagram account ID is required'}), 400
    
    try:
        params = {"metric": metric}
        
        result = meta_api.make_api_request(f"{instagram_account_id}/insights", "GET", params)
        
        insights = []
        for data_point in result.get("data", []):
            insights.append({
                'name': data_point.get('name', 'Unknown'),
                'value': data_point.get('values', [{}])[0].get('value', 'N/A')
            })
        
        return jsonify({'insights': insights})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)