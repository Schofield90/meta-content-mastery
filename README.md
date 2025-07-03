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

## 🎯 Current Status (When You Return)

### ✅ **COMPLETED FEATURES:**
1. **Supabase Integration** - Persistent database and image storage
2. **Bulk Upload Page** - Professional drag & drop interface at `/bulk-upload`
3. **Claude AI Training Hub** - Complete training interface at `/claude-training`
4. **Google Drive Removal** - Eliminated all OAuth complexity 
5. **Environment Setup** - All required variables configured in Vercel
6. **Database Schema** - Tables created and ready for data

### 🚀 **READY TO USE:**
- **Bulk Upload**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/bulk-upload`
- **Claude Training Hub**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/claude-training`
- **AI Training**: Upload images → Build content library → Generate better posts
- **Categories**: Workouts, Equipment, Testimonials, Facility, etc.
- **Persistent Storage**: All data survives app restarts

### 📋 **NEXT STEPS (When You Pick This Up):**

1. **🤖 Train Claude for Your Business** (15 minutes)
   - Go to `/claude-training` in your app
   - Add knowledge about Atlas Gyms in "Teach Claude" tab
   - Fill in business basics, services, target audience, brand voice
   - Test Claude's knowledge with the assessment feature
   - Chat with Claude to see how it responds with your business context

2. **✅ Test Bulk Upload** (5 minutes)
   - Go to `/bulk-upload` in your app
   - Drag & drop 10-20 gym images
   - Verify they upload to Supabase successfully
   - Check different categories work

3. **🎯 Train Your AI** (30 minutes) 
   - Upload 50+ images across categories
   - Fill out business profile in AI Training
   - Add successful social media posts to content library
   - Test Smart Post Creator with your training data

4. **📈 Scale Content Creation** (Ongoing)
   - Use Smart Post Creator for daily content
   - Build library of high-performing posts
   - Train Claude with more business knowledge
   - Export to Meta platforms

### 🔧 **If Issues Arise:**
- **Deployment problems**: Check Vercel dashboard for errors
- **Upload failures**: Verify Supabase credentials in Vercel environment
- **Missing features**: Check deployment has latest commit (`3ea49d2`)

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
- **Claude Training Hub**: Train Claude specifically about your business with knowledge assessment
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

### Common Issues (Updated)
1. **Bulk upload not working**: Check Supabase credentials in Vercel environment
2. **Images not saving**: Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set
3. **App not loading**: Check Vercel deployment status and logs
4. **Missing navigation**: Ensure latest code is deployed (commit `3ea49d2` or later)

### Debug Steps
1. **Check deployment**: Visit `/health` endpoint to see current version
2. **Verify environment**: Ensure all Supabase variables are set in Vercel
3. **Test Supabase**: Check your Supabase project dashboard for storage bucket
4. **Check logs**: Review Vercel function logs for detailed error messages

### Quick Health Check
- **App URL**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app`
- **Health Check**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/health`
- **Claude Training Hub**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/claude-training`
- **Bulk Upload**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/bulk-upload`

### Success Indicators
- ✅ Health endpoint shows version 2.1+
- ✅ "Claude Training Hub" appears in navigation menu
- ✅ "Bulk Upload" appears in navigation menu
- ✅ Claude Training Hub loads with 4 tabs: Teach Claude, Test Knowledge, Knowledge Base, Chat
- ✅ Bulk upload page loads with drag & drop interface
- ✅ Images upload successfully to Supabase

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

**Last Updated**: July 3, 2025
**Status**: ✅ FULLY FUNCTIONAL - Google Drive removed, Supabase integrated
**Next Action**: Test bulk upload feature and start training AI with your images