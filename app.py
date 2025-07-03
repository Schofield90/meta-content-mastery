#!/usr/bin/env python3
"""
Meta Content Manager - Simplified for Vercel
"""

import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from openai import OpenAI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
from supabase_client import supabase_manager

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'meta-content-manager-secret-key')

# OpenAI configuration
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Google Drive configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"

# OAuth 2.0 scopes for Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def create_google_flow():
    """Create Google OAuth flow"""
    # Use the current deployment URL for redirect
    base_url = os.getenv('VERCEL_URL', 'https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app')
    redirect_uri = f"{base_url}/oauth/google/callback"
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = redirect_uri
    return flow

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

@app.route('/data-deletion', methods=['GET', 'POST'])
def data_deletion():
    """Data deletion endpoint for Meta app compliance"""
    if request.method == 'GET':
        return """
        <html>
        <head><title>Data Deletion - Meta Content Manager</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>Data Deletion Request</h1>
            <p>This Meta Content Manager app does not store any user data persistently.</p>
            <p>All user interactions are processed in real-time and no personal data is retained.</p>
            <p>If you have any concerns about data privacy, please contact: samschofield90@hotmail.co.uk</p>
            <h2>What data we don't store:</h2>
            <ul>
                <li>No user profiles or account information</li>
                <li>No post content or media files</li>
                <li>No analytics data beyond what Meta provides via API</li>
                <li>No personal information or contact details</li>
            </ul>
            <p>This app only facilitates real-time communication with Meta's API and does not maintain any database of user information.</p>
        </body>
        </html>
        """
    
    # Handle POST request (Meta's callback)
    return jsonify({
        "url": request.form.get("confirmation_code", ""),
        "confirmation_code": request.form.get("confirmation_code", "")
    })

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

@app.route('/smart-post')
def smart_post():
    """Smart post creator page"""
    return render_template('smart_post.html')

@app.route('/ai-training')
def ai_training():
    """AI training center page"""
    return render_template('ai_training.html')

