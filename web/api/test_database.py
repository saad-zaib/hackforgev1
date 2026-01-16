#!/usr/bin/env python3
"""
Database Connection Test Script
Run this to verify MongoDB is working correctly
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent / "database"))

try:
    from database import get_db
    
    print("=" * 60)
    print("HACKFORGE DATABASE CONNECTION TEST")
    print("=" * 60)
    print()
    
    # Get database instance
    db = get_db()
    print("✓ Database manager initialized")
    
    # Test connection
    try:
        result = db.users.find_one()
        print("✓ MongoDB connection successful")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("\nPlease ensure MongoDB is running:")
        print("  sudo systemctl start mongod")
        sys.exit(1)
    
    # Get counts
    user_count = db.users.count_documents({})
    campaign_count = db.campaigns.count_documents({})
    progress_count = db.progress.count_documents({})
    
    print(f"\nDatabase Statistics:")
    print(f"  Users: {user_count}")
    print(f"  Campaigns: {campaign_count}")
    print(f"  Progress records: {progress_count}")
    
    # Test user creation
    print("\nTesting user operations...")
    test_user = db.get_user('user_default')
    if test_user:
        print(f"✓ Found user: {test_user['username']}")
    else:
        print("! Default user not found, creating...")
        user_data = {
            'user_id': 'user_default',
            'username': 'user_default',
            'email': 'user_default@hackforge.local',
            'role': 'student',
            'total_points': 0,
            'machines_solved': 0,
            'campaigns_completed': 0
        }
        db.create_user(user_data)
        print("✓ Default user created")
    
    # List campaigns
    print("\nCampaigns in database:")
    campaigns = list(db.campaigns.find())
    if campaigns:
        for i, camp in enumerate(campaigns, 1):
            print(f"  {i}. {camp.get('campaign_name', 'Unnamed')} (ID: {camp['campaign_id']})")
    else:
        print("  No campaigns found in database")
    
    print("\n" + "=" * 60)
    print("✓ Database test completed successfully!")
    print("=" * 60)
    
except ImportError as e:
    print(f"✗ Failed to import database module: {e}")
    print("\nMake sure you're in the correct directory:")
    print("  cd ~/hackforge/web/api")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
