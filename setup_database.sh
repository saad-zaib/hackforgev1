#!/bin/bash

echo "=========================================="
echo "Hackforge Database Setup"
echo "=========================================="
echo ""

# Check if MongoDB is installed
if command -v mongod &> /dev/null; then
    echo "✓ MongoDB is installed"
else
    echo "❌ MongoDB is not installed"
    echo ""
    echo "Install MongoDB:"
    echo "  Ubuntu/Debian: sudo apt install mongodb"
    echo "  macOS: brew install mongodb-community"
    echo "  Or use Docker: docker run -d -p 27017:27017 --name hackforge-mongo mongo:latest"
    exit 1
fi

# Check if MongoDB is running
if pgrep -x "mongod" > /dev/null; then
    echo "✓ MongoDB is running"
else
    echo "⚠️  MongoDB is not running"
    echo "Starting MongoDB..."
    
    # Try to start MongoDB
    if command -v systemctl &> /dev/null; then
        sudo systemctl start mongod
    elif command -v service &> /dev/null; then
        sudo service mongod start
    else
        echo "Please start MongoDB manually"
        exit 1
    fi
    
    sleep 2
fi

# Install Python dependencies
echo ""
echo "Installing Python database dependencies..."
pip3 install -r web/database_requirements.txt

# Test connection
echo ""
echo "Testing MongoDB connection..."
python3 << EOF
from pymongo import MongoClient

try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.server_info()
    print("✓ Successfully connected to MongoDB")
    
    # Create database and collections
    db = client['hackforge']
    
    # Create collections
    collections = ['users', 'campaigns', 'progress', 'flag_submissions', 
                   'hint_usage', 'achievements', 'user_achievements', 'sessions']
    
    for coll in collections:
        if coll not in db.list_collection_names():
            db.create_collection(coll)
            print(f"  ✓ Created collection: {coll}")
        else:
            print(f"  ✓ Collection exists: {coll}")
    
    print("")
    print("✓ Database setup complete!")
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    print("")
    print("Make sure MongoDB is running:")
    print("  sudo systemctl start mongodb")
    print("  OR")
    print("  docker run -d -p 27017:27017 mongo:latest")
    exit(1)
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "MongoDB is ready at: mongodb://localhost:27017/"
echo "Database name: hackforge"
echo ""
echo "Start the API with database:"
echo "  python3 web/api/main_with_db.py"
echo ""
