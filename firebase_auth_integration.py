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
                # Load service account key
                service_account_path = 'firebase-service-account.json'
                
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    self.initialized = True
                    print("✅ Firebase Admin SDK initialized successfully")
                else:
                    print("❌ Firebase service account file not found")
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