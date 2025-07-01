# Deployment Guide

This guide will help you deploy the Meta Content Manager to GitHub and Vercel.

## 📋 Prerequisites

1. **GitHub Account**: [Sign up here](https://github.com)
2. **Vercel Account**: [Sign up here](https://vercel.com) (can use GitHub login)
3. **Meta App**: Your existing Meta App with credentials

## 🚀 Step 1: Deploy to GitHub

### Option A: Using GitHub CLI (Recommended)

1. Install GitHub CLI if you haven't: [Download here](https://cli.github.com/)

2. Login to GitHub:
```bash
gh auth login
```

3. Create repository and push:
```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Meta Content Manager"

# Create GitHub repository and push
gh repo create meta-content-manager --public --push --source=.
```

### Option B: Using GitHub Web Interface

1. Go to [GitHub](https://github.com) and create a new repository named `meta-content-manager`

2. Initialize git and push:
```bash
git init
git add .
git commit -m "Initial commit: Meta Content Manager"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/meta-content-manager.git
git push -u origin main
```

## 🌐 Step 2: Deploy to Vercel

### Option A: Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login and deploy:
```bash
vercel login
vercel --prod
```

### Option B: Vercel Web Interface

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Click "Deploy"

## ⚙️ Step 3: Configure Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add these variables:

```
META_APP_ID = 1667446050583846
META_ACCESS_TOKEN = your_actual_access_token_here
SECRET_KEY = your_secure_random_secret_key_here
FLASK_ENV = production
```

### Generating a Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

## 🔧 Step 4: Verify Deployment

1. Visit your Vercel app URL (provided after deployment)
2. Test the main features:
   - Home page loads
   - Content generation works
   - Facebook pages can be fetched (if token is valid)

## 🔄 Step 5: Continuous Deployment

Once connected, every push to your main branch will automatically deploy to Vercel.

To update your app:
```bash
git add .
git commit -m "Update: description of changes"
git push
```

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**: Check that `requirements.txt` is in the root directory
2. **Meta API Errors**: Verify your access token has the required permissions
3. **Environment Variables**: Make sure all required env vars are set in Vercel
4. **Static Files**: Ensure `static/` directory is committed to git

### Checking Logs:

- Vercel Dashboard → Your Project → Functions tab → View logs
- Local testing: `vercel dev`

## 📱 Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Navigate to "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## 🔒 Security Notes

- Never commit your `.env` file to GitHub
- Use strong, unique secret keys
- Regularly rotate your Meta access tokens
- Monitor your app for unusual activity

## 📊 Monitoring

Vercel provides:
- Analytics dashboard
- Function logs
- Performance metrics
- Error tracking

Access these in your Vercel project dashboard.

## 🆘 Support

If you encounter issues:

1. Check Vercel docs: [vercel.com/docs](https://vercel.com/docs)
2. Check Meta API docs: [developers.facebook.com](https://developers.facebook.com)
3. Review the logs in your Vercel dashboard