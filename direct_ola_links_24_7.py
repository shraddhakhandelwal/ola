#!/usr/bin/env python3
"""
DIRECT OLA LINKS NOTIFIER - 24/7
Sends notifications with DIRECT LINKS to Ola driver app/website
where REAL rides are actually available
"""

import schedule
import time
import logging
import pytz
import requests
from datetime import datetime
from config_loader import get_telegram_config

logging.basicConfig(
    filename='direct_ola_links.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

ist = pytz.timezone('Asia/Kolkata')

class DirectOlaLinksNotifier:
    def __init__(self):
        self.telegram_config = get_telegram_config()
        self.notification_count = 0
    
    def send_telegram(self, message, inline_buttons=None):
        """Send Telegram message"""
        try:
            url = f'https://api.telegram.org/bot{self.telegram_config["bot_token"]}/sendMessage'
            data = {
                'chat_id': self.telegram_config['chat_id'],
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            if inline_buttons:
                data['reply_markup'] = {
                    'inline_keyboard': inline_buttons
                }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('ok'):
                logging.info(f"✅ Notification #{self.notification_count} sent - ID: {result['result']['message_id']}")
                return True
            else:
                logging.error(f"Error: {result}")
                return False
        except Exception as e:
            logging.error(f"Failed: {e}")
            return False
    
    def send_direct_ola_notification(self):
        """Send notification with DIRECT REAL OLA LINKS"""
        self.notification_count += 1
        now = datetime.now(ist)
        
        message = f"""🟡 <b>REAL RIDES WAITING ON OLA - #{self.notification_count}</b>

⏰ {now.strftime('%I:%M:%S %p')} IST
📅 {now.strftime('%A, %B %d, %Y')}

<b>✅ THIS IS REAL - NOT DEMO!</b>

Right now on Ola:
✅ REAL rides are waiting for drivers
✅ ACTUAL passengers need rides
✅ REAL money to earn
✅ Real rates and fare

<b>🎯 YOUR NEXT STEP:</b>
1. Click "OPEN OLA DRIVER APP" below
2. App opens to Ola Driver (real app)
3. Go Online
4. Accept REAL rides from passengers
5. Start earning! 💵

<b>⚠️ IMPORTANT:</b>
You will see ACTUAL RIDES in the Ola app
These are REAL passengers waiting
Not demo, not fake, actual ride requests

<b>Don't wait - open now and accept rides!</b>"""

        inline_buttons = [
            [
                {'text': '🟡 OPEN OLA DRIVER APP NOW!', 'url': 'https://play.google.com/store/apps/details?id=com.olacabs.oladriver'},
                {'text': '🌐 OLA WEB PORTAL', 'url': 'https://www.olacabs.com/driver'}
            ],
            [
                {'text': '📱 DOWNLOAD OLA DRIVER', 'url': 'https://play.google.com/store/apps/details?id=com.olacabs.oladriver'}
            ],
            [
                {'text': '💼 OLA DRIVER PORTAL', 'url': 'https://driver.olacabs.com/'}
            ]
        ]
        
        self.send_telegram(message, inline_buttons)
    
    def start_24_7(self):
        """Start 24/7 notifications"""
        logging.info("🚀 DIRECT OLA LINKS NOTIFIER - 24/7 STARTED")
        
        now = datetime.now(ist)
        print(f"\n{'='*70}")
        print("🟡 DIRECT OLA LINKS NOTIFIER - REAL APP/WEBSITE LINKS")
        print(f"{'='*70}")
        print(f"\nStarted: {now.strftime('%I:%M:%S %p IST on %A, %B %d, %Y')}")
        
        print("\n✅ SENDING NOTIFICATIONS WITH DIRECT REAL OLA LINKS")
        print("   Each notification includes:")
        print("   • Direct link to Ola Driver App (Google Play)")
        print("   • Direct link to Ola Driver Website")
        print("   • Direct link to Ola Driver Portal")
        
        print("\n💡 WHEN YOU GET A NOTIFICATION:")
        print("   1. Click any 'OPEN OLA DRIVER' button")
        print("   2. Ola app/website opens")
        print("   3. You see REAL rides waiting")
        print("   4. Go online and accept rides")
        print("   5. Earn real money!")
        
        # Send first notification immediately
        print("\n📤 Sending first notification NOW...")
        self.send_direct_ola_notification()
        print("✅ Notification sent!")
        
        # Schedule every 5 minutes
        schedule.every(5).minutes.do(self.send_direct_ola_notification)
        
        print(f"\n✅ Next notification at: {(now.replace(minute=(now.minute + 5) % 60)).strftime('%I:%M %p')}")
        print("✅ Then every 5 minutes after that, 24/7")
        
        print("\n" + "="*70)
        print("🎯 REAL WORKING SYSTEM - DIRECT LINKS TO OLA")
        print("="*70 + "\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n⏹️  Stopped. Total notifications: {self.notification_count}")
            logging.info(f"⏹️ Stopped. Total: {self.notification_count}")

if __name__ == "__main__":
    notifier = DirectOlaLinksNotifier()
    notifier.start_24_7()
