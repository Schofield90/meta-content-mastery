#!/usr/bin/env python3
"""
Meta Content Manager - Simplified for Vercel
"""

import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'meta-content-manager-secret-key')

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
            response = requests.request(method, url, params=params, data=data, timeout=25)
            result = response.json()
            if response.status_code >= 400:
                raise Exception(f"Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}")
            return result
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

meta_api = MetaAPI()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'app': 'Meta Content Manager'})

@app.route('/test')
def test():
    """Simple test route"""
    return "<h1>Meta Content Manager is Working!</h1><p>Environment variables loaded successfully.</p>"

@app.route('/pages')
def pages():
    """Get user's Facebook pages"""
    try:
        if not meta_api.access_token:
            flash('Meta access token not configured', 'error')
            return render_template('pages.html', pages=[])
            
        result = meta_api.make_api_request("me/accounts", "GET")
        pages_data = result.get("data", [])
        return render_template('pages.html', pages=pages_data)
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
    try:
        topic = request.form.get('topic', '').strip()
        platform = request.form.get('platform', 'both')
        count = int(request.form.get('count', 5))
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
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
        
        platform_tips = {
            "facebook": " (use longer text and links)",
            "instagram": " (use visuals and hashtags)",
            "both": " (adapt for each platform)"
        }
        
        ideas = []
        for i in range(min(count, len(base_ideas))):
            ideas.append({
                'text': base_ideas[i] + platform_tips[platform],
                'platform': platform
            })
        
        return jsonify({'ideas': ideas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/post-facebook', methods=['GET', 'POST'])
def post_facebook():
    """Post to Facebook page"""
    if request.method == 'GET':
        try:
            if not meta_api.access_token:
                flash('Meta access token not configured', 'error')
                return render_template('post_facebook.html', pages=[])
                
            result = meta_api.make_api_request("me/accounts", "GET")
            pages_data = result.get("data", [])
            return render_template('post_facebook.html', pages=pages_data)
        except Exception as e:
            flash(f"Error fetching pages: {str(e)}", 'error')
            return render_template('post_facebook.html', pages=[])
    
    page_id = request.form.get('page_id', '').strip()
    message = request.form.get('message', '').strip()
    link = request.form.get('link', '').strip()
    
    if not page_id or not message:
        flash('Page and message are required', 'error')
        return redirect(url_for('post_facebook'))
    
    try:
        data = {"message": message}
        if link:
            data["link"] = link
        
        result = meta_api.make_api_request(f"{page_id}/feed", "POST", data)
        flash(f"Posted to Facebook! ID: {result.get('id', 'Unknown')}", 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error posting: {str(e)}", 'error')
        return redirect(url_for('post_facebook'))

@app.route('/post-instagram', methods=['GET', 'POST'])
def post_instagram():
    """Post to Instagram"""
    if request.method == 'GET':
        return render_template('post_instagram.html')
    
    instagram_account_id = request.form.get('instagram_account_id', '').strip()
    image_url = request.form.get('image_url', '').strip()
    caption = request.form.get('caption', '').strip()
    
    if not instagram_account_id or not image_url:
        flash('Instagram account ID and image URL required', 'error')
        return redirect(url_for('post_instagram'))
    
    try:
        container_data = {
            "image_url": image_url,
            "caption": caption
        }
        
        container_result = meta_api.make_api_request(
            f"{instagram_account_id}/media", "POST", container_data
        )
        
        creation_id = container_result.get("id")
        
        publish_data = {"creation_id": creation_id}
        publish_result = meta_api.make_api_request(
            f"{instagram_account_id}/media_publish", "POST", publish_data
        )
        
        flash(f"Posted to Instagram! ID: {publish_result.get('id', 'Unknown')}", 'success')
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
    """Get Facebook insights"""
    try:
        page_id = request.form.get('page_id', '').strip()
        metric = request.form.get('metric', 'page_views')
        period = request.form.get('period', 'day')
        
        if not page_id:
            return jsonify({'error': 'Page ID required'}), 400
        
        params = {"metric": metric, "period": period}
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
    try:
        instagram_account_id = request.form.get('instagram_account_id', '').strip()
        metric = request.form.get('metric', 'impressions')
        
        if not instagram_account_id:
            return jsonify({'error': 'Instagram account ID required'}), 400
        
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

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=False)