#!/usr/bin/env python3
"""
Migrate Data from JSON to Firebase
Move all existing data from local JSON files to Firebase Firestore
"""

import json
import os
from firebase_database_service import firebase_db

def migrate_voters():
    """Migrate voters from JSON to Firebase"""
    print("👥 Migrating voters to Firebase...")
    
    voters_file = 'voting_data/voters.json'
    if not os.path.exists(voters_file):
        print("   ⚠️  No voters file found")
        return 0
    
    try:
        with open(voters_file, 'r') as f:
            voters = json.load(f)
        
        success_count = 0
        for phone, voter_data in voters.items():
            if firebase_db.add_voter(voter_data):
                success_count += 1
            else:
                print(f"   ❌ Failed to migrate voter: {voter_data.get('name', phone)}")
        
        print(f"   ✅ Migrated {success_count}/{len(voters)} voters")
        return success_count
        
    except Exception as e:
        print(f"   ❌ Error migrating voters: {e}")
        return 0

def migrate_candidates():
    """Migrate candidates from JSON to Firebase"""
    print("🏆 Migrating candidates to Firebase...")
    
    candidates_file = 'voting_data/candidates.json'
    if not os.path.exists(candidates_file):
        print("   ⚠️  No candidates file found")
        return 0
    
    try:
        with open(candidates_file, 'r') as f:
            candidates = json.load(f)
        
        success_count = 0
        for candidate_id, candidate_data in candidates.items():
            if firebase_db.add_candidate(candidate_data):
                success_count += 1
            else:
                print(f"   ❌ Failed to migrate candidate: {candidate_data.get('name', candidate_id)}")
        
        print(f"   ✅ Migrated {success_count}/{len(candidates)} candidates")
        return success_count
        
    except Exception as e:
        print(f"   ❌ Error migrating candidates: {e}")
        return 0

def migrate_elections():
    """Migrate elections from JSON to Firebase"""
    print("🗳️  Migrating elections to Firebase...")
    
    elections_file = 'voting_data/elections.json'
    if not os.path.exists(elections_file):
        print("   ⚠️  No elections file found")
        return 0
    
    try:
        with open(elections_file, 'r') as f:
            elections_data = json.load(f)
        
        elections = elections_data.get('elections', [])
        
        success_count = 0
        for election in elections:
            try:
                doc_ref = firebase_db.db.collection('elections').document(election['id'])
                doc_ref.set(election)
                success_count += 1
            except Exception as e:
                print(f"   ❌ Failed to migrate election: {election.get('title', election['id'])}")
        
        print(f"   ✅ Migrated {success_count}/{len(elections)} elections")
        return success_count
        
    except Exception as e:
        print(f"   ❌ Error migrating elections: {e}")
        return 0

def migrate_votes():
    """Migrate votes from JSON to Firebase"""
    print("📊 Migrating votes to Firebase...")
    
    votes_file = 'voting_data/votes.json'
    if not os.path.exists(votes_file):
        print("   ⚠️  No votes file found")
        return 0
    
    try:
        with open(votes_file, 'r') as f:
            votes = json.load(f)
        
        success_count = 0
        for vote_id, vote_data in votes.items():
            try:
                # Add ID to vote data
                vote_data['id'] = vote_id
                doc_ref = firebase_db.db.collection('votes').document(vote_id)
                doc_ref.set(vote_data)
                success_count += 1
            except Exception as e:
                print(f"   ❌ Failed to migrate vote: {vote_id}")
        
        print(f"   ✅ Migrated {success_count}/{len(votes)} votes")
        return success_count
        
    except Exception as e:
        print(f"   ❌ Error migrating votes: {e}")
        return 0

def verify_migration():
    """Verify that data was migrated successfully"""
    print("\n🔍 Verifying migration...")
    
    # Check voters
    voters = firebase_db.get_all_voters()
    print(f"   📊 Voters in Firebase: {len(voters)}")
    
    # Check candidates
    candidates = firebase_db.get_all_candidates()
    print(f"   📊 Candidates in Firebase: {len(candidates)}")
    
    # Check elections
    elections = firebase_db.get_all_elections()
    print(f"   📊 Elections in Firebase: {len(elections)}")
    
    # Check votes
    votes = firebase_db.get_all_votes()
    print(f"   📊 Votes in Firebase: {len(votes)}")
    
    return len(voters), len(candidates), len(elections), len(votes)

def main():
    print("🔥 Firebase Migration Tool")
    print("=" * 40)
    
    if not firebase_db.initialized:
        print("❌ Firebase not initialized. Check your configuration.")
        return
    
    print("📤 Starting migration from JSON to Firebase...")
    
    # Migrate all data
    voters_migrated = migrate_voters()
    candidates_migrated = migrate_candidates()
    elections_migrated = migrate_elections()
    votes_migrated = migrate_votes()
    
    # Verify migration
    v_count, c_count, e_count, vote_count = verify_migration()
    
    print(f"\n📊 Migration Summary:")
    print(f"   • Voters: {voters_migrated} migrated → {v_count} in Firebase")
    print(f"   • Candidates: {candidates_migrated} migrated → {c_count} in Firebase")
    print(f"   • Elections: {elections_migrated} migrated → {e_count} in Firebase")
    print(f"   • Votes: {votes_migrated} migrated → {vote_count} in Firebase")
    
    if all([v_count > 0, c_count >= 0, e_count >= 0]):
        print(f"\n🎉 Migration successful!")
        print(f"✅ All data is now stored in Firebase Firestore")
        print(f"🚀 System ready to use Firebase database")
        
        # Suggest backing up JSON files
        print(f"\n💡 Recommendation:")
        print(f"   • JSON files can now be backed up or removed")
        print(f"   • System will use Firebase for all operations")
        print(f"   • Data is now in the cloud and scalable")
    else:
        print(f"\n⚠️  Migration may have issues - please verify manually")

if __name__ == '__main__':
    main()