# PythonAnywhere Deployment Guide

## Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com
2. Sign up for a **FREE Beginner account**
3. Verify your email

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)
1. Push your code to GitHub
2. In PythonAnywhere, open a **Bash console**
3. Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### Option B: Upload Files Manually
1. Go to **Files** tab in PythonAnywhere
2. Upload your project files

## Step 3: Create Virtual Environment
In the Bash console:
```bash
cd ~/YOUR_PROJECT_FOLDER
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Set Up Environment Variables
1. Go to **Files** tab
2. Navigate to your project folder
3. Create `.env` file with your credentials:
```
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your_service_account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=your_cert_url
FLASK_ENV=production
```

## Step 5: Configure Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click through the wizard

## Step 6: Configure WSGI File
1. In the **Web** tab, find the **Code** section
2. Click on the WSGI configuration file link
3. **Delete all existing content**
4. Copy and paste the content from `wsgi.py` in your project
5. **Update these lines**:
   - Replace `YOUR_USERNAME` with your PythonAnywhere username
   - Replace `YOUR_PROJECT_FOLDER` with your project folder name
   
Example:
```python
project_home = '/home/myusername/decentralised-voting-app'
```

## Step 7: Set Virtual Environment Path
1. In the **Web** tab, find **Virtualenv** section
2. Enter the path to your virtual environment:
```
/home/YOUR_USERNAME/YOUR_PROJECT_FOLDER/venv
```

## Step 8: Configure Static Files
In the **Web** tab, add static files mapping:

| URL | Directory |
|-----|-----------|
| /static/ | /home/YOUR_USERNAME/YOUR_PROJECT_FOLDER/static |

## Step 9: Create Required Directories
In Bash console:
```bash
cd ~/YOUR_PROJECT_FOLDER
mkdir -p voting_data
mkdir -p static/uploads
chmod 755 voting_data
chmod 755 static/uploads
```

## Step 10: Reload Web App
1. Go to **Web** tab
2. Click the big green **Reload** button
3. Your app should now be live at: `YOUR_USERNAME.pythonanywhere.com`

## Step 11: Configure Firebase for Your Domain
1. Go to Firebase Console
2. Navigate to **Authentication** > **Settings** > **Authorized domains**
3. Add your PythonAnywhere domain:
   - `YOUR_USERNAME.pythonanywhere.com`

## Troubleshooting

### Check Error Logs
1. Go to **Web** tab
2. Click on **Error log** link
3. Check for any errors

### Common Issues

**Import Errors:**
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

**Firebase Connection Issues:**
- Verify `.env` file exists and has correct values
- Check Firebase credentials are properly formatted
- Ensure private key has `\n` for newlines

**Permission Errors:**
- Run: `chmod 755 voting_data static/uploads`

**Static Files Not Loading:**
- Verify static files mapping in Web tab
- Check file paths are correct

### View Logs
```bash
# In Bash console
cd ~/YOUR_PROJECT_FOLDER
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

## Updating Your App
When you make changes:
```bash
# In Bash console
cd ~/YOUR_PROJECT_FOLDER
git pull  # if using Git
source venv/bin/activate
pip install -r requirements.txt  # if requirements changed
```

Then reload the web app from the **Web** tab.

## Free Tier Limitations
- 1 web app
- 512MB disk space
- Limited CPU time per day
- App domain: `username.pythonanywhere.com`
- No custom domain on free tier

## Admin Access
- Admin panel: `https://YOUR_USERNAME.pythonanywhere.com/admin`
- Admin password: `admin123` (change this in production!)

## Security Notes
1. Change the admin password in `decentralised_voting_app.py`
2. Keep your `.env` file secure
3. Never commit `.env` to Git
4. Use strong Firebase security rules

## Support
- PythonAnywhere Help: https://help.pythonanywhere.com
- Forums: https://www.pythonanywhere.com/forums/
