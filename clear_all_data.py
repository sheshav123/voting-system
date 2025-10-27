#!/usr/bin/env python3
"""
Clear All Application Data
This script completely resets the voting system database
"""

import os
import json
import shutil
from datetime import datetime

def clear_all_data():
    print("🗑️  Clearing All Application Data")
    print("=" * 40)
    
    # Data directory and files
    data_dir = 'voting_data'
    data_files = [
        'voters.json',
        'candidates.json', 
        'votes.json',
        'elections.json',
        'otps.json',
        'fast2sms_otps.json',
        'firebase_rate_limits.json'
    ]
    
    # Upload directory
    upload_dir = 'static/uploads'
    
    cleared_count = 0
    
    # Clear JSON data files
    print("📄 Clearing data files...")
    for filename in data_files:
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            try:
                if filename == 'elections.json':
                    # Reset elections with proper structure
                    empty_data = {
                        'current_election': None,
                        'elections': []
                    }
                else:
                    # Empty object for other files
                    empty_data = {}
                
                with open(filepath, 'w') as f:
                    json.dump(empty_data, f, indent=2)
                
                print(f"   ✅ Cleared: {filename}")
                cleared_count += 1
                
            except Exception as e:
                print(f"   ❌ Error clearing {filename}: {e}")
        else:
            print(f"   ⚠️  Not found: {filename}")
    
    # Clear uploaded files (voter photos)
    print(f"\n📷 Clearing uploaded files...")
    if os.path.exists(upload_dir):
        try:
            file_count = 0
            for filename in os.listdir(upload_dir):
                if filename.startswith('voter_'):
                    filepath = os.path.join(upload_dir, filename)
                    os.remove(filepath)
                    file_count += 1
            
            if file_count > 0:
                print(f"   ✅ Deleted {file_count} voter photos")
            else:
                print(f"   ℹ️  No voter photos to delete")
                
        except Exception as e:
            print(f"   ❌ Error clearing uploads: {e}")
    else:
        print(f"   ℹ️  Upload directory doesn't exist")
    
    # Create backup timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n📊 Summary:")
    print(f"   • Data files cleared: {cleared_count}")
    print(f"   • Timestamp: {timestamp}")
    print(f"   • All voters removed")
    print(f"   • All candidates removed") 
    print(f"   • All elections removed")
    print(f"   • All votes removed")
    print(f"   • All OTP records removed")
    print(f"   • All uploaded photos removed")
    
    print(f"\n✅ Database completely reset!")
    print(f"🚀 Application ready for fresh start")

def verify_clear():
    """Verify that all data has been cleared"""
    print(f"\n🔍 Verifying data clearance...")
    
    data_dir = 'voting_data'
    data_files = ['voters.json', 'candidates.json', 'votes.json', 'elections.json']
    
    all_clear = True
    
    for filename in data_files:
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if filename == 'elections.json':
                    if data.get('current_election') is None and len(data.get('elections', [])) == 0:
                        print(f"   ✅ {filename}: Empty")
                    else:
                        print(f"   ❌ {filename}: Still has data")
                        all_clear = False
                else:
                    if len(data) == 0:
                        print(f"   ✅ {filename}: Empty")
                    else:
                        print(f"   ❌ {filename}: Still has {len(data)} records")
                        all_clear = False
                        
            except Exception as e:
                print(f"   ❌ Error reading {filename}: {e}")
                all_clear = False
    
    if all_clear:
        print(f"\n🎉 Verification successful - all data cleared!")
    else:
        print(f"\n⚠️  Some data may not have been cleared properly")
    
    return all_clear

if __name__ == '__main__':
    print("⚠️  WARNING: This will permanently delete ALL application data!")
    print("   • All voters will be removed")
    print("   • All candidates will be removed") 
    print("   • All elections will be removed")
    print("   • All votes will be removed")
    print("   • All uploaded photos will be removed")
    
    confirm = input("\nAre you sure you want to continue? (type 'YES' to confirm): ")
    
    if confirm == 'YES':
        clear_all_data()
        verify_clear()
        
        print(f"\n🔄 Next steps:")
        print(f"   1. Restart the application")
        print(f"   2. Add new voters via admin panel")
        print(f"   3. Create new elections")
        print(f"   4. Add candidates")
        
    else:
        print("❌ Operation cancelled - no data was cleared")