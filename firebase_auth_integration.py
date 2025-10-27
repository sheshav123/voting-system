#!/usr/bin/env python3
"""
Firebase Authentication Integration for OTP
This module provides Firebase Admin SDK integration for phone authentication
"""

import firebase_admin
from firebase_admin import credentials, auth
import os
import json

class FirebaseAuthService:
    def __init__(self):
        self.initialized = False
        self.init_firebase()
    
    def init_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to load service account from file first
                service_account_path = 'firebase-service-account.json'
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    self.initialized = True
                    print("✅ Firebase Admin SDK initialized from file")
                else:
                    # Try to load from environment variables
                    service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
                    
                    if service_account_json:
                        try:
                            service_account_info = json.loads(service_account_json)
                            cred = credentials.Certificate(service_account_info)
                            firebase_admin.initialize_app(cred)
                            self.initialized = True
                            print("✅ Firebase Admin SDK initialized from environment variables")
                        except json.JSONDecodeError as e:
                            print(f"❌ Invalid JSON in FIREBASE_SERVICE_ACCOUNT_JSON: {e}")
                            self.initialized = False
                    else:
                        # Fallback: try to create service account info from individual env vars
                        project_id = os.environ.get('FIREBASE_PROJECT_ID')
                        private_key = os.environ.get('FIREBASE_PRIVATE_KEY')
                        client_email = os.environ.get('FIREBASE_CLIENT_EMAIL')
                        
                        if project_id and private_key and client_email:
                            service_account_info = {
                                "type": "service_account",
                                "project_id": project_id,
                                "private_key": private_key.replace('\\n', '\n'),
                                "client_email": client_email,
                                "client_id": os.environ.get('FIREBASE_CLIENT_ID', ''),
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}"
                            }
                            
                            cred = credentials.Certificate(service_account_info)
                            firebase_admin.initialize_app(cred)
                            self.initialized = True
                            print("✅ Firebase Admin SDK initialized from individual environment variables")
                        else:
                            print("❌ Firebase service account credentials not found in environment variables")
                            print("Required: FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL")
                            self.initialized = False
            else:
                self.initialized = True
                print("✅ Firebase Admin SDK already initialized")
                
        except Exception as e:
            print(f"❌ Error initializing Firebase: {e}")
            self.initialized = False
    
    def verify_id_token(self, id_token):
        """Verify Firebase ID token"""
        if not self.initialized:
            return None, "Firebase not initialized"
        
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token, None
        except Exception as e:
            return None, str(e)
    
    def get_user_by_phone(self, phone_number):
        """Get user by phone number"""
        if not self.initialized:
            return None, "Firebase not initialized"
        
        try:
            user = auth.get_user_by_phone_number(phone_number)
            return user, None
        except Exception as e:
            return None, str(e)
    
    def create_custom_token(self, uid, additional_claims=None):
        """Create custom token for user"""
        if not self.initialized:
            return None, "Firebase not initialized"
        
        try:
            custom_token = auth.create_custom_token(uid, additional_claims)
            return custom_token, None
        except Exception as e:
            return None, str(e)

# Global instance
firebase_auth_service = FirebaseAuthService()