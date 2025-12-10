#!/usr/bin/env python3
"""
REAL-TIME RIDE NOTIFIER - NO LOGIN REQUIRED
Monitors public ride availability and sends Telegram notifications
You accept rides from your phone app manually
"""

import time
import requests
import logging
from datetime import datetime
import schedule
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('ride_notifier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Your Telegram Configuration
TELEGRAM = {
    "bot_token": "8454418790:AAHy57BjdLadp1M_TUENDBJVtwWldtly-jc",
    "chat_id": "6411380646"
}

# Route Configuration
ROUTE_CONFIG = {
    "pickup": "Pune",
    "dropoff": "Mumbai",
    "check_interval": 300,  # Check every 5 minutes
    "notify_on_availability": True
}

class RideNotifier:
    """Monitors ride availability and sends notifications"""
    
    def __init__(self):
        self.last_notification_time = None
        self.daily_checks = 0
        self.rides_found = 0
        
    def send_telegram(self, message):
        """Send Telegram notification"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM['bot_token']}/sendMessage"
            data = {
                "chat_id": TELEGRAM['chat_id'],
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("📱 Telegram notification sent")
                return True
            else:
                logger.error(f"Telegram failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    def check_ola_rides(self):
        """Check Ola for Pune-Mumbai rides availability"""
        try:
            # Ola public API endpoint for ride estimates
            url = "https://devapi.olacabs.com/v1/products"
            
            # Pune coordinates
            pickup_lat = 18.5204
            pickup_lng = 73.8567
            
            # Mumbai coordinates  
            drop_lat = 19.0760
            drop_lng = 72.8777
            
            headers = {
                'X-APP-TOKEN': '1um4WEKl6rLA7dpkq1HkLYGxoEdJi0xXtn5sQa4S',
                'Accept': 'application/json'
            }
            
            params = {
                'pickup_lat': pickup_lat,
                'pickup_lng': pickup_lng,
                'drop_lat': drop_lat,
                'drop_lng': drop_lng
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self.parse_ride_data(data)
            else:
                logger.warning(f"API returned: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error checking rides: {e}")
            return None
    
    def parse_ride_data(self, data):
        """Parse ride availability data"""
        try:
            if 'categories' in data or 'products' in data:
                rides = data.get('categories', data.get('products', []))
                
                if rides:
                    ride_info = []
                    for ride in rides:
                        ride_type = ride.get('display_name', ride.get('name', 'Unknown'))
                        eta = ride.get('eta', 'N/A')
                        
                        ride_info.append({
                            'type': ride_type,
                            'eta': eta
                        })
                    
                    return ride_info
            
            return None
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None
    
    def check_uber_rides(self):
        """Check Uber for Pune-Mumbai availability"""
        try:
            # Uber price estimate API
            url = "https://api.uber.com/v1.2/estimates/price"
            
            params = {
                'start_latitude': 18.5204,
                'start_longitude': 73.8567,
                'end_latitude': 19.0760,
                'end_longitude': 72.8777
            }
            
            # Note: Requires Uber API key - using public endpoint
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self.parse_uber_data(data)
            
            return None
            
        except Exception as e:
            logger.debug(f"Uber check: {e}")
            return None
    
    def parse_uber_data(self, data):
        """Parse Uber data"""
        try:
            if 'prices' in data:
                rides = []
                for price in data['prices']:
                    rides.append({
                        'type': price.get('display_name', 'Unknown'),
                        'estimate': price.get('estimate', 'N/A'),
                        'duration': price.get('duration', 'N/A')
                    })
                return rides
            return None
        except:
            return None
    
    def monitor_rides(self):
        """Main monitoring function"""
        logger.info(f"\n{'='*70}")
        logger.info(f"🔍 Checking rides: {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}")
        logger.info(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*70}\n")
        
        self.daily_checks += 1
        
        # Check Ola
        ola_rides = self.check_ola_rides()
        
        # Check Uber
        uber_rides = self.check_uber_rides()
        
        # Prepare notification
        if ola_rides or uber_rides:
            self.rides_found += 1
            self.send_ride_notification(ola_rides, uber_rides)
        else:
            logger.info("No rides available currently")
            
            # Send daily summary at specific times
            current_hour = datetime.now().hour
            if current_hour in [9, 14, 18]:  # 9 AM, 2 PM, 6 PM
                self.send_daily_summary()
    
    def send_ride_notification(self, ola_rides, uber_rides):
        """Send notification about available rides"""
        
        msg = f"🚗 <b>RIDES AVAILABLE!</b>\n"
        msg += f"📍 {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}\n"
        msg += f"⏰ {datetime.now().strftime('%I:%M %p')}\n\n"
        
        if ola_rides:
            msg += "<b>🟡 OLA:</b>\n"
            for ride in ola_rides[:3]:  # Top 3
                msg += f"  • {ride['type']}"
                if ride.get('eta'):
                    msg += f" - ETA: {ride['eta']} min"
                msg += "\n"
            msg += "\n"
        
        if uber_rides:
            msg += "<b>⚫ UBER:</b>\n"
            for ride in uber_rides[:3]:
                msg += f"  • {ride['type']}"
                if ride.get('estimate'):
                    msg += f" - {ride['estimate']}"
                msg += "\n"
            msg += "\n"
        
        msg += "📱 <b>Open your driver app to accept!</b>"
        
        self.send_telegram(msg)
        logger.info(f"✅ Notification sent - {len(ola_rides or [])} Ola + {len(uber_rides or [])} Uber rides")
    
    def send_daily_summary(self):
        """Send daily monitoring summary"""
        msg = f"📊 <b>Daily Summary</b>\n\n"
        msg += f"Checks today: {self.daily_checks}\n"
        msg += f"Rides found: {self.rides_found}\n"
        msg += f"Route: {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}\n"
        msg += f"Time: {datetime.now().strftime('%I:%M %p')}"
        
        self.send_telegram(msg)
    
    def send_morning_reminder(self):
        """Send morning reminder"""
        msg = f"🌅 <b>Good Morning!</b>\n\n"
        msg += f"Ride monitoring is active for:\n"
        msg += f"📍 {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}\n\n"
        msg += f"You'll get notifications when rides are available.\n"
        msg += f"Just open your driver app and accept! 🚗"
        
        self.send_telegram(msg)
        logger.info("Morning reminder sent")
    
    def run_continuous(self):
        """Run continuous monitoring"""
        logger.info("\n" + "╔" + "="*68 + "╗")
        logger.info("║" + " "*68 + "║")
        logger.info("║" + "REAL-TIME RIDE NOTIFIER".center(68) + "║")
        logger.info("║" + "No Login Required - Just Notifications".center(68) + "║")
        logger.info("║" + " "*68 + "║")
        logger.info("╚" + "="*68 + "╝\n")
        
        # Send startup notification
        startup_msg = f"🚀 <b>Ride Notifier Started</b>\n\n"
        startup_msg += f"📍 Route: {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}\n"
        startup_msg += f"⏰ Checking every {ROUTE_CONFIG['check_interval']//60} minutes\n"
        startup_msg += f"📱 You'll get Telegram alerts when rides are available!"
        self.send_telegram(startup_msg)
        
        # Schedule checks
        schedule.every(ROUTE_CONFIG['check_interval']//60).minutes.do(self.monitor_rides)
        
        # Morning reminder at 7 AM
        schedule.every().day.at("07:00").do(self.send_morning_reminder)
        
        # Daily summary at 9 PM
        schedule.every().day.at("21:00").do(self.send_daily_summary)
        
        # First check immediately
        self.monitor_rides()
        
        logger.info(f"\n✅ Monitoring started!")
        logger.info(f"📍 Route: {ROUTE_CONFIG['pickup']} → {ROUTE_CONFIG['dropoff']}")
        logger.info(f"⏰ Check interval: Every {ROUTE_CONFIG['check_interval']//60} minutes")
        logger.info(f"📱 Telegram notifications: ENABLED")
        logger.info(f"\n⏳ Running... (Press Ctrl+C to stop)\n")
        
        # Keep running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
            except KeyboardInterrupt:
                logger.info("\n⛔ Stopping notifier...")
                stop_msg = f"⛔ <b>Ride Notifier Stopped</b>\n\n"
                stop_msg += f"Total checks: {self.daily_checks}\n"
                stop_msg += f"Rides found: {self.rides_found}"
                self.send_telegram(stop_msg)
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "REAL-TIME RIDE NOTIFIER".center(68) + "║")
    print("║" + "Get Telegram notifications - No login needed!".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("📱 How it works:")
    print("  1. Script monitors Ola/Uber ride availability")
    print(f"  2. Checks every {ROUTE_CONFIG['check_interval']//60} minutes")
    print("  3. Sends Telegram notification when rides available")
    print("  4. YOU open your driver app and accept manually")
    print("  5. NO login required - just notifications!")
    print()
    print("📍 Monitoring route: Pune → Mumbai")
    print("📲 Telegram: CONFIGURED ✅")
    print()
    
    confirm = input("Start monitoring? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        print("\n🚀 Starting ride notifier...\n")
        notifier = RideNotifier()
        notifier.run_continuous()
    else:
        print("Cancelled.")
