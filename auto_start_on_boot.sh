#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 AUTO-START ON BOOT - Ultimate 24/7 Ride Acceptor
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# This script automatically starts the notification system when
# the dev container boots up. Ensures 24/7 operation.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Wait for system to stabilize
sleep 5

cd /workspaces/ola

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 AUTO-STARTING 24/7 RIDE NOTIFICATION SYSTEM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill any existing process
pkill -f ultimate_24_7_ride_acceptor || true
sleep 2

# Start the system
echo "🟢 Starting ultimate_24_7_ride_acceptor.py..."
nohup python3 -u ultimate_24_7_ride_acceptor.py > ultimate_24_7.log 2>&1 &
PROCESS_ID=$!
sleep 3

echo "✅ Process started with PID: $PROCESS_ID"
echo ""
echo "📊 STATUS:"
ps aux | grep "ultimate_24_7_ride_acceptor" | grep -v grep || echo "⚠️  Process not found"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 24/7 NOTIFICATION SYSTEM IS NOW LIVE!"
echo "🔔 Notifications will arrive every 2-3 minutes"
echo "📡 Auto-pushing to GitHub on each notification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
