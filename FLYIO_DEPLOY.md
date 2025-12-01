# Deploy to Fly.io (3 Minutes Setup)

## Why Fly.io?
- ✅ More generous free tier (3 VMs, 3GB storage)
- ✅ No cold starts
- ✅ Fastest setup (3 minutes)
- ✅ Better performance than Render free tier

## Setup

### 1. Install Fly CLI
```bash
# macOS
brew install flyctl

# Or use install script
curl -L https://fly.io/install.sh | sh
```

### 2. Sign Up & Login
```bash
flyctl auth signup
# or
flyctl auth login
```

### 3. Deploy
```bash
# In your project directory
flyctl launch

# Follow prompts:
# - App name: choose a name
# - Region: choose closest to you
# - PostgreSQL: No
# - Redis: No
```

### 4. Set Environment Variables
```bash
flyctl secrets set FIREBASE_PROJECT_ID="your_project_id"
flyctl secrets set FIREBASE_PRIVATE_KEY_ID="your_key_id"
flyctl secrets set FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
flyctl secrets set FIREBASE_CLIENT_EMAIL="your_service_account@project.iam.gserviceaccount.com"
flyctl secrets set FIREBASE_CLIENT_ID="your_client_id"
flyctl secrets set FIREBASE_CLIENT_CERT_URL="your_cert_url"
flyctl secrets set FLASK_ENV="production"
```

### 5. Update Firebase Authorized Domains
1. Go to Firebase Console
2. **Authentication** → **Settings** → **Authorized domains**
3. Add: `your-app-name.fly.dev`

## Done! 🎉
Your app is live at: `https://your-app-name.fly.dev`

## Update Your App
```bash
git add .
git commit -m "updates"
flyctl deploy
```

## Free Tier Limits
- 3 shared VMs
- 3GB storage
- 160GB bandwidth/month
- No cold starts!

## Admin Access
- URL: `https://your-app-name.fly.dev/admin`
- Password: admin123
