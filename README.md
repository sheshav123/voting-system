# Decentralised Voting System

## 🚀 Free Deployment on PythonAnywhere

This app can be deployed **FREE for lifetime** on PythonAnywhere! See [PYTHONANYWHERE_SETUP.md](PYTHONANYWHERE_SETUP.md) for detailed deployment instructions. 🗳️

A secure, decentralised voting application with Firebase integration, Google authentication, and real-time results.

## Features ✨

- **Google Sign-In Authentication** - Secure voter verification
- **Email-based Voter Registration** - Admin can add voters by email
- **Real-time Election Management** - Start/stop elections dynamically
- **Candidate Management** - Add/remove candidates with photos
- **Voter ID Cards** - Photo upload and ID card generation
- **Live Results** - Real-time vote counting and results
- **Admin Dashboard** - Complete election management interface
- **Mobile Responsive** - Works on all devices

## Quick Deploy 🚀

### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### Deploy to Render
1. Fork this repository
2. Connect to Render
3. Set environment variables
4. Deploy!

## Local Development 💻

### Prerequisites
- Python 3.11+
- Firebase project with Authentication and Realtime Database enabled

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voting-system.git
   cd voting-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Firebase configuration
   ```

5. **Add Firebase service account**
   - Download your Firebase service account JSON
   - Save as `firebase-service-account.json`

6. **Run the application**
   ```bash
   python decentralised_voting_app.py
   ```

7. **Access the application**
   - Voter Portal: http://localhost:3000
   - Admin Panel: http://localhost:3000/admin
   - Admin Password: `admin123`

## Configuration 🔧

### Firebase Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create new project
   - Enable Authentication (Google provider)
   - Enable Realtime Database

2. **Get Configuration**
   - Project Settings → General → Web apps
   - Copy the config values to your `.env` file

3. **Service Account**
   - Project Settings → Service Accounts
   - Generate new private key
   - Save as `firebase-service-account.json`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FIREBASE_API_KEY` | Firebase API key | Yes |
| `FIREBASE_AUTH_DOMAIN` | Firebase auth domain | Yes |
| `FIREBASE_DATABASE_URL` | Firebase database URL | Yes |
| `FIREBASE_PROJECT_ID` | Firebase project ID | Yes |
| `FIREBASE_STORAGE_BUCKET` | Firebase storage bucket | Yes |
| `FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID | Yes |
| `FIREBASE_APP_ID` | Firebase app ID | Yes |
| `ADMIN_SECRET_KEY` | Admin panel password | Yes |
| `FAST2SMS_API_KEY` | Fast2SMS API key (optional) | No |

## Usage 📱

### For Voters
1. Visit the voting portal
2. Sign in with Google account
3. Verify your email is registered
4. Upload your photo for ID card
5. Vote when election is active
6. View results after voting

### For Administrators
1. Go to `/admin`
2. Login with admin password
3. Add voters (individual or bulk upload)
4. Add candidates with photos
5. Create and manage elections
6. Start/stop voting
7. View real-time results

## API Endpoints 🔌

### Authentication
- `POST /verify-google-token` - Verify Google Sign-In token

### Voting
- `GET /get-candidates` - Get all candidates
- `POST /cast-vote` - Cast a vote
- `GET /voter-info` - Get voter information

### Admin
- `POST /admin/login` - Admin authentication
- `GET /admin/voters` - Get all voters
- `POST /admin/add-voter` - Add new voter
- `POST /admin/add-candidate` - Add new candidate
- `POST /admin/create-election` - Create election
- `POST /admin/start-election` - Start election
- `POST /admin/stop-election` - Stop election
- `GET /admin/results` - Get voting results

## Security 🔒

- Google OAuth 2.0 authentication
- Firebase security rules
- Session management
- Input validation and sanitization
- CORS protection
- Secure file uploads

## Contributing 🤝

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support and questions:
- Create an issue on GitHub
- Email: sheshavanand@gmail.com

---

Made with ❤️ for secure and transparent elections
