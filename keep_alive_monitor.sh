#!/bin/bash

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛡️ KEEP ALIVE MONITOR - Ensures System Never Stops
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# This script runs continuously and automatically restarts the
# notification system if it crashes or stops for any reason.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd /workspaces/ola

echo "🛡️ Starting Keep-Alive Monitor..."
echo "Monitoring: ultimate_24_7_ride_acceptor.py"
echo "Checking every 60 seconds..."
echo ""

while true; do
    # Check if process is running
    if ! ps aux | grep "ultimate_24_7_ride_acceptor.py" | grep -v grep > /dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S IST')] ⚠️  Process not running! Restarting..."
        
        # Kill any zombie processes
        pkill -f ultimate_24_7_ride_acceptor || true
        sleep 2
        
        # Restart the system
        nohup python3 -u ultimate_24_7_ride_acceptor.py > ultimate_24_7.log 2>&1 &
        NEW_PID=$!
        
        echo "[$(date '+%Y-%m-%d %H:%M:%S IST')] ✅ Restarted with PID: $NEW_PID"
        
        # Log to file
        echo "[$(date '+%Y-%m-%d %H:%M:%S IST')] Auto-restarted by keep-alive monitor" >> keep_alive.log
        
        sleep 10
    else
        # Process is running - just update status
        PID=$(ps aux | grep "ultimate_24_7_ride_acceptor.py" | grep -v grep | awk '{print $2}')
        echo "[$(date '+%Y-%m-%d %H:%M:%S IST')] ✅ System healthy - PID: $PID"
    fi
    
    # Wait 60 seconds before next check
    sleep 60
done
