#!/usr/bin/env python3
"""
Test Telegram Notifications
Sends a test message to verify your Telegram bot is working
"""

import requests

# Your Telegram credentials
BOT_TOKEN = "8454418790:AAHy57BjdLadp1M_TUENDBJVtwWldtly-jc"
CHAT_ID = "6411380646"

def send_test_notification():
    """Send test message to Telegram"""
    
    print("📱 Testing Telegram notifications...")
    print(f"Bot Token: {BOT_TOKEN[:20]}...")
    print(f"Chat ID: {CHAT_ID}")
    print()
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        message = """🚗 <b>Ola/Uber Driver Bot - Test Message</b>

✅ Your Telegram notifications are working!

This is what you'll receive when:
• New ride request comes
• Ride is accepted
• Session starts/ends

📍 <b>Example Ride Notification:</b>
Pickup: Pune Railway Station
Dropoff: Mumbai Central
Fare: ₹2,800
Distance: 150 km

Ready to start receiving real notifications! 🎉"""
        
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        print("Sending test message...")
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ SUCCESS! Check your Telegram - you should see the test message!")
            print()
            result = response.json()
            print(f"Message ID: {result['result']['message_id']}")
            print(f"Chat: {result['result']['chat']['first_name']}")
            return True
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print()
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "TELEGRAM NOTIFICATION TEST".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    success = send_test_notification()
    
    print()
    if success:
        print("🎉 Telegram is configured correctly!")
        print("You can now run: python3 driver_auto_accept.py 1")
        print("And you'll get ride notifications on Telegram!")
    else:
        print("⚠️  Please check:")
        print("  1. Bot token is correct")
        print("  2. Chat ID is correct")
        print("  3. You've started a chat with the bot")
        print("  4. Internet connection is working")
    print()