@app.route('/bulk-upload')
def bulk_upload():
    """Bulk image upload page"""
    return render_template('bulk_upload.html')

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

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate AI image for social media posts"""
    try:
        prompt = request.form.get('prompt', '').strip()
        style = request.form.get('style', 'realistic')
        
        if not prompt:
            return jsonify({'error': 'Image prompt is required'}), 400
        
        if not openai_client.api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 400
        
        # Enhanced prompt for social media
        enhanced_prompt = f"{prompt}, {style} style, high quality, suitable for social media, professional"
        
        # Generate image using DALL-E
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        
        image_url = response.data[0].url
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'prompt': enhanced_prompt
        })
        
    except Exception as e:
        return jsonify({'error': f'Image generation failed: {str(e)}'}), 500

@app.route('/create-smart-post', methods=['POST'])
def create_smart_post():
    """Create intelligent social media post with AI"""
    try:
        # Extract form data
        topic = request.form.get('topic', '').strip()
        platform = request.form.get('platform', 'both')
        post_type = request.form.get('post_type', 'general')
        business_name = request.form.get('business_name', 'your business')
        target_audience = request.form.get('target_audience', 'fitness enthusiasts')
        tone = request.form.get('tone', 'motivational')
        call_to_action = request.form.get('call_to_action', '')
        image_style = request.form.get('image_style', 'realistic')
        generate_image = request.form.get('generate_image') == 'on'
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        if not openai_client.api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 400
        
        # Get training context for personalization from Supabase or fallback
        if supabase_manager.is_available():
            training_context_data = supabase_manager.get_training_context()
            profile = training_context_data.get('business_profile', {})
            content_examples = training_context_data.get('content_examples', [])[-3:]  # Last 3 posts
        else:
            profile = fallback_training_data.get('business_profile', {})
            content_examples = fallback_training_data.get('content_library', [])[-3:]  # Last 3 posts
        
        # Build enhanced prompt with training data
        training_context = ""
        if profile:
            training_context += f"\nBusiness Context:\n"
            training_context += f"- Business: {profile.get('business_name', business_name)}\n"
            training_context += f"- Industry: {profile.get('industry', 'fitness')}\n"
            training_context += f"- Target Audience: {profile.get('target_audience', target_audience)}\n"
            training_context += f"- Brand Voice: {profile.get('brand_voice', tone)}\n"
            training_context += f"- Services: {profile.get('services', '')}\n"
            training_context += f"- USP: {profile.get('usp', '')}\n"
        
        if content_examples:
            training_context += f"\nSuccessful Content Examples:\n"
            for example in content_examples:
                training_context += f"- {example.get('post_content', '')[:100]}...\n"
        
        # Generate content with OpenAI
        content_prompt = f"""
        Create a {tone} social media post for {platform} about: {topic}
        
        {training_context}
        
        Context:
        - Post type: {post_type}
        - Call to action: {call_to_action}
        
        Requirements:
        - Write engaging copy that matches the brand voice and tone
        - Include relevant hashtags for {platform}
        - Keep it appropriate for the target audience
        - Make it actionable and engaging
        - Use similar style and voice as the successful examples if provided
        
        Format your response as:
        COPY:
        [The main post text here]
        
        HASHTAGS:
        [Relevant hashtags here]
        """
        
        # Generate copy with GPT
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert social media content creator specializing in fitness and wellness businesses."},
                {"role": "user", "content": content_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        generated_content = response.choices[0].message.content
        
        # Parse the response
        copy_start = generated_content.find("COPY:") + 5
        hashtags_start = generated_content.find("HASHTAGS:")
        
        if hashtags_start == -1:
            copy = generated_content[copy_start:].strip()
            hashtags = ""
        else:
            copy = generated_content[copy_start:hashtags_start].strip()
            hashtags = generated_content[hashtags_start + 9:].strip()
        
        result = {
            'success': True,
            'copy': copy,
            'hashtags': hashtags,
            'platform': platform,
            'post_type': post_type
        }
        
        # Generate image if requested
        if generate_image:
            try:
                # Create image prompt based on the content
                image_prompt = f"{topic}, {image_style} style, {business_name}, fitness, gym, {post_type}, high quality, social media"
                
                image_response = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url"
                )
                
                result['image_url'] = image_response.data[0].url
                result['image_prompt'] = image_prompt
                
            except Exception as img_error:
                print(f"Image generation failed: {img_error}")
                # Continue without image
                pass
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Smart post creation failed: {str(e)}'}), 500

# AI Training System - Using Supabase for persistent storage
# Fallback in-memory storage for when Supabase is not available
fallback_training_data = {
    'business_profile': {},
    'content_library': [],
    'images': [],
    'documents': []
}

@app.route('/save-business-profile', methods=['POST'])
def save_business_profile():
    """Save business profile for AI training"""
    try:
        # Extract form data
        profile = {
            'business_name': request.form.get('business_name', ''),
            'industry': request.form.get('industry', ''),
            'location': request.form.get('location', ''),
            'target_audience': request.form.get('target_audience', ''),
            'brand_voice': request.form.get('brand_voice', ''),
            'services': request.form.get('services', ''),
            'usp': request.form.get('usp', ''),
            'goals': request.form.getlist('goals[]')
        }
        
        # Try to save to Supabase first
        if supabase_manager.is_available():
            business_id = supabase_manager.save_business_profile(profile)
            if business_id:
                return jsonify({'success': True, 'message': 'Business profile saved successfully', 'business_id': business_id})
        
        # Fallback to in-memory storage
        fallback_training_data['business_profile'] = profile
        return jsonify({'success': True, 'message': 'Business profile saved successfully (fallback storage)'})
        
    except Exception as e:
        return jsonify({'error': f'Failed to save business profile: {str(e)}'}), 500

@app.route('/save-content', methods=['POST'])
def save_content():
    """Save content to training library"""
    try:
        content = {
            'post_content': request.form.get('post_content', ''),
            'platform': request.form.get('platform', ''),
            'performance': request.form.get('performance', ''),
        }
        
        # Try to save to Supabase first
        if supabase_manager.is_available():
            content_id = supabase_manager.save_content(content)
            if content_id:
                return jsonify({'success': True, 'message': 'Content added to library', 'content_id': content_id})
        
        # Fallback to in-memory storage
        content['id'] = len(fallback_training_data['content_library']) + 1
        content['timestamp'] = request.form.get('timestamp', '')
        fallback_training_data['content_library'].append(content)
        
        return jsonify({'success': True, 'message': 'Content added to library (fallback storage)'})
        
    except Exception as e:
        return jsonify({'error': f'Failed to save content: {str(e)}'}), 500

@app.route('/upload-images', methods=['POST'])
def upload_images():
    """Handle image uploads for AI training with Supabase storage"""
    try:
        if 'images' not in request.files:
            return jsonify({'error': 'No images provided'}), 400
        
        files = request.files.getlist('images')
        category = request.form.get('category', 'general')
        
        uploaded_images = []
        for file in files:
            if file and file.filename:
                file_data = file.read()
                
                # Try to upload to Supabase storage
                if supabase_manager.is_available():
                    # Upload to Supabase storage
                    public_url = supabase_manager.upload_image(
                        file_data=file_data,
                        filename=f"{category}_{file.filename}",
                        content_type=file.content_type or 'image/jpeg'
                    )
                    
                    if public_url:
                        # Save metadata to database
                        image_data = {
                            'filename': file.filename,
                            'storage_path': public_url,
                            'category': category,
                            'source': 'upload',
                            'file_size': len(file_data)
                        }
                        
                        image_id = supabase_manager.save_image_metadata(image_data)
                        if image_id:
                            image_data['id'] = image_id
                            image_data['url'] = public_url
                            uploaded_images.append(image_data)
                            continue
                
                # Fallback to in-memory storage
                image_data = {
                    'filename': file.filename,
                    'category': category,
                    'size': len(file_data),
                    'source': 'upload_fallback',
                    'id': len(fallback_training_data['images']) + 1
                }
                fallback_training_data['images'].append(image_data)
                uploaded_images.append(image_data)
        
        storage_type = 'Supabase' if supabase_manager.is_available() else 'fallback'
        return jsonify({
            'success': True, 
            'message': f'Uploaded {len(uploaded_images)} images to {storage_type} storage',
            'images': uploaded_images
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to upload images: {str(e)}'}), 500

@app.route('/get-saved-content')
def get_saved_content():
    """Get saved content from training library"""
    if supabase_manager.is_available():
        content = supabase_manager.get_content_library()
        return jsonify({
            'success': True,
            'content': content,
            'source': 'supabase'
        })
    
    # Fallback to in-memory storage
    return jsonify({
        'success': True,
        'content': fallback_training_data['content_library'],
        'source': 'fallback'
    })

@app.route('/get-uploaded-images')
def get_uploaded_images():
    """Get uploaded images from training library"""
    if supabase_manager.is_available():
        images = supabase_manager.get_training_images()
        return jsonify({
            'success': True,
            'images': images,
            'source': 'supabase'
        })
    
    # Fallback to in-memory storage
    return jsonify({
        'success': True,
        'images': fallback_training_data['images'],
        'source': 'fallback'
    })

@app.route('/get-training-context')
def get_training_context():
    """Get all training context for AI personalization"""
    if supabase_manager.is_available():
        context = supabase_manager.get_training_context()
        context['source'] = 'supabase'
        return jsonify({
            'success': True,
            'context': context
        })
    
    # Fallback to in-memory storage
    context = {
        'business_profile': fallback_training_data['business_profile'],
        'content_examples': fallback_training_data['content_library'][-5:],  # Last 5 posts
        'image_categories': list(set([img.get('category', 'general') for img in fallback_training_data['images']])),
        'total_content': len(fallback_training_data['content_library']),
        'total_images': len(fallback_training_data['images']),
        'source': 'fallback'
    }
    
    return jsonify({
        'success': True,
        'context': context
    })

# Google Drive OAuth Routes
@app.route('/oauth/google/login')
def google_login():
    """Initiate Google OAuth flow"""
    try:
        flow = create_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        session['state'] = state
        return redirect(authorization_url)
    except Exception as e:
        return jsonify({'error': f'OAuth login failed: {str(e)}'}), 500

@app.route('/oauth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        flow = create_google_flow()
        flow.fetch_token(authorization_response=request.url)
        
        # Store credentials in session
        credentials = flow.credentials
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        return redirect(url_for('ai_training') + '?google_connected=true')
    except Exception as e:
        return jsonify({'error': f'OAuth callback failed: {str(e)}'}), 500

@app.route('/google-drive/folders')
def get_google_drive_folders():
    """Get folders from Google Drive"""
    try:
        if 'google_credentials' not in session:
            return jsonify({'error': 'Not authenticated with Google'}), 401
        
        # Create credentials from session
        creds = Credentials(**session['google_credentials'])
        service = build('drive', 'v3', credentials=creds)
        
        # Get folders
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            pageSize=50,
            fields="nextPageToken, files(id, name, parents)"
        ).execute()
        
        folders = results.get('files', [])
        
        return jsonify({
            'success': True,
            'folders': folders
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get folders: {str(e)}'}), 500

@app.route('/google-drive/images')
def get_google_drive_images():
    """Get images from Google Drive"""
    try:
        if 'google_credentials' not in session:
            return jsonify({'error': 'Not authenticated with Google'}), 401
        
        folder_id = request.args.get('folder_id', 'root')
        
        # Create credentials from session
        creds = Credentials(**session['google_credentials'])
        service = build('drive', 'v3', credentials=creds)
        
        # Get images
        query = f"'{folder_id}' in parents and (mimeType contains 'image/')"
        results = service.files().list(
            q=query,
            pageSize=50,
            fields="nextPageToken, files(id, name, mimeType, thumbnailLink, webViewLink, size)"
        ).execute()
        
        images = results.get('files', [])
        
        return jsonify({
            'success': True,
            'images': images
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get images: {str(e)}'}), 500

@app.route('/google-drive/image/<file_id>')
def get_google_drive_image(file_id):
    """Get specific image from Google Drive"""
    try:
        if 'google_credentials' not in session:
            return jsonify({'error': 'Not authenticated with Google'}), 401
        
        # Create credentials from session
        creds = Credentials(**session['google_credentials'])
        service = build('drive', 'v3', credentials=creds)
        
        # Get file metadata
        file_metadata = service.files().get(fileId=file_id).execute()
        
        # Get download link
        download_link = f"https://drive.google.com/uc?id={file_id}&export=download"
        
        return jsonify({
            'success': True,
            'file': file_metadata,
            'download_link': download_link
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get image: {str(e)}'}), 500

@app.route('/save-drive-image', methods=['POST'])
def save_drive_image():
    """Save Google Drive image to training library"""
    try:
        data = request.get_json()
        
        image_data = {
            'filename': data.get('filename', ''),
            'source': 'google_drive',
            'file_id': data.get('file_id', ''),
            'download_link': data.get('download_link', ''),
            'category': data.get('category', 'google_drive'),
            'timestamp': data.get('timestamp', ''),
            'id': len(training_data['images']) + 1
        }
        
        training_data['images'].append(image_data)
        
        return jsonify({
            'success': True,
            'message': 'Google Drive image added to training library'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to save Drive image: {str(e)}'}), 500

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
        # First get the page access token
        result = meta_api.make_api_request("me/accounts", "GET")
        pages_data = result.get("data", [])
        
        page_access_token = None
        for page in pages_data:
            if page.get("id") == page_id:
                page_access_token = page.get("access_token")
                break
        
        if not page_access_token:
            flash('Could not find access token for selected page', 'error')
            return redirect(url_for('post_facebook'))
        
        # Use page access token for posting
        url = f"{meta_api.base_url}/{page_id}/feed"
        params = {'access_token': page_access_token}
        data = {"message": message}
        if link:
            data["link"] = link
        
        response = requests.post(url, params=params, data=data, timeout=25)
        result = response.json()
        
        if response.status_code >= 400:
            raise Exception(f"Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}")
        
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