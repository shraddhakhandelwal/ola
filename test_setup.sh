#!/bin/bash

# Test Setup Script - Validates configuration and dependencies

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_test() {
    echo -e "${CYAN}Testing: ${1}${NC}"
}

print_pass() {
    echo -e "${GREEN}✓ PASS: ${1}${NC}"
}

print_fail() {
    echo -e "${RED}✗ FAIL: ${1}${NC}"
}

echo -e "${CYAN}${'='*60}${NC}"
echo -e "${GREEN}🧪 Testing Ride Automation Setup${NC}"
echo -e "${CYAN}${'='*60}${NC}"
echo ""

# Test 1: Python version
print_test "Python version (>=3.8 required)"
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION >= 3.8" | bc -l) )); then
    print_pass "Python $PYTHON_VERSION"
else
    print_fail "Python version $PYTHON_VERSION is too old"
    exit 1
fi

# Test 2: Virtual environment
print_test "Virtual environment"
if [ -d "venv" ]; then
    print_pass "Virtual environment exists"
else
    print_fail "Virtual environment not found. Run setup.sh first"
    exit 1
fi

# Test 3: Dependencies
print_test "Python dependencies"
source venv/bin/activate

REQUIRED_PACKAGES=("selenium" "schedule" "colorama" "requests" "webdriver_manager")
ALL_INSTALLED=true

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $package"
    else
        echo -e "  ${RED}✗${NC} $package"
        ALL_INSTALLED=false
    fi
done

if [ "$ALL_INSTALLED" = true ]; then
    print_pass "All required packages installed"
else
    print_fail "Some packages missing. Run: pip install -r requirements.txt"
    exit 1
fi

# Test 4: Configuration file
print_test "Configuration file"
if [ -f "config.json" ]; then
    if python3 -c "import json; json.load(open('config.json'))" 2>/dev/null; then
        print_pass "config.json is valid JSON"
        
        # Check required fields
        PICKUP=$(python3 -c "import json; print(json.load(open('config.json')).get('pickup_location', ''))")
        DROP=$(python3 -c "import json; print(json.load(open('config.json')).get('drop_location', ''))")
        
        if [ -n "$PICKUP" ] && [ -n "$DROP" ]; then
            print_pass "Route configured: $PICKUP → $DROP"
        else
            print_fail "Pickup or drop location not configured"
        fi
    else
        print_fail "config.json has invalid JSON"
        exit 1
    fi
else
    print_fail "config.json not found"
    exit 1
fi

# Test 5: Chrome/Chromium
print_test "Chrome/Chromium browser"
if command -v google-chrome &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version)
    print_pass "$CHROME_VERSION"
elif command -v chromium-browser &> /dev/null; then
    CHROME_VERSION=$(chromium-browser --version)
    print_pass "$CHROME_VERSION"
elif command -v chromium &> /dev/null; then
    CHROME_VERSION=$(chromium --version)
    print_pass "$CHROME_VERSION"
else
    print_fail "Chrome/Chromium not found"
    exit 1
fi

# Test 6: Directories
print_test "Required directories"
if [ -d "screenshots" ]; then
    print_pass "screenshots/ directory exists"
else
    mkdir -p screenshots
    print_pass "screenshots/ directory created"
fi

# Test 7: File permissions
print_test "Script permissions"
if [ -x "setup.sh" ]; then
    print_pass "setup.sh is executable"
else
    chmod +x setup.sh
    print_pass "Made setup.sh executable"
fi

# Test 8: Import test
print_test "Importing main modules"
if python3 -c "from enhanced_ride_automation import RideBookingAutomation; print('OK')" 2>/dev/null; then
    print_pass "Main module imports successfully"
else
    print_fail "Failed to import main module"
    exit 1
fi

echo ""
echo -e "${GREEN}${'='*60}${NC}"
echo -e "${GREEN}✅ All tests passed!${NC}"
echo -e "${GREEN}${'='*60}${NC}"
echo ""
echo -e "${CYAN}Ready to run:${NC}"
echo "  • One-time booking: python enhanced_ride_automation.py"
echo "  • Scheduled booking: python enhanced_scheduler.py"
echo ""
