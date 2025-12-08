#!/usr/bin/env python3
"""
SIMPLE RIDE ALERTS - Real-Time Telegram Notifications
NO LOGIN REQUIRED - Just send you alerts to check your driver app!
"""

import requests
import schedule
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('ride_alerts.log'),
        logging.StreamHandler()
    ]
)

class SimpleRideAlert:
    def __init__(self):
        # Telegram configuration
        self.bot_token = '8454418790:AAHy57BjdLadp1M_TUENDBJVtwWldtly-jc'
        self.chat_id = '6411380646'
        
        # Route configuration
        self.route = "Pune → Mumbai"
        
        # Timing configuration (peak hours for Pune-Mumbai rides)
        self.peak_hours = [
            (6, 0),   # 6:00 AM
            (7, 0),   # 7:00 AM  
            (8, 0),   # 8:00 AM
            (9, 0),   # 9:00 AM
            (14, 0),  # 2:00 PM
            (15, 0),  # 3:00 PM
            (16, 0),  # 4:00 PM
            (17, 0),  # 5:00 PM
            (18, 0),  # 6:00 PM
            (19, 0),  # 7:00 PM
        ]
        
        self.checks_today = 0
        
    def send_telegram(self, message):
        """Send Telegram notification"""
        try:
            url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            if response.json().get('ok'):
                logging.info("✅ Telegram notification sent")
                return True
            else:
                logging.error(f"❌ Telegram error: {response.text}")
                return False
        except Exception as e:
            logging.error(f"❌ Failed to send Telegram: {e}")
            return False
    
    def send_peak_hour_reminder(self):
        """Send reminder during peak hours"""
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        
        # Check if it's a peak hour
        if (hour, minute) in self.peak_hours:
            self.checks_today += 1
            
            message = f"""🚗 PEAK HOUR ALERT! 

⏰ {current_time.strftime('%I:%M %p')} - High demand time!
📍 Route: {self.route}

💡 CHECK YOUR DRIVER APP NOW!
   • Ola Driver App
   • Uber Driver App

This is prime time for Pune→Mumbai rides.
Riders are booking now! 🔥

Checked today: {self.checks_today} times"""
            
            self.send_telegram(message)
            logging.info(f"🔔 Peak hour alert sent ({hour}:{minute:02d})")
    
    def send_morning_greeting(self):
        """Send morning greeting"""
        message = f"""🌅 GOOD MORNING DRIVER!

📅 {datetime.now().strftime('%A, %B %d, %Y')}
⏰ {datetime.now().strftime('%I:%M %p')}

📍 Monitoring: {self.route}

💼 Today's Schedule:
   • Morning rush: 6 AM - 9 AM
   • Afternoon peak: 2 PM - 4 PM  
   • Evening rush: 5 PM - 8 PM

📱 Keep your driver apps ready!

You'll get alerts during peak hours.
Good luck earning today! 💰"""
        
        self.send_telegram(message)
        self.checks_today = 0
        logging.info("🌅 Morning greeting sent")
    
    def send_afternoon_reminder(self):
        """Send afternoon reminder"""
        message = f"""☀️ AFTERNOON CHECK-IN

⏰ {datetime.now().strftime('%I:%M %p')}
📍 Route: {self.route}

🔥 Afternoon rush starting soon!

💡 Pro Tips:
   • Position yourself near pickup areas
   • Keep both Ola & Uber apps open
   • Charge your phone
   • Stay hydrated

Next peak: 2 PM - 4 PM 📊"""
        
        self.send_telegram(message)
        logging.info("☀️ Afternoon reminder sent")
    
    def send_evening_reminder(self):
        """Send evening reminder"""
        message = f"""🌆 EVENING RUSH ALERT!

⏰ {datetime.now().strftime('%I:%M %p')}
📍 Route: {self.route}

🔥 PRIME TIME FOR RIDES!

Return trips Mumbai → Pune common now.
Many riders going home from work.

📱 OPEN YOUR APPS NOW!
   High demand period ahead.

Checks today: {self.checks_today} 🚗"""
        
        self.send_telegram(message)
        logging.info("🌆 Evening reminder sent")
    
    def send_night_summary(self):
        """Send night summary"""
        message = f"""🌙 END OF DAY SUMMARY

📅 {datetime.now().strftime('%B %d, %Y')}
⏰ {datetime.now().strftime('%I:%M %p')}

📊 Today's Monitoring:
   • Peak hour alerts sent: {self.checks_today}
   • Route monitored: {self.route}
   
🙏 Great job today!

Tomorrow's first alert: 6:00 AM
Sleep well, drive safe! 😴"""
        
        self.send_telegram(message)
        logging.info("🌙 Night summary sent")
    
    def check_rides_continuous(self):
        """Continuous ride checking - every 5 minutes during peak hours"""
        current_hour = datetime.now().hour
        
        # Only check frequently during likely ride hours (6 AM - 10 PM)
        if 6 <= current_hour <= 22:
            self.checks_today += 1
            
            # Send reminders every 2 hours during active time
            if current_hour in [8, 10, 12, 14, 16, 18, 20] and datetime.now().minute < 5:
                message = f"""🔔 RIDE CHECK REMINDER

⏰ {datetime.now().strftime('%I:%M %p')}
📍 {self.route}

💡 Quick Check:
   ✓ Open Ola Driver App
   ✓ Open Uber Driver App
   ✓ Check for ride requests

Active monitoring in progress...
Total checks today: {self.checks_today}"""
                
                self.send_telegram(message)
                logging.info(f"🔍 Continuous check reminder sent (Hour: {current_hour})")
    
    def run(self):
        """Main execution loop"""
        print("\n" + "="*70)
        print("🚗 SIMPLE RIDE ALERTS - REAL-TIME NOTIFICATIONS")
        print("="*70)
        print(f"\n📍 Route: {self.route}")
        print(f"📱 Telegram: CONFIGURED ✅")
        print(f"\n⏰ Alert Schedule:")
        print(f"   • 6:00 AM - Morning greeting")
        print(f"   • 7:00 AM - 9:00 AM - Peak hour alerts")
        print(f"   • 12:00 PM - Afternoon check-in")
        print(f"   • 2:00 PM - 4:00 PM - Afternoon rush")
        print(f"   • 5:00 PM - 8:00 PM - Evening rush alerts")
        print(f"   • 10:00 PM - Daily summary")
        print(f"   • Every 2 hours - Reminder to check apps")
        print(f"\n💡 Purpose: Remind you to check your driver apps during peak times!")
        print("="*70 + "\n")
        
        # Send startup notification
        startup_msg = f"""🚀 RIDE ALERT SYSTEM STARTED!

⏰ {datetime.now().strftime('%I:%M %p')}
📍 Route: {self.route}

✅ You'll receive:
   • Peak hour alerts
   • Morning/evening reminders
   • Check-your-app notifications
   • Daily summaries

💡 How to use:
When you get an alert, simply open your Ola/Uber driver app and check for ride requests!

No login automation - just helpful reminders! 🎯"""
        
        self.send_telegram(startup_msg)
        
        # Schedule alerts
        schedule.every().day.at("06:00").do(self.send_morning_greeting)
        schedule.every().day.at("12:00").do(self.send_afternoon_reminder)
        schedule.every().day.at("17:00").do(self.send_evening_reminder)
        schedule.every().day.at("22:00").do(self.send_night_summary)
        
        # Peak hour reminders
        for hour, minute in self.peak_hours:
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.send_peak_hour_reminder)
        
        # Continuous checks every 5 minutes
        schedule.every(5).minutes.do(self.check_rides_continuous)
        
        logging.info("🚀 Ride alert system started")
        logging.info(f"📍 Monitoring: {self.route}")
        
        print("✅ System is running!")
        print("📱 Check your Telegram for alerts")
        print("⏳ Press Ctrl+C to stop\n")
        
        # Main loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            logging.info("\n👋 Ride alert system stopped by user")
            
            # Send shutdown notification
            shutdown_msg = f"""⏹️ ALERT SYSTEM STOPPED

⏰ {datetime.now().strftime('%I:%M %p')}

Ride monitoring has been paused.
Restart anytime with: python3 simple_ride_alerts.py

Stay safe! 👋"""
            
            self.send_telegram(shutdown_msg)
            print("\n👋 Goodbye! Alerts stopped.\n")

if __name__ == "__main__":
    try:
        alert_system = SimpleRideAlert()
        alert_system.run()
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        print(f"\n❌ Error: {e}\n")
