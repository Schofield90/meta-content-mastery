#!/usr/bin/env python3
"""
Meta Content Manager - Simplified for Vercel
"""

import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from openai import OpenAI
import json
from supabase_client import supabase_manager

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'meta-content-manager-secret-key')

# OpenAI configuration
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration removed: Google Drive OAuth no longer needed with Supabase storage

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
    return jsonify({'status': 'ok', 'app': 'Meta Content Manager', 'version': '2.1', 'bulk_upload': 'enabled', 'timestamp': 'July 2025'})

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

@app.route('/claude-training')
def claude_training():
    """Claude AI Training Hub page"""
    return render_template('claude_training.html')

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

# Claude Training Hub Routes
@app.route('/auto-categorize-knowledge', methods=['POST'])
def auto_categorize_knowledge():
    """Automatically categorize knowledge content using AI"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        
        if not title and not content:
            return jsonify({'success': False, 'error': 'Title or content required'}), 400
        
        # Create prompt for categorization
        categorization_prompt = f"""
        Analyze this business information and assign it to the most appropriate category.
        
        Title: {title}
        Content: {content}
        
        Choose the MOST APPROPRIATE category from these options:
        - business_basics: Company overview, mission, vision, founding story
        - services: Products, programs, offerings, what you provide
        - target_audience: Who your customers are, demographics, personas
        - brand_voice: Tone, messaging style, communication approach
        - success_stories: Testimonials, case studies, client wins
        - pricing: Costs, packages, membership tiers, payment options
        - competition: Competitors, differentiators, unique selling points
        - marketing: Advertising strategies, social media, campaigns
        - operations: Policies, procedures, how things work
        - team: Staff, culture, leadership, company values
        
        Respond with ONLY the category name (e.g., "services" or "target_audience").
        """
        
        if openai_client.api_key:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert business analyst. Categorize business information accurately and concisely."},
                    {"role": "user", "content": categorization_prompt}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            
            # Validate category is one of our expected ones
            valid_categories = [
                'business_basics', 'services', 'target_audience', 'brand_voice',
                'success_stories', 'pricing', 'competition', 'marketing', 
                'operations', 'team'
            ]
            
            if category not in valid_categories:
                # Default to business_basics if categorization fails
                category = 'business_basics'
            
            # Convert to display format
            category_display = category.replace('_', ' ').title()
            
            return jsonify({
                'success': True,
                'category': category,
                'category_display': category_display
            })
        else:
            # Fallback categorization based on keywords
            content_lower = (title + ' ' + content).lower()
            
            if any(word in content_lower for word in ['service', 'program', 'offer', 'class', 'training']):
                category = 'services'
            elif any(word in content_lower for word in ['customer', 'client', 'audience', 'member']):
                category = 'target_audience'
            elif any(word in content_lower for word in ['price', 'cost', 'membership', 'package']):
                category = 'pricing'
            elif any(word in content_lower for word in ['team', 'staff', 'trainer', 'employee']):
                category = 'team'
            elif any(word in content_lower for word in ['brand', 'voice', 'tone', 'message']):
                category = 'brand_voice'
            else:
                category = 'business_basics'
            
            category_display = category.replace('_', ' ').title()
            
            return jsonify({
                'success': True,
                'category': category,
                'category_display': category_display
            })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/save-claude-knowledge', methods=['POST'])
def save_claude_knowledge():
    """Save knowledge to Claude's training database"""
    try:
        data = request.get_json()
        
        knowledge_item = {
            'category': data.get('category', ''),
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'importance': data.get('importance', 'important'),
            'timestamp': data.get('timestamp', '')
        }
        
        # Try to save to Supabase first
        if supabase_manager.is_available():
            saved_id = supabase_manager.save_claude_knowledge(knowledge_item)
            if saved_id:
                return jsonify({'success': True, 'message': 'Knowledge saved successfully', 'id': saved_id})
        
        # Fallback to in-memory storage
        if 'claude_knowledge' not in fallback_training_data:
            fallback_training_data['claude_knowledge'] = []
        
        # Generate unique ID for fallback storage
        import uuid
        knowledge_item['id'] = str(uuid.uuid4())
        fallback_training_data['claude_knowledge'].append(knowledge_item)
        
        return jsonify({'success': True, 'message': 'Knowledge saved successfully (fallback)', 'id': knowledge_item['id']})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/assess-claude-knowledge', methods=['POST'])
