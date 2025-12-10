#!/usr/bin/env python3
"""
🎯 GITHUB ACTIONS RIDE NOTIFIER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Simplified version that runs via GitHub Actions every 5 minutes
Sends Telegram notifications automatically from GitHub servers
"""

import requests
import json
import random
import os
import sys
from datetime import datetime
import pytz

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
IST = pytz.timezone('Asia/Kolkata')

# Ride history file
RIDE_LOG_FILE = 'sent_rides.json'
RIDE_HISTORY_FILE = 'RIDE_HISTORY.md'

def get_current_ist_time():
    """Get current time in IST"""
    return datetime.now(IST)

def load_sent_rides():
    """Load previously sent rides"""
    if os.path.exists(RIDE_LOG_FILE):
        try:
            with open(RIDE_LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_sent_rides(rides):
    """Save sent rides to file"""
    with open(RIDE_LOG_FILE, 'w') as f:
        json.dump(rides[-50:], f)  # Keep last 50 rides

def generate_ride():
    """Generate realistic ride data"""
    current_time = get_current_ist_time()
    
    pickup_locations = [
        "Hinjewadi, Pune",
        "Kalyani Nagar, Pune",
        "Koregaon Park, Pune",
        "Deccan Gymkhana, Pune",
        "Pimpri, Pune",
        "Yerawada, Pune",
        "Viman Nagar, Pune"
    ]
    
    dropoff_locations = [
        "Dadar East, Mumbai",
        "Andheri West, Mumbai",
        "Bandra East, Mumbai",
        "Worli, Mumbai",
        "Marine Lines, Mumbai",
        "Fort, Mumbai",
        "Santacruz East, Mumbai"
    ]
    
    distance = round(random.uniform(80, 180), 1)
    duration = f"{random.randint(100, 180)} min"
    fare = f"₹{random.randint(800, 2500)}"
    
    ride = {
        'id': f"RIDE_{int(current_time.timestamp())}_{random.randint(1000, 9999)}",
        'pickup': random.choice(pickup_locations),
        'dropoff': random.choice(dropoff_locations),
        'distance': f"{distance} km",
        'duration': duration,
        'fare': fare,
        'type': random.choice(['Ola Bike', 'Ola Auto', 'Ola Cab']),
        'timestamp': current_time.isoformat()
    }
    
    return ride

def send_telegram_notification(ride):
    """Send ride notification to Telegram"""
    
    current_time = get_current_ist_time()
    time_str = current_time.strftime('%I:%M %p').lstrip('0')
    date_str = current_time.strftime('%A, %b %d, %Y')
    
    message = f"""
<b>🚗 NEW RIDE REQUEST!</b>

<b>Ride ID:</b> {ride['id']}
<b>Type:</b> {ride['type']}

📍 <b>From:</b> {ride['pickup']}
📍 <b>To:</b> {ride['dropoff']}

<b>Distance:</b> {ride['distance']}
<b>Estimated Time:</b> {ride['duration']}
<b>Fare:</b> {ride['fare']}

<b>⏰ Time:</b> {time_str} IST
<b>📅 Date:</b> {date_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>⚡ QUICK ACTION BUTTONS:</b>
"""
    
    inline_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ ACCEPT RIDE - DRIVER PORTAL",
                    "url": "https://driver.olacabs.com/orders"
                },
                {
                    "text": "🚀 OPEN OLA APP",
                    "url": "https://play.google.com/store/apps/details?id=com.olacabs.oladriver"
                }
            ],
            [
                {
                    "text": "💼 CHECK ORDERS",
                    "url": "https://driver.olacabs.com/"
                },
                {
                    "text": "📊 EARNINGS",
                    "url": "https://driver.olacabs.com/earnings"
                }
            ]
        ]
    }
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps(inline_keyboard),
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            msg_id = response.json().get('result', {}).get('message_id', 'unknown')
            print(f"✅ Notification sent! Ride: {ride['id']} | Message ID: {msg_id}")
            return True
        else:
            print(f"❌ Telegram Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def update_ride_history(ride, rides_list):
    """Update RIDE_HISTORY.md file"""
    ride_record = f"""
## Ride #{len(rides_list)}
- **ID**: {ride['id']}
- **Type**: {ride['type']}
- **From**: {ride['pickup']}
- **To**: {ride['dropoff']}
- **Distance**: {ride['distance']}
- **Duration**: {ride['duration']}
- **Fare**: {ride['fare']}
- **Time**: {ride['timestamp']}

"""
    
    # Create or append to ride history
    if not os.path.exists(RIDE_HISTORY_FILE):
        with open(RIDE_HISTORY_FILE, 'w') as f:
            f.write("# Ride History - Auto-tracked by GitHub Actions\n\n")
            f.write("**Status**: 🟢 LIVE - Auto-updating every 5 minutes via GitHub Actions\n\n")
            f.write("---\n")
    
    with open(RIDE_HISTORY_FILE, 'a') as f:
        f.write(ride_record)

def main():
    """Main function"""
    print("🚀 GitHub Actions Ride Notifier")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Check environment variables
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERROR: Missing Telegram credentials!")
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in GitHub Secrets")
        sys.exit(1)
    
    # Load sent rides
    sent_rides = load_sent_rides()
    
    # Generate new ride
    ride = generate_ride()
    print(f"📦 Generated ride: {ride['id']}")
    
    # Send notification
    if send_telegram_notification(ride):
        # Save to history
        sent_rides.append(ride['id'])
        save_sent_rides(sent_rides)
        update_ride_history(ride, sent_rides)
        print(f"✅ Complete! Total rides: {len(sent_rides)}")
    else:
        print("❌ Failed to send notification")
        sys.exit(1)

if __name__ == '__main__':
    main()
