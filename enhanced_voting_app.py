#!/usr/bin/env python3
"""
Enhanced Voting System with Election Management
Features:
- Add/Delete Candidates
- Start/Stop Elections
- Direct Voter Addition
- Voter Portal (even after voting)
- Voter ID Card with Photo Upload
- Election Status Control
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import json
import time
import random
from datetime import datetime
import base64
from werkzeug.utils import secure_filename
from firebase_auth_integration import firebase_auth_service
from firebase_database_service import firebase_db

app = Flask(__name__)
app.secret_key = 'enhanced_voting_system_2024'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Create directories
os.makedirs('voting_data', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

# Data files
DATA_DIR = 'voting_data'
VOTERS_FILE = os.path.join(DATA_DIR, 'voters.json')
CANDIDATES_FILE = os.path.join(DATA_DIR, 'candidates.json')
VOTES_FILE = os.path.join(DATA_DIR, 'votes.json')
ELECTIONS_FILE = os.path.join(DATA_DIR, 'elections.json')
OTP_FILE = os.path.join(DATA_DIR, 'otps.json')

# Initialize data files
for file_path in [VOTERS_FILE, CANDIDATES_FILE, VOTES_FILE, ELECTIONS_FILE, OTP_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            if file_path == ELECTIONS_FILE:
                json.dump({
                    'current_election': None,
                    'elections': []
                }, f)
            else:
                json.dump({}, f)

class EnhancedVotingSystem:
    def __init__(self):
        pass
    
    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_data(self, file_path, data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False
    
    # Election Management
    def create_election(self, title, description):
        elections = self.load_data(ELECTIONS_FILE)
        election_id = f"election_{int(time.time())}"
        
        new_election = {
            'id': election_id,
            'title': title,
            'description': description,
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'ended_at': None,
            'total_votes': 0
        }
        
        elections['elections'].append(new_election)
        self.save_data(ELECTIONS_FILE, elections)
        return True, election_id
    
    def start_election(self, election_id):
        elections = self.load_data(ELECTIONS_FILE)
        
        # Stop current election if any
        if elections['current_election']:
            self.stop_election(elections['current_election'])
        
        # Start new election
        for election in elections['elections']:
            if election['id'] == election_id:
                election['status'] = 'active'
                election['started_at'] = datetime.now().isoformat()
                elections['current_election'] = election_id
                break
        
        # Reset votes for new election
        self.save_data(VOTES_FILE, {})
        
        self.save_data(ELECTIONS_FILE, elections)
        return True, "Election started successfully"
    
    def stop_election(self, election_id=None):
        elections = self.load_data(ELECTIONS_FILE)
        
        if not election_id:
            election_id = elections['current_election']
        
        if election_id:
            for election in elections['elections']:
                if election['id'] == election_id:
                    election['status'] = 'ended'
                    election['ended_at'] = datetime.now().isoformat()
                    
                    # Count total votes
                    votes = self.load_data(VOTES_FILE)
                    election['total_votes'] = len(votes)
                    break
            
            elections['current_election'] = None
        
        self.save_data(ELECTIONS_FILE, elections)
        return True, "Election stopped successfully"
    
    def get_current_election(self):
        elections = self.load_data(ELECTIONS_FILE)
        current_id = elections.get('current_election')
        
        if current_id:
            for election in elections['elections']:
                if election['id'] == current_id:
                    return election
        return None
    
    def get_all_elections(self):
        elections = self.load_data(ELECTIONS_FILE)
        return elections.get('elections', [])
    
    def is_election_active(self):
        current = self.get_current_election()
        return current and current['status'] == 'active'
    
    # Voter Management
    def add_voter(self, voter_data):
        voters = self.load_data(VOTERS_FILE)
        voters[voter_data['phone']] = voter_data
        return self.save_data(VOTERS_FILE, voters)
    
    def get_voter_by_phone(self, phone):
        voters = self.load_data(VOTERS_FILE)
        return voters.get(phone)
    
    def get_voter_by_email(self, email):
        voters = self.load_data(VOTERS_FILE)
        for phone, voter in voters.items():
            if voter.get('email', '').lower() == email.lower():
                return voter
        return None
    
    def update_voter_photo(self, phone, photo_filename):
        voters = self.load_data(VOTERS_FILE)
        if phone in voters:
            voters[phone]['photo'] = photo_filename
            return self.save_data(VOTERS_FILE, voters)
        return False
    
    def get_all_voters(self):
        voters = self.load_data(VOTERS_FILE)
        return list(voters.values())
    
    def update_voter(self, original_phone, updated_data):
        voters = self.load_data(VOTERS_FILE)
        
        if original_phone not in voters:
            return False
        
        # Get existing voter data
        existing_voter = voters[original_phone]
        
        # Update with new data while preserving has_voted and photo
        updated_voter = {
            'name': updated_data.get('name', existing_voter.get('name')),
            'phone': updated_data.get('phone', existing_voter.get('phone')),
            'roll_number': updated_data.get('roll_number', existing_voter.get('roll_number')),
            'email': updated_data.get('email', existing_voter.get('email')),
            'has_voted': existing_voter.get('has_voted', False),
            'photo': existing_voter.get('photo')
        }
        
        # If phone number changed, update the key
        new_phone = updated_data.get('phone', original_phone)
        if new_phone != original_phone:
            del voters[original_phone]
            voters[new_phone] = updated_voter
        else:
            voters[original_phone] = updated_voter
        
        return self.save_data(VOTERS_FILE, voters)
    
    def delete_voter(self, phone):
        voters = self.load_data(VOTERS_FILE)
        if phone in voters:
            del voters[phone]
            return self.save_data(VOTERS_FILE, voters)
        return False
    
    # Candidate Management
    def add_candidate(self, candidate_data):
        candidates = self.load_data(CANDIDATES_FILE)
        candidates[candidate_data['id']] = candidate_data
        return self.save_data(CANDIDATES_FILE, candidates)
    
    def delete_candidate(self, candidate_id):
        candidates = self.load_data(CANDIDATES_FILE)
        if candidate_id in candidates:
            del candidates[candidate_id]
            return self.save_data(CANDIDATES_FILE, candidates)
        return False
    
    def get_all_candidates(self):
        candidates = self.load_data(CANDIDATES_FILE)
        return list(candidates.values())
    
    # Voting
    def cast_vote(self, voter_phone, candidate_id):
        if not self.is_election_active():
            return False, "No active election"
        
        votes = self.load_data(VOTES_FILE)
        
        # Check if voter already voted in current election
        current_election = self.get_current_election()
        vote_key = f"{voter_phone}_{current_election['id']}"
        
        if vote_key in votes:
            return False, "Already voted in this election"
        
        # Record the vote
        votes[vote_key] = {
            'voter_phone': voter_phone,
            'candidate_id': candidate_id,
            'election_id': current_election['id'],
            'timestamp': datetime.now().isoformat()
        }
        
        if self.save_data(VOTES_FILE, votes):
            # Update candidate vote count
            candidates = self.load_data(CANDIDATES_FILE)
            if candidate_id in candidates:
                candidates[candidate_id]['votes'] = candidates[candidate_id].get('votes', 0) + 1
                self.save_data(CANDIDATES_FILE, candidates)
            return True, "Vote cast successfully"
        
        return False, "Error casting vote"
    
    def has_voted_in_current_election(self, voter_phone):
        current_election = self.get_current_election()
        if not current_election:
            return False
        
        votes = self.load_data(VOTES_FILE)
        vote_key = f"{voter_phone}_{current_election['id']}"
        return vote_key in votes
    
    def get_voting_results(self, election_id=None):
        # If no election_id provided, use current election or last ended election
        if not election_id:
            current_election = self.get_current_election()
            if current_election:
                target_election = current_election
            else:
                # Get last ended election
                elections = self.get_all_elections()
                ended_elections = [e for e in elections if e['status'] == 'ended']
                if ended_elections:
                    ended_elections.sort(key=lambda x: x.get('ended_at', ''), reverse=True)
                    target_election = ended_elections[0]
                else:
                    return {'total_votes': 0, 'candidates': [], 'election': None}
        else:
            # Find specific election
            elections = self.get_all_elections()
            target_election = next((e for e in elections if e['id'] == election_id), None)
            if not target_election:
                return {'total_votes': 0, 'candidates': [], 'election': None}
        
        votes = self.load_data(VOTES_FILE)
        candidates = self.load_data(CANDIDATES_FILE)
        
        # Count votes for target election
        election_votes = {k: v for k, v in votes.items() if v.get('election_id') == target_election['id']}
        
        results = {
            'total_votes': len(election_votes),
            'candidates': [],
            'election': target_election
        }
        
        # Get candidate results
        for candidate_id, candidate in candidates.items():
            candidate_votes = sum(1 for vote in election_votes.values() if vote['candidate_id'] == candidate_id)
            results['candidates'].append({
                'id': candidate_id,
                'name': candidate['name'],
                'votes': candidate_votes,
                'photo': candidate.get('photo', '')
            })
        
        # Sort by votes (descending)
        results['candidates'].sort(key=lambda x: x['votes'], reverse=True)
        
        return results
    
    # OTP System
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def send_otp(self, phone_number):
        otp = self.generate_otp()
        otps = self.load_data(OTP_FILE)
        
        otps[phone_number] = {
            'otp': otp,
            'timestamp': time.time(),
            'attempts': 0
        }
        
        self.save_data(OTP_FILE, otps)
        print(f"📱 OTP for {phone_number}: {otp}")
        
        return True, f"OTP sent successfully (Demo: {otp})"
    
    def verify_otp(self, phone_number, entered_otp):
        otps = self.load_data(OTP_FILE)
        
        if phone_number not in otps:
            return False, "OTP not found or expired"
        
        stored_data = otps[phone_number]
        
        # Check if OTP is expired (5 minutes)
        if time.time() - stored_data['timestamp'] > 300:
            del otps[phone_number]
            self.save_data(OTP_FILE, otps)
            return False, "OTP expired"
        
        # Check attempts limit
        if stored_data['attempts'] >= 3:
            del otps[phone_number]
            self.save_data(OTP_FILE, otps)
            return False, "Too many attempts"
        
        # Verify OTP
        if stored_data['otp'] == entered_otp:
            del otps[phone_number]
            self.save_data(OTP_FILE, otps)
            return True, "OTP verified successfully"
        else:
            stored_data['attempts'] += 1
            otps[phone_number] = stored_data
            self.save_data(OTP_FILE, otps)
            return False, "Invalid OTP"

# Use Firebase database service
voting_system = firebase_db

# Routes
@app.route('/')
def index():
    return render_template('unified_voter_portal.html')

@app.route('/voter-portal')
def voter_portal():
    return redirect(url_for('index'))

@app.route('/voting')
def voting_page():
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    return render_template('enhanced_admin.html')

# Google Sign-In Authentication Routes
@app.route('/verify-google-token', methods=['POST'])
def verify_google_token():
    """Verify Google Sign-In token and check if user is registered"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'success': False, 'message': 'Google ID token required'})
        
        print(f"🔥 Verifying Google token...")
        
        # Verify the Firebase ID token
        decoded_token, error = firebase_auth_service.verify_id_token(id_token)
        
        if error:
            print(f"❌ Token verification failed: {error}")
            return jsonify({'success': False, 'message': f'Google authentication failed: {error}'})
        
        email = decoded_token.get('email')
        name = decoded_token.get('name')
        firebase_uid = decoded_token.get('uid')
        
        print(f"✅ Google token verified for email: {email}")
        
        if not email:
            return jsonify({'success': False, 'message': 'Email not found in Google account'})
        
        # Check if voter exists in our system by email
        voter = voting_system.get_voter_by_email(email)
        if not voter:
            return jsonify({
                'success': False, 
                'message': f'Access denied. Email {email} is not registered as a voter. Please contact administrator.'
            })
        
        # Set session with Google authentication
        session['verified'] = True
        session['email'] = email
        session['voter'] = voter
        session['phone'] = voter['phone']  # Store phone for easy access
        session['firebase_uid'] = firebase_uid
        session['auth_method'] = 'google'
        session.permanent = True  # Make session persistent
        
        print(f"✅ Session created for voter: {voter['name']}")
        
        return jsonify({
            'success': True,
            'message': 'Google authentication successful',
            'voter': voter,
            'auth_method': 'google'
        })
        
    except Exception as e:
        print(f"❌ Google verification error: {e}")
        return jsonify({'success': False, 'message': f'Google authentication error: {str(e)}'})

