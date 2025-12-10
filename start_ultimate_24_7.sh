#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 ULTIMATE 24/7 RIDE ACCEPTOR - START SCRIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

cd /workspaces/ola

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 STARTING ULTIMATE 24/7 RIDE ACCEPTOR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill any existing process
pkill -f "ultimate_24_7_ride_acceptor" || true
sleep 2

# Start the system in background
echo "🟢 Starting ultimate_24_7_ride_acceptor.py..."
nohup python3 -u ultimate_24_7_ride_acceptor.py > ultimate_24_7.log 2>&1 &
PROCESS_ID=$!
sleep 3

echo "✅ Process started with PID: $PROCESS_ID"
echo ""
echo "📊 SYSTEM STATUS:"
ps aux | grep "ultimate_24_7_ride_acceptor" | grep -v grep || echo "⚠️  Process not found"

echo ""
echo "📝 Live log (last 20 lines):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -20 ultimate_24_7.log || echo "Log file not created yet"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYSTEM IS NOW LIVE!"
echo ""
echo "🔔 You will get Telegram notifications every 2-3 minutes"
echo "📍 Each notification has ACCEPT button to open Ola app"
echo "📡 Rides are auto-saved to GitHub"
echo ""
echo "To check status: tail -f ultimate_24_7.log"
echo "To stop: pkill -f ultimate_24_7_ride_acceptor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
