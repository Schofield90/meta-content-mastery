# Meta Content Manager - Claude MCP Integration

## Project Overview
Meta Content Manager is a Flask-based web application that integrates with Meta's Graph API, OpenAI's API, and Google Drive to provide social media content creation and management capabilities. The app is deployed on Vercel and features AI-powered content generation, social media posting, and training data management.

## Current Status & Next Steps

### ✅ Completed Features
- Flask web application with multiple routes for content creation
- Meta API integration for Facebook and Instagram posting
- OpenAI integration for AI content generation and image creation
- Supabase integration for persistent image storage
- AI training system with business profile and content library
- Vercel deployment configuration

### ✅ Issue Resolved: Google Drive Integration Removed
**Status**: COMPLETED - Replaced Google Drive with Supabase storage

**Solution**: 
- Removed all Google OAuth complexity
- Using Supabase for persistent image storage
- No more OAuth consent screen issues
- Direct image uploads with public URLs

### 🛠️ Immediate Next Steps

1. **✅ COMPLETED: Supabase Integration** 
   - Added persistent database and image storage
   - Replaced in-memory storage with Supabase
   - Includes fallback for when Supabase is unavailable

2. **Set up Supabase** (NEW PRIORITY)
   - Create Supabase project and run SQL schema
   - Add SUPABASE_URL and SUPABASE_ANON_KEY to Vercel
   - Test image uploads and data persistence

3. **✅ COMPLETED: Removed Google Drive Integration**
   - Eliminated OAuth complexity entirely
   - All image storage now handled by Supabase

4. **Test Application**
   - Deploy updated version with Supabase
   - Test AI training features with persistent storage
   - Verify image uploads work correctly

## Environment Variables

### Vercel Environment Variables (Required)
```
OPENAI_API_KEY=[Your OpenAI API Key]
META_ACCESS_TOKEN=[Your Meta Access Token]
META_APP_ID=1667446050583846
SECRET_KEY=[Your Flask Secret Key]
VERCEL_URL=https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app
SUPABASE_URL=[Your Supabase Project URL]
SUPABASE_ANON_KEY=[Your Supabase Anon Key]
```

### Supabase Setup (NEW)
1. **Create Supabase project** at [supabase.com](https://supabase.com)
2. **Run SQL schema** from `supabase_setup.sql` in your Supabase SQL Editor
3. **Get credentials** from Project Settings > API:
   - Project URL → `SUPABASE_URL`
   - Anon public key → `SUPABASE_ANON_KEY`
4. **Add to Vercel** environment variables

## Application Structure

### Main Features
- **Content Creation**: AI-powered social media content generation
- **Smart Posts**: Intelligent post creation with business context
- **AI Training**: Business profile and content library management
- **Supabase Storage**: Image upload and management
- **Social Media Posting**: Direct posting to Facebook and Instagram
- **Analytics**: Performance insights and metrics

### Key Files
- `app.py`: Main Flask application with all routes
- `templates/`: HTML templates for all pages
- `static/`: CSS and JavaScript assets
- `vercel.json`: Vercel deployment configuration
- `requirements.txt`: Python dependencies

### API Integrations
1. **Meta Graph API**: Facebook and Instagram posting, analytics
2. **OpenAI API**: Content generation and image creation (DALL-E)
3. **Supabase API**: Database and image storage management

## Deployment

### Current Deployment URLs
- Production: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app`
- Alternative: `https://meta-content-mastery-766ozocne-schofield90s-projects.vercel.app`

### Deployment Process
1. Push changes to GitHub repository
2. Vercel automatically deploys from connected GitHub repo
3. Environment variables are configured in Vercel dashboard

## Security Notes
- All sensitive API keys stored as environment variables
- OAuth credentials properly externalized
- No hardcoded secrets in codebase
- HTTPS-only redirect URIs

## Troubleshooting

### Common Issues
1. **OAuth "Access blocked"**: Complete consent screen configuration
2. **Environment variables**: Ensure all required vars are set in Vercel
3. **API rate limits**: Check Meta and OpenAI API quotas
4. **CORS issues**: Verify domain configurations in all services

### Debug Steps
1. Check Vercel deployment logs
2. Verify environment variables are set
3. Test API connections individually
4. Check OAuth consent screen status in Google Cloud Console

## Development Workflow

### Local Development
```bash
# Set environment variables
export GOOGLE_CLIENT_ID="your_client_id"
export GOOGLE_CLIENT_SECRET="your_client_secret"
# ... other env vars

# Run Flask app
python app.py
```

### Deployment
```bash
# Push to GitHub
git add .
git commit -m "Update message"
git push origin main

# Vercel auto-deploys from GitHub
```

## Legacy MCP Server Features

### Tools Available
- **post_to_facebook_page**: Post content to Facebook pages
- **post_to_instagram**: Post content to Instagram Business accounts
- **get_facebook_page_insights**: Get analytics/insights for Facebook pages
- **get_instagram_insights**: Get analytics/insights for Instagram posts
- **generate_content_ideas**: Generate content ideas based on topics
- **get_pages**: Get list of managed Facebook pages

## Contact & Support
- Developer: Sam Schofield
- Email: samschofield90@hotmail.co.uk
- Business: Atlas Gyms (atlas-gyms.co.uk)

---

**Last Updated**: July 2, 2025
**Status**: OAuth configuration in progress
**Next Action**: Complete Google OAuth consent screen setup