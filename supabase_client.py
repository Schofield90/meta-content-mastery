"""
Supabase client configuration for Meta Content Manager
"""
import os
from supabase import create_client, Client
from typing import Optional, Dict, List, Any
import logging

class SupabaseManager:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            logging.warning("Supabase credentials not found. Using fallback storage.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.url, self.key)
                logging.info("Supabase client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Supabase client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if Supabase is available and configured"""
        return self.client is not None
    
    # Business Profile Methods
    def get_business_profile(self, business_id: Optional[str] = None) -> Dict[str, Any]:
        """Get business profile by ID or get the first one"""
        if not self.is_available():
            return {}
        
        try:
            if business_id:
                response = self.client.table('business_profiles').select('*').eq('id', business_id).execute()
            else:
                # Get the first business profile (for single-business use)
                response = self.client.table('business_profiles').select('*').limit(1).execute()
            
            if response.data:
                return response.data[0]
            return {}
        except Exception as e:
            logging.error(f"Error getting business profile: {e}")
            return {}
    
    def save_business_profile(self, profile_data: Dict[str, Any]) -> Optional[str]:
        """Save or update business profile"""
        if not self.is_available():
            return None
        
        try:
            # Check if profile already exists
            existing = self.get_business_profile()
            
            if existing:
                # Update existing profile
                response = self.client.table('business_profiles').update(profile_data).eq('id', existing['id']).execute()
                return existing['id']
            else:
                # Create new profile
                response = self.client.table('business_profiles').insert(profile_data).execute()
                if response.data:
                    return response.data[0]['id']
            return None
        except Exception as e:
            logging.error(f"Error saving business profile: {e}")
            return None
    
    # Content Library Methods
    def get_content_library(self, business_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get content library items"""
        if not self.is_available():
            return []
        
        try:
            query = self.client.table('content_library').select('*').order('created_at', desc=True).limit(limit)
            
            if business_id:
                query = query.eq('business_id', business_id)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            logging.error(f"Error getting content library: {e}")
            return []
    
    def save_content(self, content_data: Dict[str, Any], business_id: Optional[str] = None) -> Optional[str]:
        """Save content to library"""
        if not self.is_available():
            return None
        
        try:
            # Get business ID if not provided
            if not business_id:
                profile = self.get_business_profile()
                business_id = profile.get('id') if profile else None
            
            if business_id:
                content_data['business_id'] = business_id
            
            response = self.client.table('content_library').insert(content_data).execute()
            if response.data:
                return response.data[0]['id']
            return None
        except Exception as e:
            logging.error(f"Error saving content: {e}")
            return None
    
    # Training Images Methods
    def get_training_images(self, business_id: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get training images"""
        if not self.is_available():
            return []
        
        try:
            query = self.client.table('training_images').select('*').order('created_at', desc=True)
            
            if business_id:
                query = query.eq('business_id', business_id)
            
            if category:
                query = query.eq('category', category)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            logging.error(f"Error getting training images: {e}")
            return []
    
    def save_image_metadata(self, image_data: Dict[str, Any], business_id: Optional[str] = None) -> Optional[str]:
        """Save image metadata to database"""
        if not self.is_available():
            return None
        
        try:
            # Get business ID if not provided
            if not business_id:
                profile = self.get_business_profile()
                business_id = profile.get('id') if profile else None
            
            if business_id:
                image_data['business_id'] = business_id
            
            response = self.client.table('training_images').insert(image_data).execute()
            if response.data:
                return response.data[0]['id']
            return None
        except Exception as e:
            logging.error(f"Error saving image metadata: {e}")
            return None
    
    def upload_image(self, file_data: bytes, filename: str, content_type: str = 'image/jpeg') -> Optional[str]:
        """Upload image to Supabase storage"""
        if not self.is_available():
            return None
        
        try:
            # Upload to storage bucket
            response = self.client.storage.from_('training-images').upload(
                path=filename,
                file=file_data,
                file_options={'content-type': content_type}
            )
            
            if response:
                # Get public URL
                public_url = self.client.storage.from_('training-images').get_public_url(filename)
                return public_url
            
            return None
        except Exception as e:
            logging.error(f"Error uploading image: {e}")
            return None
    
    def get_training_context(self, business_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive training context for AI"""
        try:
            profile = self.get_business_profile(business_id)
            content_examples = self.get_content_library(business_id, limit=5)
            images = self.get_training_images(business_id)
            
            # Get image categories
            image_categories = list(set([img.get('category', 'general') for img in images]))
            
            return {
                'business_profile': profile,
                'content_examples': content_examples,
                'image_categories': image_categories,
                'total_content': len(content_examples),
                'total_images': len(images)
            }
        except Exception as e:
            logging.error(f"Error getting training context: {e}")
            return {
                'business_profile': {},
                'content_examples': [],
                'image_categories': [],
                'total_content': 0,
                'total_images': 0
            }
    
    # Claude Knowledge Management Methods
    def save_claude_knowledge(self, knowledge_data: Dict[str, Any], business_id: Optional[str] = None) -> Optional[str]:
        """Save Claude knowledge item"""
        if not self.is_available():
            return None
        
        try:
            # Get business ID if not provided
            if not business_id:
                profile = self.get_business_profile()
                business_id = profile.get('id') if profile else None
            
            if business_id:
                knowledge_data['business_id'] = business_id
            
            response = self.client.table('claude_knowledge').insert(knowledge_data).execute()
            if response.data:
                return response.data[0]['id']
            return None
        except Exception as e:
            logging.error(f"Error saving Claude knowledge: {e}")
            return None
    
    def get_claude_knowledge(self, category: Optional[str] = None, business_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Claude knowledge items"""
        if not self.is_available():
            return []
        
        try:
            query = self.client.table('claude_knowledge').select('*').order('created_at', desc=True)
            
            if business_id:
                query = query.eq('business_id', business_id)
            
            if category:
                query = query.eq('category', category)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            logging.error(f"Error getting Claude knowledge: {e}")
            return []
    
    def get_claude_knowledge_by_id(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """Get specific Claude knowledge item by ID"""
        if not self.is_available():
            return None
        
        try:
            response = self.client.table('claude_knowledge').select('*').eq('id', knowledge_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error getting Claude knowledge by ID: {e}")
            return None


# Global instance
supabase_manager = SupabaseManager()