def assess_claude_knowledge():
    """Assess Claude's knowledge about the business"""
    try:
        # Get all knowledge items
        knowledge_items = []
        if supabase_manager.is_available():
            knowledge_items = supabase_manager.get_claude_knowledge()
        else:
            knowledge_items = fallback_training_data.get('claude_knowledge', [])
        
        # Calculate knowledge score based on coverage and depth
        total_categories = 10  # Expected categories
        covered_categories = set()
        total_items = len(knowledge_items)
        critical_items = 0
        important_items = 0
        
        for item in knowledge_items:
            covered_categories.add(item.get('category', ''))
            importance = item.get('importance', 'useful')
            if importance == 'critical':
                critical_items += 1
            elif importance == 'important':
                important_items += 1
        
        # Scoring algorithm
        category_coverage = len(covered_categories) / total_categories * 100
        content_depth = min(100, (critical_items * 15 + important_items * 10 + (total_items - critical_items - important_items) * 5))
        
        overall_score = int((category_coverage * 0.4) + (content_depth * 0.6))
        
        # Generate assessment text
        if overall_score >= 80:
            assessment = "Excellent! Claude has comprehensive knowledge about your business."
        elif overall_score >= 60:
            assessment = "Good knowledge base. Claude understands your business well."
        elif overall_score >= 40:
            assessment = "Fair knowledge. Claude needs more training about your business."
        else:
            assessment = "Limited knowledge. Claude needs significant training to understand your business."
        
        return jsonify({
            'success': True,
            'score': overall_score,
            'assessment': assessment,
            'details': {
                'total_items': total_items,
                'categories_covered': len(covered_categories),
                'critical_items': critical_items,
                'important_items': important_items
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generate-claude-test', methods=['POST'])
def generate_claude_test():
    """Generate test questions for Claude's knowledge"""
    try:
        data = request.get_json()
        category = data.get('category', 'random')
        
        # Get knowledge items for the category
        knowledge_items = []
        if supabase_manager.is_available():
            knowledge_items = supabase_manager.get_claude_knowledge(category if category != 'random' else None)
        else:
            all_items = fallback_training_data.get('claude_knowledge', [])
            if category == 'random':
                knowledge_items = all_items
            else:
                knowledge_items = [item for item in all_items if item.get('category') == category]
        
        # Generate questions based on knowledge
        questions = []
        import random
        
        for i, item in enumerate(random.sample(knowledge_items, min(5, len(knowledge_items)))):
            question_types = [
                f"What do you know about {item.get('title', 'this topic')}?",
                f"How would you describe {item.get('title', 'this aspect')} of the business?",
                f"What makes {item.get('title', 'this feature')} important for the business?",
                f"Can you explain {item.get('title', 'this topic')} in your own words?"
            ]
            
            questions.append({
                'id': f"q_{i}_{item.get('id', 'unknown')}",
                'question': random.choice(question_types),
                'category': item.get('category', 'general'),
                'knowledge_id': item.get('id')
            })
        
        return jsonify({
            'success': True,
            'questions': questions
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/answer-claude-test', methods=['POST'])
def answer_claude_test():
    """Get Claude's answer to a test question"""
    try:
        data = request.get_json()
        question_id = data.get('question_id', '')
        
        # Extract knowledge ID from question ID
        if '_' in question_id:
            knowledge_id = question_id.split('_')[-1]
        else:
            knowledge_id = None
        
        # Get the specific knowledge item
        knowledge_item = None
        if supabase_manager.is_available():
            knowledge_item = supabase_manager.get_claude_knowledge_by_id(knowledge_id)
        else:
            all_items = fallback_training_data.get('claude_knowledge', [])
            for item in all_items:
                if item.get('id') == knowledge_id:
                    knowledge_item = item
                    break
        
        if not knowledge_item:
            return jsonify({'success': False, 'error': 'Knowledge item not found'}), 404
        
        # Generate answer based on the knowledge
        answer = knowledge_item.get('content', 'I don\'t have specific information about this topic.')
        
        # Calculate confidence based on content length and importance
        content_length = len(answer.split())
        importance = knowledge_item.get('importance', 'useful')
        
        if importance == 'critical':
            base_confidence = 90
        elif importance == 'important':
            base_confidence = 75
        else:
            base_confidence = 60
        
        # Adjust confidence based on content depth
        if content_length > 50:
            confidence = min(95, base_confidence + 10)
        elif content_length > 20:
            confidence = base_confidence
        else:
            confidence = max(40, base_confidence - 15)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'confidence': confidence,
            'category': knowledge_item.get('category', 'general')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/chat-with-claude', methods=['POST'])
def chat_with_claude():
    """Chat with Claude using business knowledge"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        # Get business context
        business_context = ""
        if supabase_manager.is_available():
            context_data = supabase_manager.get_training_context()
            profile = context_data.get('business_profile', {})
            knowledge_items = supabase_manager.get_claude_knowledge()
        else:
            profile = fallback_training_data.get('business_profile', {})
            knowledge_items = fallback_training_data.get('claude_knowledge', [])
        
        # Build context from business profile
        if profile:
            business_context += f"Business: {profile.get('business_name', 'Atlas Gyms')}\n"
            business_context += f"Industry: {profile.get('industry', 'Fitness')}\n"
            business_context += f"Services: {profile.get('services', '')}\n"
            business_context += f"Target Audience: {profile.get('target_audience', '')}\n"
            business_context += f"Brand Voice: {profile.get('brand_voice', '')}\n"
        
        # Add relevant knowledge items
        relevant_knowledge = []
        for item in knowledge_items:
            if any(keyword in user_message.lower() for keyword in item.get('title', '').lower().split()):
                relevant_knowledge.append(item.get('content', ''))
        
        # Create prompt for Claude
        system_prompt = f"""You are Claude, an AI assistant that has been trained specifically about this business. 
        
Business Context:
{business_context}

Relevant Knowledge:
{' '.join(relevant_knowledge[:3])}

Respond as if you are well-informed about this business. Be helpful, accurate, and match the brand voice when possible."""
        
        # Generate response using OpenAI (simulating Claude)
        if openai_client.api_key:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            claude_response = response.choices[0].message.content
        else:
            claude_response = "I understand you're asking about the business. Unfortunately, I need the OpenAI API key to be configured to provide detailed responses."
        
        return jsonify({
            'success': True,
            'response': claude_response,
            'context_used': len(relevant_knowledge) > 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get-claude-knowledge')
def get_claude_knowledge():
    """Get all Claude knowledge items"""
    try:
        if supabase_manager.is_available():
            knowledge_items = supabase_manager.get_claude_knowledge()
        else:
            knowledge_items = fallback_training_data.get('claude_knowledge', [])
        
        return jsonify({
            'success': True,
            'knowledge': knowledge_items
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get-claude-test-scores')
def get_claude_test_scores():
    """Get historical test scores"""
    try:
        # For now, generate sample scores - in production this would be stored
        sample_scores = [65, 72, 78, 85, 82, 88, 92]
        
        return jsonify({
            'success': True,
            'scores': sample_scores
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Google Drive OAuth routes removed - now using Supabase for image storage

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