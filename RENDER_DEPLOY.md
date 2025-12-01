# Deploy to Render (5 Minutes Setup)

## Why Render?
- ✅ Free tier (750 hours/month)
- ✅ Auto-deploys from GitHub
- ✅ Simple setup (5 minutes)
- ✅ No manual configuration needed

## Quick Setup

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Connect your repository
5. Render auto-detects settings from `render.yaml`
6. Add environment variables (see below)
7. Click **Create Web Service**

### 3. Add Environment Variables
In Render dashboard, go to **Environment** and add:

```
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_key_id
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n
FIREBASE_CLIENT_EMAIL=your_service_account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_CERT_URL=your_cert_url
```

### 4. Update Firebase Authorized Domains
1. Go to Firebase Console
2. **Authentication** → **Settings** → **Authorized domains**
3. Add your Render URL: `your-app-name.onrender.com`

## Done! 🎉
Your app will be live at: `https://your-app-name.onrender.com`

## Notes
- Free tier: App sleeps after 15 min inactivity (cold start ~30 sec)
- Auto-deploys on every git push
- Admin panel: `/admin` (password: admin123)

## Alternative: Fly.io (Even Simpler)
If you want even more free resources, try Fly.io - see FLYIO_DEPLOY.md
