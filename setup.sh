#!/bin/bash

# Ola/Uber Ride Automation - Complete Setup Script
# This script automates the entire installation process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${CYAN}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

print_header() {
    echo -e "${CYAN}${'='*60}${NC}"
    echo -e "${GREEN}${1}${NC}"
    echo -e "${CYAN}${'='*60}${NC}"
}

# Main setup
main() {
    print_header "🚗 Ola/Uber Ride Automation - Complete Setup"
    echo ""
    
    # Step 1: Check Python
    print_info "Step 1/7: Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
    echo ""
    
    # Step 2: Check Chrome
    print_info "Step 2/7: Checking Google Chrome..."
    if command -v google-chrome &> /dev/null || command -v chromium &> /dev/null || command -v chromium-browser &> /dev/null; then
        print_success "Chrome/Chromium found"
    else
        print_warning "Chrome not found. Installing..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update
            sudo apt-get install -y chromium-browser
            print_success "Chromium installed"
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            print_warning "Please install Google Chrome manually from https://www.google.com/chrome/"
        fi
    fi
    echo ""
    
    # Step 3: Create virtual environment
    print_info "Step 3/7: Creating virtual environment..."
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Skipping..."
    else
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    echo ""
    
    # Step 4: Activate and install dependencies
    print_info "Step 4/7: Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "All dependencies installed"
    echo ""
    
    # Step 5: Create necessary directories
    print_info "Step 5/7: Creating project directories..."
    mkdir -p screenshots
    mkdir -p logs
    print_success "Directories created"
    echo ""
    
    # Step 6: Setup configuration
    print_info "Step 6/7: Setting up configuration..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_success ".env file created"
        print_warning "Please edit .env file with your credentials"
    else
        print_warning ".env file already exists"
    fi
    
    if [ -f "config.json" ]; then
        print_success "config.json already exists"
    else
        print_warning "Please ensure config.json has your route details"
    fi
    echo ""
    
    # Step 7: Test installation
    print_info "Step 7/7: Testing installation..."
    python3 -c "import selenium; import schedule; import colorama; print('All imports successful')"
    print_success "Installation test passed"
    echo ""
    
    # Display next steps
    print_header "✅ Setup Complete!"
    echo ""
    print_info "Next Steps:"
    echo "  1. Edit config.json with your pickup/drop locations"
    echo "  2. Edit .env with your credentials (optional)"
    echo "  3. Test the setup: ./test_setup.sh"
    echo "  4. Run one-time booking: python enhanced_ride_automation.py"
    echo "  5. Start scheduler: python enhanced_scheduler.py"
    echo ""
    print_info "To activate virtual environment:"
    echo "  source venv/bin/activate"
    echo ""
    print_success "Happy Automated Commuting! 🚗💨"
    echo ""
}

# Run main function
main
