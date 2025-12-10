#!/bin/bash

# Quick Start Script - Run this to get started quickly

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}${'='*70}${NC}"
echo -e "${GREEN}🚗 Ola/Uber Ride Automation - Quick Start${NC}"
echo -e "${CYAN}${'='*70}${NC}"
echo ""

# Check if setup is done
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  First time setup required${NC}"
    echo ""
    echo "Running setup script..."
    chmod +x setup.sh
    ./setup.sh
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Show menu
echo -e "${CYAN}Choose an option:${NC}"
echo ""
echo "  1) Test setup and configuration"
echo "  2) Book a ride now (one-time)"
echo "  3) Start daily scheduler"
echo "  4) View configuration"
echo "  5) Edit configuration"
echo "  6) Install as system service (Linux)"
echo "  7) Exit"
echo ""

read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        echo ""
        echo -e "${CYAN}Running tests...${NC}"
        chmod +x test_setup.sh
        ./test_setup.sh
        ;;
    2)
        echo ""
        echo -e "${CYAN}Starting one-time booking...${NC}"
        python enhanced_ride_automation.py
        ;;
    3)
        echo ""
        echo -e "${CYAN}Starting scheduler...${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        python enhanced_scheduler.py
        ;;
    4)
        echo ""
        echo -e "${CYAN}Current Configuration:${NC}"
        cat config.json | python -m json.tool
        ;;
    5)
        echo ""
        echo -e "${CYAN}Opening configuration editor...${NC}"
        ${EDITOR:-nano} config.json
        ;;
    6)
        echo ""
        echo -e "${CYAN}Installing system service...${NC}"
        
        # Replace %USER% with current user
        sed "s/%USER%/$USER/g" ride-automation.service > /tmp/ride-automation.service
        
        sudo cp /tmp/ride-automation.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable ride-automation.service
        sudo systemctl start ride-automation.service
        
        echo -e "${GREEN}✓ Service installed and started${NC}"
        echo ""
        echo "Service commands:"
        echo "  • Status: sudo systemctl status ride-automation"
        echo "  • Stop:   sudo systemctl stop ride-automation"
        echo "  • Start:  sudo systemctl start ride-automation"
        echo "  • Logs:   sudo journalctl -u ride-automation -f"
        ;;
    7)
        echo ""
        echo -e "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${YELLOW}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
echo ""
