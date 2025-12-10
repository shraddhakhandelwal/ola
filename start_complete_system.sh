#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 START COMPLETE SYSTEM - 24/7 with Auto-Recovery
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

cd /workspaces/ola

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🎯 ULTIMATE 24/7 RIDE NOTIFIER WITH AUTO-RECOVERY          ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f ultimate_24_7_ride_acceptor || true
pkill -f keep_alive_monitor || true
sleep 2

# Start the main notification system
echo "🟢 Starting notification system..."
nohup python3 -u ultimate_24_7_ride_acceptor.py > ultimate_24_7.log 2>&1 &
MAIN_PID=$!
sleep 3

# Start the keep-alive monitor
echo "🛡️ Starting keep-alive monitor..."
nohup bash keep_alive_monitor.sh > keep_alive_monitor.log 2>&1 &
MONITOR_PID=$!
sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYSTEM STARTED SUCCESSFULLY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 RUNNING PROCESSES:"
echo ""
echo "1️⃣  Notification System:"
ps aux | grep "ultimate_24_7_ride_acceptor" | grep -v grep | awk '{print "   PID: " $2 ", Memory: " $6 " KB"}'
echo ""
echo "2️⃣  Keep-Alive Monitor:"
ps aux | grep "keep_alive_monitor" | grep -v grep | awk '{print "   PID: " $2 ", Memory: " $6 " KB"}'
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 24/7 OPERATION ACTIVE"
echo ""
echo "Features:"
echo "  ✓ Notifications every 2-3 minutes"
echo "  ✓ Auto-restart if process crashes"
echo "  ✓ Auto-start on container boot"
echo "  ✓ Auto-push to GitHub"
echo "  ✓ IST timezone (India Standard Time)"
echo ""
echo "📝 View logs:"
echo "  Main system:    tail -f ultimate_24_7.log"
echo "  Keep-alive:     tail -f keep_alive_monitor.log"
echo ""
echo "🛑 Stop everything:"
echo "  pkill -f ultimate_24_7_ride_acceptor"
echo "  pkill -f keep_alive_monitor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔔 Check your Telegram - notifications starting now!"
echo ""
