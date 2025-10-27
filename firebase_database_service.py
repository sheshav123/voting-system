#!/usr/bin/env python3
"""
Firebase Database Service
Handles all data operations using Firebase Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
import time

class FirebaseDatabaseService:
    def __init__(self):
        self.db = None
        self.initialized = False
        self.init_firebase()
    
    def init_firebase(self):
        """Initialize Firebase Admin SDK and Firestore"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Load service account key
                service_account_path = 'firebase-service-account.json'
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    self.initialized = True
                    print("✅ Firebase Firestore initialized successfully")
                else:
                    print("❌ Firebase service account file not found")
                    self.initialized = False
            else:
                self.db = firestore.client()
                self.initialized = True
                print("✅ Firebase Firestore already initialized")
                
        except Exception as e:
            print(f"❌ Error initializing Firebase Firestore: {e}")
            self.initialized = False
    
    # Voter Operations
    def add_voter(self, voter_data):
        """Add a voter to Firestore"""
        try:
            if not self.initialized:
                return False
            
            phone = voter_data['phone']
            doc_ref = self.db.collection('voters').document(phone)
            doc_ref.set(voter_data)
            return True
            
        except Exception as e:
            print(f"Error adding voter: {e}")
            return False
    
    def get_voter_by_phone(self, phone):
        """Get voter by phone number"""
        try:
            if not self.initialized:
                return None
            
            doc_ref = self.db.collection('voters').document(phone)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"Error getting voter: {e}")
            return None
    
    def get_voter_by_email(self, email):
        """Get voter by email address"""
        try:
            if not self.initialized:
                return None
            
            voters_ref = self.db.collection('voters')
            query = voters_ref.where('email', '==', email).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            print(f"Error getting voter by email: {e}")
            return None
    
    def get_all_voters(self):
        """Get all voters"""
        try:
            if not self.initialized:
                return []
            
            voters_ref = self.db.collection('voters')
            docs = voters_ref.stream()
            
            voters = []
            for doc in docs:
                voters.append(doc.to_dict())
            
            return voters
            
        except Exception as e:
            print(f"Error getting all voters: {e}")
            return []
    
    def update_voter(self, original_phone, updated_data):
        """Update voter information"""
        try:
            if not self.initialized:
                return False
            
            # Get existing voter
            existing_voter = self.get_voter_by_phone(original_phone)
            if not existing_voter:
                return False
            
            # Merge with updated data while preserving has_voted and photo
            updated_voter = {
                'name': updated_data.get('name', existing_voter.get('name')),
                'phone': updated_data.get('phone', existing_voter.get('phone')),
                'roll_number': updated_data.get('roll_number', existing_voter.get('roll_number')),
                'email': updated_data.get('email', existing_voter.get('email')),
                'has_voted': existing_voter.get('has_voted', False),
                'photo': existing_voter.get('photo')
            }
            
            new_phone = updated_data.get('phone', original_phone)
            
            # If phone number changed, create new document and delete old one
            if new_phone != original_phone:
                # Add new document
                new_doc_ref = self.db.collection('voters').document(new_phone)
                new_doc_ref.set(updated_voter)
                
                # Delete old document
                old_doc_ref = self.db.collection('voters').document(original_phone)
                old_doc_ref.delete()
            else:
                # Update existing document
                doc_ref = self.db.collection('voters').document(original_phone)
                doc_ref.set(updated_voter)
            
            return True
            
        except Exception as e:
            print(f"Error updating voter: {e}")
            return False
    
    def delete_voter(self, phone):
        """Delete a voter"""
        try:
            if not self.initialized:
                return False
            
            doc_ref = self.db.collection('voters').document(phone)
            doc_ref.delete()
            return True
            
        except Exception as e:
            print(f"Error deleting voter: {e}")
            return False
    
    def update_voter_photo(self, phone, photo_filename):
        """Update voter photo"""
        try:
            if not self.initialized:
                return False
            
            doc_ref = self.db.collection('voters').document(phone)
            doc_ref.update({'photo': photo_filename})
            return True
            
        except Exception as e:
            print(f"Error updating voter photo: {e}")
            return False
    
    # Candidate Operations
    def add_candidate(self, candidate_data):
        """Add a candidate to Firestore"""
        try:
            if not self.initialized:
                return False
            
            candidate_id = candidate_data['id']
            doc_ref = self.db.collection('candidates').document(candidate_id)
            doc_ref.set(candidate_data)
            return True
            
        except Exception as e:
            print(f"Error adding candidate: {e}")
            return False
    
    def get_all_candidates(self):
        """Get all candidates"""
        try:
            if not self.initialized:
                return []
            
            candidates_ref = self.db.collection('candidates')
            docs = candidates_ref.stream()
            
            candidates = []
            for doc in docs:
                candidates.append(doc.to_dict())
            
            return candidates
            
        except Exception as e:
            print(f"Error getting candidates: {e}")
            return []
    
    def delete_candidate(self, candidate_id):
        """Delete a candidate"""
        try:
            if not self.initialized:
                return False
            
            doc_ref = self.db.collection('candidates').document(candidate_id)
            doc_ref.delete()
            return True
            
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            return False
    
    # Election Operations
    def create_election(self, title, description):
        """Create a new election"""
        try:
            if not self.initialized:
                return False, None
            
            election_id = f"election_{int(time.time())}"
            
            election_data = {
                'id': election_id,
                'title': title,
                'description': description,
                'status': 'created',
                'created_at': datetime.now().isoformat(),
                'started_at': None,
                'ended_at': None,
                'total_votes': 0
            }
            
            doc_ref = self.db.collection('elections').document(election_id)
            doc_ref.set(election_data)
            
            return True, election_id
            
        except Exception as e:
            print(f"Error creating election: {e}")
            return False, None
    
    def get_all_elections(self):
        """Get all elections"""
        try:
            if not self.initialized:
                return []
            
            elections_ref = self.db.collection('elections')
            docs = elections_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            elections = []
            for doc in docs:
                elections.append(doc.to_dict())
            
            return elections
            
        except Exception as e:
            print(f"Error getting elections: {e}")
            return []
    
    def get_current_election(self):
        """Get the current active election"""
        try:
            if not self.initialized:
                return None
            
            elections_ref = self.db.collection('elections')
            query = elections_ref.where('status', '==', 'active').limit(1)
            docs = query.stream()
            
            for doc in docs:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            print(f"Error getting current election: {e}")
            return None
    
    def start_election(self, election_id):
        """Start an election"""
        try:
            if not self.initialized:
                return False, "Firebase not initialized"
            
            # Stop current election if any
            current = self.get_current_election()
            if current:
                self.stop_election(current['id'])
            
            # Start new election
            doc_ref = self.db.collection('elections').document(election_id)
            doc_ref.update({
                'status': 'active',
                'started_at': datetime.now().isoformat()
            })
            
            # Clear previous votes (start fresh)
            self.clear_all_votes()
            
            return True, "Election started successfully"
            
        except Exception as e:
            print(f"Error starting election: {e}")
            return False, str(e)
    
    def stop_election(self, election_id=None):
        """Stop an election"""
        try:
            if not self.initialized:
                return False, "Firebase not initialized"
            
            # If no election_id provided, get current active election
            if not election_id:
                current_election = self.get_current_election()
                if not current_election:
                    return False, "No active election to stop"
                election_id = current_election['id']
            
            # Count total votes
            votes = self.get_all_votes()
            total_votes = len([v for v in votes if v.get('election_id') == election_id])
            
            # Update election
            doc_ref = self.db.collection('elections').document(election_id)
            doc_ref.update({
                'status': 'ended',
                'ended_at': datetime.now().isoformat(),
                'total_votes': total_votes
            })
            
            return True, "Election stopped successfully"
            
        except Exception as e:
            print(f"Error stopping election: {e}")
            return False, str(e)
    
    def is_election_active(self):
        """Check if there's an active election"""
        current = self.get_current_election()
        return current and current['status'] == 'active'
    
    def delete_election(self, election_id):
        """Delete an election and all its associated votes"""
        try:
            if not self.initialized:
                return False, "Firebase not initialized"
            
            # Check if election exists
            doc_ref = self.db.collection('elections').document(election_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return False, "Election not found"
            
            election_data = doc.to_dict()
            
            # Don't allow deleting active elections
            if election_data.get('status') == 'active':
                return False, "Cannot delete active election. Stop it first."
            
            # Delete all votes associated with this election
            votes_ref = self.db.collection('votes')
            query = votes_ref.where('election_id', '==', election_id)
            vote_docs = query.stream()
            
            for vote_doc in vote_docs:
                vote_doc.reference.delete()
            
            # Delete the election
            doc_ref.delete()
            
            return True, "Election and associated votes deleted successfully"
            
        except Exception as e:
            print(f"Error deleting election: {e}")
            return False, str(e)
    
    # Vote Operations
    def cast_vote(self, voter_phone, candidate_id):
        """Cast a vote"""
        try:
            if not self.initialized:
                return False, "Firebase not initialized"
            
            if not self.is_election_active():
                return False, "No active election"
            
            current_election = self.get_current_election()
            vote_id = f"{voter_phone}_{current_election['id']}"
            
            # Check if already voted
            existing_vote = self.get_vote(vote_id)
            if existing_vote:
                return False, "Already voted in this election"
            
            # Record the vote
            vote_data = {
                'id': vote_id,
                'voter_phone': voter_phone,
                'candidate_id': candidate_id,
                'election_id': current_election['id'],
                'timestamp': datetime.now().isoformat()
            }
            
            doc_ref = self.db.collection('votes').document(vote_id)
            doc_ref.set(vote_data)
            
            # Update candidate vote count
            self.increment_candidate_votes(candidate_id)
            
            return True, "Vote cast successfully"
            
        except Exception as e:
            print(f"Error casting vote: {e}")
            return False, str(e)
    
    def get_vote(self, vote_id):
        """Get a specific vote"""
        try:
            if not self.initialized:
                return None
            
            doc_ref = self.db.collection('votes').document(vote_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"Error getting vote: {e}")
            return None
    
    def get_all_votes(self):
        """Get all votes"""
        try:
            if not self.initialized:
                return []
            
            votes_ref = self.db.collection('votes')
            docs = votes_ref.stream()
            
            votes = []
            for doc in docs:
                votes.append(doc.to_dict())
            
            return votes
            
        except Exception as e:
            print(f"Error getting votes: {e}")
            return []
    
    def has_voted_in_current_election(self, voter_phone):
        """Check if voter has voted in current election"""
        current_election = self.get_current_election()
        if not current_election:
            return False
        
        vote_id = f"{voter_phone}_{current_election['id']}"
        return self.get_vote(vote_id) is not None
    
    def increment_candidate_votes(self, candidate_id):
        """Increment candidate vote count"""
        try:
            if not self.initialized:
                return False
            
            doc_ref = self.db.collection('candidates').document(candidate_id)
            doc_ref.update({'votes': firestore.Increment(1)})
            return True
            
        except Exception as e:
            print(f"Error incrementing votes: {e}")
            return False
    
    def clear_all_votes(self):
        """Clear all votes (for new election)"""
        try:
            if not self.initialized:
                return False
            
            # Delete all votes
            votes_ref = self.db.collection('votes')
            docs = votes_ref.stream()
            
            for doc in docs:
                doc.reference.delete()
            
            # Reset candidate vote counts
            candidates_ref = self.db.collection('candidates')
            docs = candidates_ref.stream()
            
            for doc in docs:
                doc.reference.update({'votes': 0})
            
            return True
            
        except Exception as e:
            print(f"Error clearing votes: {e}")
            return False
    
    def get_voting_results(self, election_id=None):
        """Get voting results for an election"""
        try:
            if not self.initialized:
                return {'total_votes': 0, 'candidates': [], 'election': None}
            
            # Get target election
            if election_id:
                doc_ref = self.db.collection('elections').document(election_id)
                doc = doc_ref.get()
                target_election = doc.to_dict() if doc.exists else None
            else:
                target_election = self.get_current_election()
                if not target_election:
                    # Get last ended election
                    elections = self.get_all_elections()
                    ended_elections = [e for e in elections if e['status'] == 'ended']
                    target_election = ended_elections[0] if ended_elections else None
            
            if not target_election:
                return {'total_votes': 0, 'candidates': [], 'election': None}
            
            # Get votes for this election
            votes_ref = self.db.collection('votes')
            query = votes_ref.where('election_id', '==', target_election['id'])
            vote_docs = query.stream()
            
            election_votes = [doc.to_dict() for doc in vote_docs]
            
            # Get candidates and count votes
            candidates = self.get_all_candidates()
            results = {
                'total_votes': len(election_votes),
                'candidates': [],
                'election': target_election
            }
            
            for candidate in candidates:
                candidate_votes = sum(1 for vote in election_votes if vote['candidate_id'] == candidate['id'])
                results['candidates'].append({
                    'id': candidate['id'],
                    'name': candidate['name'],
                    'votes': candidate_votes,
                    'photo': candidate.get('photo', '')
                })
            
            # Sort by votes (descending)
            results['candidates'].sort(key=lambda x: x['votes'], reverse=True)
            
            return results
            
        except Exception as e:
            print(f"Error getting results: {e}")
            return {'total_votes': 0, 'candidates': [], 'election': None}

# Global instance
firebase_db = FirebaseDatabaseService()