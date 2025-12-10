#!/bin/bash

# Setup for Ola/Uber Driver - Auto Ride Acceptor
# Automatically accepts ride requests when you're online

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     DRIVER AUTO RIDE ACCEPTOR - SETUP                          ║"
echo "║     For Ola & Uber Drivers                                     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Install packages
echo "📦 Installing required packages..."
pip3 install selenium webdriver-manager --quiet
echo "✓ Packages installed"
echo ""

# Configure
echo "⚙️  Configuration"
echo ""
echo "Edit driver_auto_accept.py to set:"
echo "  - Your driver phone number"
echo "  - Preferred route (e.g., 'Pune to Mumbai')"
echo "  - Minimum fare you want to accept"
echo "  - Auto-accept on/off"
echo ""

read -p "Press Enter to continue..."
echo ""

echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HOW TO USE (FOR DRIVERS):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "For Ola Drivers:"
echo "  python3 driver_auto_accept.py 1"
echo ""
echo "For Uber Drivers:"
echo "  python3 driver_auto_accept.py 2"
echo ""
echo "What happens:"
echo "  1. Opens driver app in browser"
echo "  2. You login with OTP (one time)"
echo "  3. Sets you online/available"
echo "  4. Automatically accepts ride requests"
echo "  5. Prefers Pune-Mumbai rides (if configured)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 TIP: Keep this running while driving to auto-accept rides!"
echo ""
