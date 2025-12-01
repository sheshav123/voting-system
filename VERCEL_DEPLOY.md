# 🚀 Deploy to Vercel (Easiest Option)

Vercel is even simpler than Render - no configuration needed!

## Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

## Step 2: Deploy

```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- What's your project's name? (press enter for default)
- In which directory is your code located? **.**
- Want to override settings? **N**

## Step 3: Add Environment Variables

```bash
vercel env add FIREBASE_PROJECT_ID
# Enter: voting-system-2024

vercel env add FIREBASE_PRIVATE_KEY_ID
# Enter: 6be5f0d9c05134c89ee9de7d32a85d3e1c70a940

vercel env add FIREBASE_CLIENT_EMAIL
# Enter: firebase-adminsdk-fbsvc@voting-system-2024.iam.gserviceaccount.com

vercel env add FIREBASE_CLIENT_ID
# Enter: 112735651629023911145

vercel env add FIREBASE_CLIENT_CERT_URL
# Enter: https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40voting-system-2024.iam.gserviceaccount.com

vercel env add FLASK_ENV
# Enter: production
```

For the private key (multi-line):
```bash
vercel env add FIREBASE_PRIVATE_KEY
# Paste the entire private key including BEGIN and END lines
```

## Step 4: Redeploy with Environment Variables

```bash
vercel --prod
```

## Step 5: Update Firebase

1. Go to **Firebase Console**
2. **Authentication** → **Settings** → **Authorized domains**
3. Add your Vercel domain (shown after deployment)

## Done! 🎉

Your app is live! Vercel will show you the URL.

## Update Your App

```bash
git add .
git commit -m "updates"
vercel --prod
```

## Why Vercel?

- ✅ Fastest deployment (1 command)
- ✅ No cold starts
- ✅ Free SSL
- ✅ Global CDN
- ✅ No credit card required
- ✅ Generous free tier

## Note

Vercel is optimized for serverless. If you have issues with file uploads, use Render instead.
