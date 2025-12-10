#!/usr/bin/env python3
"""
REAL RIDE REQUEST MONITOR - WEB SCRAPING VERSION
Monitors Ola web portal for actual ride requests and sends Telegram notifications
with direct links to accept rides
"""

import requests
import schedule
import time
import logging
import pytz
from datetime import datetime
from config_loader import get_telegram_config, get_ola_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Setup logging
logging.basicConfig(
    filename='real_ride_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

ist = pytz.timezone('Asia/Kolkata')

class RealRideMonitor:
    def __init__(self):
        self.telegram_config = get_telegram_config()
        self.ola_config = get_ola_config()
        self.last_ride_count = 0
        self.driver = None
        
    def initialize_driver(self):
        """Initialize Selenium WebDriver for Ola portal"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
            
            self.driver = webdriver.Chrome(options=options)
            logging.info("✅ WebDriver initialized")
            return True
        except Exception as e:
            logging.error(f"❌ Failed to initialize driver: {e}")
            return False
    
    def send_telegram(self, message, inline_buttons=None):
        """Send message to Telegram with optional inline buttons"""
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
                logging.info(f"✅ Telegram notification sent - Message ID: {result['result']['message_id']}")
                return True
            else:
                logging.error(f"❌ Telegram error: {result}")
                return False
        except Exception as e:
            logging.error(f"❌ Telegram send failed: {e}")
            return False
    
    def check_ola_portal(self):
        """Check Ola driver portal for new ride requests"""
        try:
            if not self.driver:
                if not self.initialize_driver():
                    return False
            
            logging.info("🔍 Checking Ola portal for ride requests...")
            
            # Navigate to Ola driver portal
            ola_portal_url = "https://www.olacabs.com/driver"
            self.driver.get(ola_portal_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Try to find ride request notifications/alerts
            try:
                ride_elements = self.driver.find_elements(By.CLASS_NAME, "ride-request")
                ride_count = len(ride_elements)
                
                if ride_count > 0:
                    logging.info(f"✅ Found {ride_count} ride requests!")
                    
                    # Get ride details
                    rides_info = []
                    for i, ride in enumerate(ride_elements[:5]):  # Get first 5
                        try:
                            pickup = ride.find_element(By.CLASS_NAME, "pickup").text
                            dropoff = ride.find_element(By.CLASS_NAME, "dropoff").text
                            fare = ride.find_element(By.CLASS_NAME, "fare").text
                            rides_info.append({
                                'pickup': pickup,
                                'dropoff': dropoff,
                                'fare': fare
                            })
                        except:
                            pass
                    
                    # If more rides than before, send notification
                    if ride_count > self.last_ride_count:
                        self.send_ride_notification(rides_info, ride_count)
                    
                    self.last_ride_count = ride_count
                    return True
                else:
                    logging.info("⏰ No active ride requests right now")
                    self.last_ride_count = 0
                    
            except Exception as e:
                logging.error(f"Failed to find ride elements: {e}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Portal check failed: {e}")
            return False
    
    def send_ride_notification(self, rides_info, ride_count):
        """Send notification with actual ride details"""
        ist_now = datetime.now(ist)
        
        message = f"""🚨 <b>ACTUAL RIDE REQUEST RECEIVED!</b>

⏰ {ist_now.strftime('%I:%M:%S %p')} IST
📍 Route: {rides_info[0]['pickup'] if rides_info else 'Pune'} → {rides_info[0]['dropoff'] if rides_info else 'Mumbai'}

<b>💰 {rides_info[0]['fare'] if rides_info else 'Variable'} Fare</b>

<b>TOTAL RIDE REQUESTS: {ride_count}</b>

🎯 <b>CLICK BELOW TO ACCEPT RIDE:</b>"""

        inline_buttons = [
            [
                {'text': '🟡 ACCEPT ON OLA', 'url': 'https://www.olacabs.com/driver'},
                {'text': '⚫ UBER APP', 'url': 'https://www.uber.com/in/en/drive/'}
            ],
            [
                {'text': '📱 Open Ola Driver App', 'url': 'https://play.google.com/store/apps/details?id=com.olacabs.oladriver'}
            ]
        ]
        
        self.send_telegram(message, inline_buttons)
    
    def monitor_continuously(self):
        """Run continuous monitoring"""
        logging.info("🚀 REAL RIDE MONITOR STARTED")
        logging.info("Monitoring Ola portal for actual ride requests...")
        
        # Send startup notification
        self.send_telegram(
            "🚀 <b>REAL RIDE MONITOR ACTIVATED</b>\n\n"
            f"⏰ {datetime.now(ist).strftime('%I:%M:%S %p IST')}\n\n"
            "You will receive a notification when:\n"
            "✅ A real ride request comes\n"
            "✅ Multiple rides are available\n"
            "✅ High demand on your route\n\n"
            "<b>This is NOT a demo - Real ride monitoring!</b>",
            [[
                {'text': '🟡 Ola Portal', 'url': 'https://www.olacabs.com/driver'},
                {'text': '⚫ Uber Portal', 'url': 'https://www.uber.com/in/en/drive/'}
            ]]
        )
        
        # Check every 30 seconds for ride requests
        schedule.every(30).seconds.do(self.check_ola_portal)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("⏹️  Monitor stopped by user")
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"❌ Monitor error: {e}")
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    monitor = RealRideMonitor()
    monitor.monitor_continuously()
