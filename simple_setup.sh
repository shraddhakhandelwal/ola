#!/bin/bash

# Simple Setup Script for Auto Ride Booking
# Books ride automatically so it's ready when you open Ola/Uber app

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     AUTO RIDE BOOKING SETUP - Pune → Mumbai                    ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Install Python packages
echo "📦 Step 1: Installing required packages..."
pip3 install selenium webdriver-manager schedule --quiet
echo "✓ Packages installed"
echo ""

# Step 2: Configure your details
echo "⚙️  Step 2: Configure your details"
echo ""
echo "Current configuration:"
echo "  Pickup:  Pune Railway Station, Pune"
echo "  Dropoff: Mumbai Central, Mumbai"
echo "  Time:    7:30 AM (books 30 min before you need it)"
echo ""

read -p "Is this correct? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo ""
    echo "Edit the file: auto_book_ride.py"
    echo "Change these lines in CONFIG section:"
    echo "  phone_number: Your phone number"
    echo "  pickup: Your pickup location"
    echo "  dropoff: Your dropoff location"
    echo "  booking_time: What time to book (e.g., '07:30')"
    echo ""
fi

# Step 3: Test
echo ""
echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HOW TO USE:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Option 1: Book ride RIGHT NOW (test it)"
echo "  Command: python3 auto_book_ride.py 1"
echo "  Result:  Ride booked in 1-2 min, open app to see it"
echo ""
echo "Option 2: Setup DAILY auto-booking"
echo "  Command: python3 auto_book_ride.py 2"
echo "  Result:  Runs in background, books at 7:30 AM daily"
echo "           When you open app at 8 AM, ride is already there!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Try it now:"
echo "   python3 auto_book_ride.py 1"
echo ""