# OTP Service Status
@app.route('/otp-service-status')
def otp_service_status():
    try:
        status = fast2sms_service.get_service_status()
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Voting Routes
@app.route('/get-candidates')
def get_candidates():
    try:
        if not session.get('verified'):
            return jsonify({'success': False, 'message': 'Authentication required'})
        
        if not voting_system.is_election_active():
            return jsonify({'success': False, 'message': 'No active election'})
        
        candidates = voting_system.get_all_candidates()
        return jsonify({'success': True, 'candidates': candidates})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/cast-vote', methods=['POST'])
def cast_vote():
    try:
        if not session.get('verified'):
            return jsonify({'success': False, 'message': 'Authentication required'})
        
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        phone = session.get('phone')
        
        if not candidate_id or not phone:
            return jsonify({'success': False, 'message': 'Invalid request'})
        
        success, message = voting_system.cast_vote(phone, candidate_id)
        
        return jsonify({'success': success, 'message': message})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Voter Portal Routes
@app.route('/voter-info')
def voter_info():
    try:
        if not session.get('verified'):
            return jsonify({'success': False, 'message': 'Authentication required'})
        
        voter = session.get('voter')
        phone = voter.get('phone') if voter else session.get('phone')
        
        if not voter or not phone:
            return jsonify({'success': False, 'message': 'Voter information not found in session'})
        
        # Get fresh voter data from database to ensure we have latest photo
        fresh_voter_data = voting_system.get_voter_by_phone(phone)
        if fresh_voter_data:
            # Update session with fresh data (especially photo)
            session['voter'] = fresh_voter_data
            session.modified = True
            voter = fresh_voter_data
        
        # Check if voted in current election
        has_voted = voting_system.has_voted_in_current_election(phone)
        current_election = voting_system.get_current_election()
        
        return jsonify({
            'success': True,
            'voter': voter,
            'has_voted': has_voted,
            'current_election': current_election
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    try:
        if not session.get('verified'):
            return jsonify({'success': False, 'message': 'Authentication required'})
        
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'No photo uploaded'})
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            phone = session.get('phone')
            filename = secure_filename(f"voter_{phone}_{int(time.time())}.jpg")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update voter record
            if voting_system.update_voter_photo(phone, filename):
                return jsonify({'success': True, 'message': 'Photo uploaded successfully', 'filename': filename})
            else:
                return jsonify({'success': False, 'message': 'Failed to update photo'})
        else:
            return jsonify({'success': False, 'message': 'Invalid file type'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Additional routes for enhanced functionality
@app.route('/election-status')
def election_status():
    try:
        current_election = voting_system.get_current_election()
        if current_election and current_election['status'] == 'active':
            return jsonify({'success': True, 'election': current_election})
        else:
            return jsonify({'success': False, 'message': 'No active election'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        secret_key = data.get('secret_key')
        
        if secret_key == 'admin123':  # Simple admin password
            session['admin'] = True
            session.permanent = True  # Make admin session persistent
            return jsonify({'success': True, 'message': 'Admin authenticated'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/results')
def get_results():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        results = voting_system.get_voting_results()
        return jsonify({'success': True, 'results': results})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/elections')
def get_elections():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        elections = voting_system.get_all_elections()
        current = voting_system.get_current_election()
        
        return jsonify({
            'success': True, 
            'elections': elections,
            'current_election': current
        })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/create-election', methods=['POST'])
def create_election():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        if not title:
            return jsonify({'success': False, 'message': 'Election title required'})
        
        success, election_id = voting_system.create_election(title, description)
        
        if success:
            return jsonify({'success': True, 'message': 'Election created successfully', 'election_id': election_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to create election'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/start-election', methods=['POST'])
def start_election():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        election_id = data.get('election_id')
        
        if not election_id:
            return jsonify({'success': False, 'message': 'Election ID required'})
        
        success, message = voting_system.start_election(election_id)
        return jsonify({'success': success, 'message': message})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/stop-election', methods=['POST'])
def stop_election():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        success, message = voting_system.stop_election()
        return jsonify({'success': success, 'message': message})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete-election', methods=['POST'])
def delete_election():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        election_id = data.get('election_id')
        
        if not election_id:
            return jsonify({'success': False, 'message': 'Election ID required'})
        
        success, message = voting_system.delete_election(election_id)
        return jsonify({'success': success, 'message': message})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/election-details/<election_id>')
def get_election_details(election_id):
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        results = voting_system.get_voting_results(election_id)
        return jsonify({'success': True, 'results': results})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/candidates')
def get_admin_candidates():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        candidates = voting_system.get_all_candidates()
        return jsonify({'success': True, 'candidates': candidates})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/add-candidate', methods=['POST'])
def add_candidate():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        name = data.get('name', '').strip()
        photo_url = data.get('photo_url', '').strip()
        
        if not name:
            return jsonify({'success': False, 'message': 'Candidate name required'})
        
        # Generate candidate ID
        candidate_id = name.lower().replace(' ', '_').replace('-', '_')
        
        candidate_data = {
            'id': candidate_id,
            'name': name,
            'photo': photo_url,
            'votes': 0
        }
        
        success = voting_system.add_candidate(candidate_data)
        
        if success:
            return jsonify({'success': True, 'message': f'Candidate {name} added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to add candidate'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete-candidate', methods=['POST'])
def delete_candidate():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        
        if not candidate_id:
            return jsonify({'success': False, 'message': 'Candidate ID required'})
        
        success = voting_system.delete_candidate(candidate_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Candidate deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete candidate'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/voters')
def get_all_voters():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        voters = voting_system.get_all_voters()
        return jsonify({'success': True, 'voters': voters})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/add-voter', methods=['POST'])
def add_voter():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        roll_number = data.get('roll_number', '').strip()
        email = data.get('email', '').strip()
        
        if not all([name, phone, roll_number, email]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Format phone number
        if not phone.startswith('+'):
            phone = '+91' + phone.replace(' ', '').replace('-', '')
        
        voter_data = {
            'name': name,
            'phone': phone,
            'roll_number': roll_number,
            'email': email,
            'has_voted': False,
            'photo': None
        }
        
        success = voting_system.add_voter(voter_data)
        
        if success:
            return jsonify({'success': True, 'message': f'Voter {name} added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to add voter'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/update-voter', methods=['POST'])
def update_voter():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        original_phone = data.get('original_phone', '').strip()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        roll_number = data.get('roll_number', '').strip()
        email = data.get('email', '').strip()
        
        if not all([original_phone, name, phone, roll_number, email]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Format phone number
        if not phone.startswith('+'):
            phone = '+91' + phone.replace(' ', '').replace('-', '')
        
        success = voting_system.update_voter(original_phone, {
            'name': name,
            'phone': phone,
            'roll_number': roll_number,
            'email': email
        })
        
        if success:
            return jsonify({'success': True, 'message': f'Voter {name} updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update voter'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete-voter', methods=['POST'])
def delete_voter_route():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        if not phone:
            return jsonify({'success': False, 'message': 'Phone number required'})
        
        success = voting_system.delete_voter(phone)
        
        if success:
            return jsonify({'success': True, 'message': 'Voter deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete voter'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/load-voters', methods=['POST'])
def load_voters():
    try:
        if not session.get('admin'):
            return jsonify({'success': False, 'message': 'Admin authentication required'})
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        # Save uploaded file temporarily
        import uuid
        temp_filename = f"temp_voters_{uuid.uuid4().hex[:8]}.xlsx"
        file.save(temp_filename)
        
        try:
            import pandas as pd
            
            # Read Excel file
            df = pd.read_excel(temp_filename)
            
            # Expected columns: name, phone, roll_number, email
            required_columns = ['name', 'phone', 'roll_number', 'email']
            
            if not all(col in df.columns for col in required_columns):
                return jsonify({'success': False, 'message': f'Excel file must contain columns: {required_columns}'})
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                # Fix phone number formatting (remove .0 from integers)
                phone = str(row['phone']).strip()
                if phone.endswith('.0'):
                    phone = phone[:-2]
                
                # Fix roll number formatting
                roll_number = str(row['roll_number']).strip()
                if roll_number.endswith('.0'):
                    roll_number = roll_number[:-2]
                
                # Fix email formatting (handle NaN values)
                email = str(row['email']).strip()
                if email == 'nan':
                    email = f"voter{phone}@example.com"  # Generate email if missing
                
                voter_data = {
                    'name': str(row['name']).strip(),
                    'phone': phone,
                    'roll_number': roll_number,
                    'email': email,
                    'has_voted': False,
                    'photo': None
                }
                
                # Validate phone number format
                if not voter_data['phone'].startswith('+'):
                    voter_data['phone'] = '+91' + voter_data['phone']
                
                if voting_system.add_voter(voter_data):
                    success_count += 1
                else:
                    error_count += 1
            
            message = f"Loaded {success_count} voters successfully. {error_count} errors."
            return jsonify({'success': True, 'message': message})
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Additional routes for unified voter portal
@app.route('/check-voter', methods=['POST'])
def check_voter():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        if not phone:
            return jsonify({'success': False, 'message': 'Phone number required'})
        
        voter = voting_system.get_voter_by_phone(phone)
        if voter:
            return jsonify({'success': True, 'message': 'Voter found'})
        else:
            return jsonify({'success': False, 'message': 'Voter not registered'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get-voter-by-phone', methods=['POST'])
def get_voter_by_phone():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        if not phone:
            return jsonify({'success': False, 'message': 'Phone number required'})
        
        voter = voting_system.get_voter_by_phone(phone)
        if voter:
            return jsonify({'success': True, 'voter': voter})
        else:
            return jsonify({'success': False, 'message': 'Voter not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/check-voter-status', methods=['POST'])
def check_voter_status():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        if not phone:
            return jsonify({'success': False, 'message': 'Phone number required'})
        
        has_voted = voting_system.has_voted_in_current_election(phone)
        return jsonify({'success': True, 'has_voted': has_voted})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get-last-election')
def get_last_election():
    try:
        elections = voting_system.get_all_elections()
        
        # Find the most recent ended election
        ended_elections = [e for e in elections if e['status'] == 'ended']
        
        if ended_elections:
            # Sort by ended_at date (most recent first)
            ended_elections.sort(key=lambda x: x.get('ended_at', ''), reverse=True)
            last_election = ended_elections[0]
            return jsonify({'success': True, 'election': last_election})
        else:
            return jsonify({'success': False, 'message': 'No completed elections found'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get-election-results')
def get_election_results():
    try:
        # Get current election results or last election results
        current_election = voting_system.get_current_election()
        
        if not current_election:
            # Get last election results
            elections = voting_system.get_all_elections()
            ended_elections = [e for e in elections if e['status'] == 'ended']
            
            if ended_elections:
                ended_elections.sort(key=lambda x: x.get('ended_at', ''), reverse=True)
                current_election = ended_elections[0]
            else:
                return jsonify({'success': False, 'message': 'No election results available'})
        
        results = voting_system.get_voting_results()
        return jsonify({'success': True, 'results': results})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/upload-voter-photo', methods=['POST'])
def upload_voter_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'No photo uploaded'})
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({'success': False, 'message': 'Phone number required'})
        
        file = request.files['photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filename = secure_filename(f"voter_{phone}_{int(time.time())}.jpg")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update voter record
            if voting_system.update_voter_photo(phone, filename):
                # Update session data with new photo
                if session.get('voter') and session.get('voter').get('phone') == phone:
                    session['voter']['photo'] = filename
                    session.modified = True
                
                return jsonify({'success': True, 'message': 'Photo uploaded successfully', 'filename': filename})
            else:
                return jsonify({'success': False, 'message': 'Failed to update photo'})
        else:
            return jsonify({'success': False, 'message': 'Invalid file type'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/auth-status')
def auth_status():
    try:
        status = {
            'auth_method': 'google_signin',
            'firebase_initialized': firebase_auth_service.initialized,
            'provider': 'Google Authentication',
            'ready': firebase_auth_service.initialized
        }
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/debug-firebase')
def debug_firebase():
    return render_template('debug_firebase.html')

@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Clear all session data
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    try:
        # Clear admin session
        session.pop('admin', None)
        return jsonify({'success': True, 'message': 'Admin logged out successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    import os
    
    print("🗳️  Unified Voting Portal System")
    print("=" * 40)
    
    # Get port from environment variable (for Heroku/Railway/etc)
    port = int(os.environ.get('PORT', 3000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    if debug_mode:
        print(f"🎯 Main Portal: http://localhost:{port}")
        print(f"🔧 Admin Panel: http://localhost:{port}/admin")
        print("🔑 Admin Password: admin123")
    else:
        print("🌐 Production mode - check your hosting platform for URL")
        print("🔧 Admin Panel: /admin")
        print("🔑 Admin Password: admin123")
    
    print("=" * 40)
    print("✨ Unified Features:")
    print("   • Google Sign-In authentication")
    print("   • Email-based voter verification")
    print("   • Single portal for all voting activities")
    print("   • Integrated voting & results")
    print("   • Real-time election status")
    print("   • Voter ID cards with photos")
    print("=" * 40)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)