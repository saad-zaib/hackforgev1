#!/bin/bash

# Hackforge Test Runner - Enhanced

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              HACKFORGE TEST RUNNER                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check services
check_services() {
    echo "Checking required services..."
    echo ""
    
    # MongoDB
    if pgrep -x "mongod" > /dev/null; then
        echo -e "${GREEN}✓${NC} MongoDB is running"
    else
        echo -e "${YELLOW}⚠${NC} MongoDB is not running (database tests will be skipped)"
    fi
    
    # API
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} API is running"
    else
        echo -e "${RED}✗${NC} API is not running"
        echo "  Start with: python3 web/api/main_with_db.py"
        echo ""
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Docker
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker is available"
    else
        echo -e "${RED}✗${NC} Docker is not available"
    fi
    
    echo ""
}

# Run specific component tests
run_component() {
    case $1 in
        1|core)
            echo "Running Component 1: Core Generation Tests..."
            python3 tests/test_suite.py TestComponent1_CoreGeneration -v
            ;;
        2|template)
            echo "Running Component 2: Template Engine Tests..."
            python3 tests/test_suite.py TestComponent2_TemplateEngine -v
            ;;
        3|docker)
            echo "Running Component 3: Docker Orchestrator Tests..."
            python3 tests/test_suite.py TestComponent3_DockerOrchestrator -v
            ;;
        4|api)
            echo "Running Component 4: API Tests..."
            python3 tests/test_suite.py TestComponent4_API -v
            ;;
        6|database|db)
            echo "Running Component 6: Database Tests..."
            python3 tests/test_suite.py TestComponent6_Database -v
            ;;
        7|integration|e2e)
            echo "Running Component 7: Integration Tests..."
            python3 tests/test_suite.py TestComponent7_Integration -v
            ;;
        all)
            echo "Running ALL tests..."
            python3 tests/test_suite.py
            ;;
        quick)
            echo "Running quick smoke tests..."
            python3 tests/test_suite.py TestComponentStatus -v
            ;;
        *)
            echo "Unknown test category: $1"
            echo ""
            echo "Available options:"
            echo "  1, core       - Core generation tests"
            echo "  2, template   - Template engine tests"
            echo "  3, docker     - Docker orchestrator tests"
            echo "  4, api        - API tests"
            echo "  6, database   - Database tests"
            echo "  7, integration - Integration tests"
            echo "  all           - Run all tests"
            echo "  quick         - Quick smoke tests"
            exit 1
            ;;
    esac
}

# Performance benchmark
benchmark() {
    echo "Running performance benchmarks..."
    echo ""
    
    echo "1. Campaign Generation Speed"
    time python3 -c "
import sys
sys.path.append('core')
from generator import HackforgeGenerator
g = HackforgeGenerator()
machines = g.generate_campaign('bench_user', 2, 2)
print(f'Generated {len(machines)} machines')
"
    
    echo ""
    echo "2. Template Rendering Speed"
    time python3 -c "
import sys
sys.path.append('core')
from generator import HackforgeGenerator
from template_engine import TemplateEngine
g = HackforgeGenerator()
t = TemplateEngine('tests/bench_output')
machines = g.generate_campaign('bench_user', 2, 2)
for m in machines:
    t.generate_machine_app(m)
print('Rendered all templates')
"
    
    echo ""
    rm -rf tests/bench_output
}

# Coverage report
coverage_report() {
    echo "Generating code coverage report..."
    
    if ! command -v coverage &> /dev/null; then
        echo "Installing coverage..."
        pip3 install coverage
    fi
    
    coverage run tests/test_suite.py
    coverage report
    coverage html
    
    echo ""
    echo "Coverage report generated: htmlcov/index.html"
}

# Main
if [ $# -eq 0 ]; then
    check_services
    echo "Running all tests..."
    python3 tests/test_suite.py
elif [ "$1" == "benchmark" ]; then
    benchmark
elif [ "$1" == "coverage" ]; then
    coverage_report
elif [ "$1" == "watch" ]; then
    echo "Running tests in watch mode..."
    while true; do
        clear
        python3 tests/test_suite.py TestComponentStatus -v
        echo ""
        echo "Watching for changes... (Ctrl+C to stop)"
        sleep 5
    done
else
    check_services
    run_component $1
fi
