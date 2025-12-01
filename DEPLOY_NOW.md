# 🚀 Deploy to Render (100% Free - No Credit Card)

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

If you don't have a GitHub repo yet:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 2: Deploy on Render

1. Go to **https://render.com**
2. Click **Get Started for Free**
3. Sign up with GitHub
4. Click **New +** → **Web Service**
5. Click **Connect** next to your repository
6. Render will auto-detect settings from `render.yaml`

**If Render asks for manual configuration:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn decentralised_voting_app:app`

## Step 3: Add Environment Variables

In the Render dashboard, scroll to **Environment Variables** and add:

```
FIREBASE_PROJECT_ID
voting-system-2024

FIREBASE_PRIVATE_KEY_ID
6be5f0d9c05134c89ee9de7d32a85d3e1c70a940

FIREBASE_PRIVATE_KEY
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCshthX40FccKbk
WdWFn42z/4kiEHKVFazuQNH4ggQyX/M92L5gO6llfN+q/s9OGPrVyBXGspwbDtS9
UE2oZkXIQsYgoyC3BgbERBib/pBuocfvxhPZS0HdW1PdAYG4tFWNcshJA8dFVlr0
NVJUCMTbwSdm0rBN7h/e0NxrqTL+yV/UuNyjlKXCPImZUczNWrpbAOiIhsfmBIox
P6Lv0vNotOQj7M0YHhmm5PYlx5R6y149H0x+71XA92MGbbw8DiBCWp4B2eFLuO6o
3JxeH2BwZRzNvyyFW+y8LT/M+enSvJycOPdxmLBN6ASf6Agd4yqjt+KK1dKfLobW
oU3mgvEvAgMBAAECggEADA4GYwQa0D3oa19oVZENP0NFO0wXtX/X0kEiBFGRWYCH
m0ETWRLSIA7Wa591fLXiHbqzsTgc3QciqXFJYjeplV4upp+MIAqCKCFZ8HLPd+t1
8BsDzm49VYPI6FHvbnVE3qbjUVBVeOxmKCO4DO2DIJe7P3cy1Avymu8Dd8JRMQ9j
oNsYURrY/qLm33BLNjqwArXoW0MI8SyzhJMqjF7dJDcnjCIsjVdRXdKcwAs07FcF
hpeVByqkoIv4k2lzCrE0Q3azQifFtBsXt7bQIrKco71UqxwTCZMt74KQglnXCHFY
29EFNpr2yIkZOHgAAR6rV/mDe5qXGf1SqZoTX+HkgQKBgQDbNp4qrVzzkISpKWW/
FTpO2Btmc0358A57e8fB3UO8mEZwcpQe9nh/Oy9wzTFoewIXtKU9wgjA/13oMzQ5
j1CLhhJwDtF4XWKhApJ4GVfwAid43efdPxkO6ba2Gv9kK/BsdtweeIe4351csty7
Tm5p0ozjz+EUUhb0rgYIuyZhewKBgQDJepNLfO2a8blbkMvLKcDmBYR27QyPpgl5
Qmwe/xH97pqErtXHj88t5r7yroxpp3WgeOVIO8GbG4z71/EN+2Vxlv7Qbazpm9JV
L2fvraMpDcuSSn/u5DyLBZlr5xGcmfw9AZFip3rXCK90fsaqwe8jBGsdZKg0HcuM
Z5TR8L8+3QKBgBC8A6kIYP8q+iWbxmum6DOapcTVao949vIQSfiPtpsQGNh+trYC
ZMJ5ty5qS6pJMaiznqWvSVHKbNXMCuGWAjUUgBXT28PPhTb7ZkkKzj7BO1grwIaQ
SY5s4wjV2MdB33G4RSeCVgIT+ARalyUpYJ5td1nwxaLyfVQicM170/s/AoGBAJAS
puGEJCR4ViO0FwbghJ/3shGY0TKneH7NkKNZonQC+1uF6jkaDPy11DWVu7KRnPtz
eAF/OaLAwMAWWrm024Wug+hnhQ5H7tAbZidt8w6YXsntnC4n52NCTcNrKJzjQAwf
4ua4/I5oF48mWMoig+52amJKaD1cUQHF0BWQIjHBAoGAWhtGnFGkR4vWYI2Rrd7a
EScoMbtirTUZ6hbKme1CyD/i7i3nbsoyIHSrprgfThENMg82K5oVYQc2nsLKJxac
ttVv5Ch0odZWpVJ2QSbp7kLHstDBrYSe3mk8GWMkFnA78frc9M8IrP5OGvo+qzaX
orjkxFsvdNS8dWl4KpmtltM=
-----END PRIVATE KEY-----

FIREBASE_CLIENT_EMAIL
firebase-adminsdk-fbsvc@voting-system-2024.iam.gserviceaccount.com

FIREBASE_CLIENT_ID
112735651629023911145

FIREBASE_CLIENT_CERT_URL
https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40voting-system-2024.iam.gserviceaccount.com

FLASK_ENV
production
```

## Step 4: Create Web Service

Click **Create Web Service** - Render will start deploying!

## Step 5: Update Firebase

1. Go to **Firebase Console**
2. **Authentication** → **Settings** → **Authorized domains**
3. Add: `your-app-name.onrender.com` (you'll see this in Render dashboard)

## Done! 🎉

Your app will be live at: `https://your-app-name.onrender.com`

- Main portal: `https://your-app-name.onrender.com`
- Admin panel: `https://your-app-name.onrender.com/admin`
- Admin password: `admin123`

## Notes

- **Free tier**: 750 hours/month (enough for 1 app)
- **Cold starts**: App sleeps after 15 min inactivity (~30 sec to wake)
- **Auto-deploy**: Every git push triggers new deployment
- **No credit card required!**

## Alternative: Vercel (Even Simpler)

If Render doesn't work, try Vercel - see `VERCEL_DEPLOY.md`
