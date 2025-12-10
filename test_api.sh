#!/bin/bash

# Quick test script for Ola API integration

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}  Testing Ola API Integration${NC}"
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment not found. Run ./setup.sh first${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from credentials...${NC}"
    cat > .env << 'EOF'
OLA_PROJECT_ID=7387ed63-a1f3-4601-bba3-a659a56c912d
OLA_API_KEY=1um4WEKl6rLA7dpkq1HkLYGxoEdJi0xXtn5sQa4S
EOF
    echo -e "${GREEN}✓ .env file created with API credentials${NC}"
fi

echo ""
echo -e "${CYAN}Your Ola API Configuration:${NC}"
echo -e "  Project ID: 7387ed63-a1f3-4601-bba3-a659a56c912d"
echo -e "  API Key: 1um4WEKl6rLA*********************"
echo ""

# Check Python dependencies
echo -e "${CYAN}Checking dependencies...${NC}"
python3 -c "import requests; import colorama; print('✓ All required packages installed')" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Installing missing packages...${NC}"
    pip install requests colorama python-dotenv
}

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}  Ready to test API booking!${NC}"
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo ""
echo -e "${CYAN}Run this command to test:${NC}"
echo -e "  python ola_api_automation.py"
echo ""
echo -e "${YELLOW}Note: This will attempt to book a real ride using the API${NC}"
echo -e "${YELLOW}Make sure your config.json has correct pickup/drop locations${NC}"
echo ""
