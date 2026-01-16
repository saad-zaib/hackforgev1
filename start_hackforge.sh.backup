#!/bin/bash

# Hackforge Unified Startup Script
# Starts all components in the correct order

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              HACKFORGE PLATFORM STARTUP                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if MongoDB is running
check_mongodb() {
    echo -e "${YELLOW}[1/4] Checking MongoDB...${NC}"
    
    if pgrep -x "mongod" > /dev/null; then
        echo -e "${GREEN}✓ MongoDB is running${NC}"
        return 0
    else
        echo -e "${YELLOW}MongoDB not running. Starting...${NC}"
        
        # Try to start MongoDB
        if command -v systemctl &> /dev/null; then
            sudo systemctl start mongod
            sleep 2
            echo -e "${GREEN}✓ MongoDB started${NC}"
        else
            echo -e "${RED}❌ Could not start MongoDB automatically${NC}"
            echo "Please start MongoDB manually or use Docker:"
            echo "  docker-compose -f docker-compose.mongodb.yml up -d"
            exit 1
        fi
    fi
}

# Start API with Database
start_api() {
    echo -e "\n${YELLOW}[2/4] Starting API Server...${NC}"
    
    # Kill existing API process if running
    pkill -f "main_with_db.py" 2>/dev/null || true
    
    cd "$SCRIPT_DIR/web/api"
    python3 main_with_db.py > "$SCRIPT_DIR/logs/api.log" 2>&1 &
    API_PID=$!
    
    echo $API_PID > "$SCRIPT_DIR/.api.pid"
    
    # Wait for API to start
    sleep 3
    
    if ps -p $API_PID > /dev/null; then
        echo -e "${GREEN}✓ API started (PID: $API_PID)${NC}"
        echo "  URL: http://localhost:8000"
        echo "  Docs: http://localhost:8000/docs"
    else
        echo -e "${RED}❌ API failed to start. Check logs/api.log${NC}"
        exit 1
    fi
}

# Start Frontend
start_frontend() {
    echo -e "\n${YELLOW}[3/4] Starting React Frontend...${NC}"
    
    if [ ! -d "$SCRIPT_DIR/web/frontend/node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        cd "$SCRIPT_DIR/web/frontend"
        npm install > "$SCRIPT_DIR/logs/npm-install.log" 2>&1
    fi
    
    cd "$SCRIPT_DIR/web/frontend"
    
    # Kill existing frontend process
    pkill -f "react-scripts start" 2>/dev/null || true
    
    # Start frontend in background
    BROWSER=none npm start > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    
    echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"
    
    # Wait for frontend to start
    echo "Waiting for frontend to compile..."
    sleep 10
    
    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
        echo "  URL: http://localhost:3000"
    else
        echo -e "${RED}❌ Frontend failed to start. Check logs/frontend.log${NC}"
        exit 1
    fi
}

# Start Docker Machines (optional)
start_docker() {
    echo -e "\n${YELLOW}[4/4] Docker Machines...${NC}"
    
    if [ -d "$SCRIPT_DIR/core/generated_machines" ]; then
        read -p "Start Docker machines now? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$SCRIPT_DIR/core/generated_machines"
            
            if [ -f "docker-compose.yml" ]; then
                docker-compose up -d --build
                echo -e "${GREEN}✓ Docker machines started${NC}"
            else
                echo -e "${YELLOW}⚠️  No docker-compose.yml found${NC}"
                echo "Generate machines first: ./hackforge generate"
            fi
        else
            echo "Skipping Docker machines. Start later with: ./hackforge start"
        fi
    else
        echo -e "${YELLOW}⚠️  No machines generated yet${NC}"
        echo "Generate machines first: ./hackforge generate"
    fi
}

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Main startup sequence
main() {
    check_mongodb
    start_api
    start_frontend
    start_docker
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              HACKFORGE IS NOW RUNNING!                    ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}Services:${NC}"
    echo "  • Frontend:  http://localhost:3000"
    echo "  • API:       http://localhost:8000"
    echo "  • API Docs:  http://localhost:8000/docs"
    echo "  • MongoDB:   mongodb://localhost:27017"
    echo ""
    echo -e "${YELLOW}Logs:${NC}"
    echo "  • API:       tail -f logs/api.log"
    echo "  • Frontend:  tail -f logs/frontend.log"
    echo ""
    echo -e "${YELLOW}Management:${NC}"
    echo "  • Stop all:  ./stop_hackforge.sh"
    echo "  • Status:    ./hackforge status"
    echo ""
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}Use ./stop_hackforge.sh to stop all services${NC}"; exit 0' INT

main
