#!/bin/bash
# Quick status check for 24/7 ride notification system

echo ""
echo "======================================================================"
echo "📊 24/7 RIDE NOTIFICATION SYSTEM - STATUS CHECK"
echo "======================================================================"
echo ""

# Check if system is running
if pgrep -f "always_on_ride_notifier" > /dev/null; then
    echo "✅ System Status: RUNNING"
    echo "🔄 Process ID: $(pgrep -f always_on_ride_notifier)"
else
    echo "❌ System Status: STOPPED"
    echo "⚠️  Run this to restart: cd /workspaces/ola && nohup python3 -u always_on_ride_notifier.py > always_on.log 2>&1 &"
    exit 1
fi

echo ""
echo "----------------------------------------------------------------------"
echo "📬 RECENT NOTIFICATIONS:"
echo "----------------------------------------------------------------------"
tail -5 /workspaces/ola/always_on_notifier.log 2>/dev/null || echo "No logs yet"

echo ""
echo "----------------------------------------------------------------------"
echo "⏰ SYSTEM OUTPUT (Last 10 lines):"
echo "----------------------------------------------------------------------"
tail -10 /workspaces/ola/always_on.log 2>/dev/null || echo "No output yet"

echo ""
echo "----------------------------------------------------------------------"
echo "💡 QUICK ACTIONS:"
echo "----------------------------------------------------------------------"
echo "  View all logs:     tail -f /workspaces/ola/always_on_notifier.log"
echo "  Stop system:       pkill -f always_on_ride_notifier"
echo "  Restart system:    cd /workspaces/ola && nohup python3 -u always_on_ride_notifier.py > always_on.log 2>&1 &"
echo "  Check status:      bash /workspaces/ola/check_status.sh"
echo ""
echo "======================================================================"
echo "✅ YOUR SYSTEM IS RUNNING 24/7 - NOTIFICATIONS EVERY 5 MINUTES!"
echo "======================================================================"
echo ""
