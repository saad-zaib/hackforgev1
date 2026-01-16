#!/bin/bash
# Stop all Hackforge services
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           STOPPING HACKFORGE SERVICES                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Stop API
echo -e "${YELLOW}Stopping API...${NC}"
if [ -f ".api.pid" ]; then
    API_PID=$(cat .api.pid)
    if ps -p $API_PID > /dev/null; then
        kill $API_PID 2>/dev/null
        echo -e "${GREEN}✓ API stopped (PID: $API_PID)${NC}"
    fi
    rm .api.pid
fi

# Kill by port and process name
lsof -ti:8000 | xargs kill -9 2>/dev/null && echo -e "${GREEN}✓ Killed processes on port 8000${NC}" || true
pkill -9 -f "main_with_db.py" 2>/dev/null || true

# Stop Frontend
echo -e "${YELLOW}Stopping Frontend...${NC}"
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✓ Frontend stopped (PID: $FRONTEND_PID)${NC}"
    fi
    rm .frontend.pid
fi

# Kill by port (most reliable for React)
if lsof -ti:3000 >/dev/null 2>&1; then
    echo -e "${YELLOW}Killing processes on port 3000...${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ Port 3000 freed${NC}"
fi

# Kill by process name
pkill -9 -f "react-scripts start" 2>/dev/null || true
pkill -9 -f "node.*frontend" 2>/dev/null || true

# Wait for port to be fully released
sleep 1

# Verify port is free
if lsof -ti:3000 >/dev/null 2>&1; then
    echo -e "${RED}⚠️  Warning: Port 3000 still in use${NC}"
    echo "Run: lsof -ti:3000 | xargs kill -9"
else
    echo -e "${GREEN}✓ Frontend completely stopped${NC}"
fi

# Stop Docker machines
echo -e "${YELLOW}Stopping Docker machines...${NC}"
if [ -d "docker/orchestrator" ]; then
    cd docker/orchestrator
    python3 orchestrator.py stop 2>/dev/null && echo -e "${GREEN}✓ Docker machines stopped${NC}" || true
    cd "$SCRIPT_DIR"
elif [ -d "core/generated_machines" ]; then
    cd core/generated_machines
    docker-compose down 2>/dev/null && echo -e "${GREEN}✓ Docker machines stopped${NC}" || true
    cd "$SCRIPT_DIR"
fi

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
