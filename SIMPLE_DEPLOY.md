# 🚀 Simple Deployment (Your Firebase Keys Already Set)

## Option 1: Fly.io (Recommended - 2 Commands)

### Install Fly CLI
```bash
# macOS
brew install flyctl

# Or
curl -L https://fly.io/install.sh | sh
```

### Deploy
```bash
chmod +x deploy_flyio.sh
./deploy_flyio.sh
```

That's it! The script uses your existing Firebase credentials.

---

## Option 2: Render (Push to GitHub)

### 1. Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2. Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Connect your repository
5. Render auto-detects from `render.yaml`
6. In **Environment**, add these from your `firebase-service-account.json`:

```
FIREBASE_PROJECT_ID=voting-system-2024
FIREBASE_PRIVATE_KEY_ID=6be5f0d9c05134c89ee9de7d32a85d3e1c70a940
FIREBASE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
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
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@voting-system-2024.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=112735651629023911145
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40voting-system-2024.iam.gserviceaccount.com
FLASK_ENV=production
```

7. Click **Create Web Service**

---

## After Deployment

### Update Firebase Authorized Domains
1. Go to Firebase Console
2. **Authentication** → **Settings** → **Authorized domains**
3. Add your deployment URL:
   - Fly.io: `your-app.fly.dev`
   - Render: `your-app.onrender.com`

### Access Your App
- Main portal: `https://your-app-url.com`
- Admin panel: `https://your-app-url.com/admin`
- Admin password: `admin123`

---

## Which to Choose?

**Fly.io**: Faster, better free tier, no cold starts
**Render**: Easier if you prefer web dashboard, auto-deploys from GitHub

Both are free and simple!
