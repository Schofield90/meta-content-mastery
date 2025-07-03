# Meta Content Manager - Claude MCP Integration

## Project Overview
Meta Content Manager is a Flask-based web application that integrates with Meta's Graph API, OpenAI's API, and Google Drive to provide social media content creation and management capabilities. The app is deployed on Vercel and features AI-powered content generation, social media posting, and training data management.

## Current Status & Next Steps

### ✅ Completed Features
- Flask web application with multiple routes for content creation
- Meta API integration for Facebook and Instagram posting
- OpenAI integration for AI content generation and image creation
- Google Drive OAuth integration for image management
- AI training system with business profile and content library
- Vercel deployment configuration

### 🚨 Current Issue: Google OAuth "Access blocked: authorisation error"
**Status**: IN PROGRESS - OAuth consent screen needs configuration

**Problem**: 
- Error 400: invalid_request
- App doesn't comply with Google's OAuth 2.0 policy

**Solution**: Complete OAuth consent screen setup in Google Cloud Console

**Required OAuth Consent Screen Fields** (CRITICAL):
1. **Application home page**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app`
2. **Application privacy policy link**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/privacy`
3. **Application terms of service link**: `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/terms`
4. **Authorized domains**: `vercel.app`

**Google OAuth Configuration**:
- Client ID: `1071902930073-as763hgtkglfvj1ag9jeuonus4pvdlqc.apps.googleusercontent.com`
- Client Secret: `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`
- Redirect URIs: 
  - `https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app/oauth/google/callback`
  - `https://meta-content-mastery-766ozocne-schofield90s-projects.vercel.app/oauth/google/callback`

### 🛠️ Immediate Next Steps

1. **Complete OAuth Consent Screen** (HIGH PRIORITY)
   - Fill in required fields mentioned above
   - Create placeholder privacy policy and terms pages
   - Add test users to test the OAuth flow
   - Set publishing status to "Testing"

2. **Create Missing Pages**
   - Create `/privacy` route and template
   - Create `/terms` route and template
   - These can be simple placeholder pages initially

3. **Test OAuth Flow**
   - Once consent screen is configured, wait 5-10 minutes for propagation
   - Test Google Drive authentication in the AI Training section
   - Verify successful OAuth callback

## Environment Variables

### Vercel Environment Variables (Required)
```
GOOGLE_CLIENT_ID=1071902930073-as763hgtkglfvj1ag9jeuonus4pvdlqc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
OPENAI_API_KEY=[Your OpenAI API Key]
META_ACCESS_TOKEN=[Your Meta Access Token]
META_APP_ID=1667446050583846
SECRET_KEY=[Your Flask Secret Key]
VERCEL_URL=https://claude-meta-99sce5xcm-schofield90s-projects.vercel.app
```

## Application Structure

### Main Features
- **Content Creation**: AI-powered social media content generation
- **Smart Posts**: Intelligent post creation with business context
- **AI Training**: Business profile and content library management
- **Google Drive Integration**: Image access and management
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
3. **Google Drive API**: Image access and training data management

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