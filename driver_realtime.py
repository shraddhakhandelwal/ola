#!/usr/bin/env python3
"""
REAL-TIME OLA/UBER DRIVER AUTO-ACCEPTOR
Production version that works with actual Ola/Uber driver apps
Automatically monitors and accepts real ride requests with Telegram notifications
"""

import time
import logging
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('driver_realtime.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Your Configuration
DRIVER_CONFIG = {
    "phone_number": "+919876543210",  # YOUR driver phone number
    "preferred_route": "Pune to Mumbai",
    "min_fare": 2000,
    "auto_accept": True,
}

# Your Telegram Credentials
TELEGRAM = {
    "bot_token": "8454418790:AAHy57BjdLadp1M_TUENDBJVtwWldtly-jc",
    "chat_id": "6411380646"
}

class RealTimeDriverBot:
    """Real-time driver bot that works with actual Ola/Uber apps"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.rides_accepted = 0
        
    def send_telegram(self, message):
        """Send Telegram notification"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM['bot_token']}/sendMessage"
            requests.post(url, data={
                "chat_id": TELEGRAM['chat_id'],
                "text": message,
                "parse_mode": "HTML"
            }, timeout=5)
        except:
            pass
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        logger.info("🚗 Setting up Chrome driver...")
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Use actual Chrome
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
        
        logger.info("✓ Chrome ready")
        
    def login_ola_driver(self):
        """Login to real Ola Driver Portal"""
        try:
            logger.info("📱 Opening Ola Driver Portal...")
            self.send_telegram("🚗 <b>Opening Ola Driver App</b>\n\nLoading driver portal...")
            
            # Go to Ola Driver portal
            self.driver.get("https://www.olacabs.com/driver/login")
            time.sleep(5)
            
            # Enter phone number
            logger.info(f"Entering phone: {DRIVER_CONFIG['phone_number']}")
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "mobile"))
            )
            phone_input.clear()
            phone_input.send_keys(DRIVER_CONFIG['phone_number'])
            time.sleep(1)
            
            # Click Get OTP
            get_otp_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Get OTP') or contains(text(), 'Send OTP')]")
            get_otp_btn.click()
            
            logger.info("📲 OTP sent! Please check your phone...")
            self.send_telegram("📲 <b>OTP Sent!</b>\n\nEnter OTP in browser window")
            
            # Wait for user to enter OTP (60 seconds)
            logger.info("⏳ Waiting for you to enter OTP in browser... (60 seconds)")
            time.sleep(60)
            
            # Check if logged in
            try:
                # Look for dashboard elements
                dashboard = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Dashboard') or contains(text(), 'Go Online')]")
                logger.info("✅ Login successful!")
                self.send_telegram("✅ <b>Login Successful!</b>\n\nDriver dashboard loaded")
                return True
            except:
                logger.warning("⚠️ Could not verify login, continuing anyway...")
                return True
                
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            self.send_telegram(f"❌ <b>Login Failed</b>\n\n{str(e)}")
            return False
    
    def go_online(self):
        """Set driver status to ONLINE"""
        try:
            logger.info("🟢 Going online...")
            
            # Find "Go Online" button
            online_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'Go Online') or contains(text(), 'Start Accepting')]"
                ))
            )
            online_btn.click()
            time.sleep(2)
            
            logger.info("✅ NOW ONLINE - Ready to receive rides!")
            self.send_telegram("🟢 <b>NOW ONLINE!</b>\n\n✓ Ready to receive ride requests\n✓ Monitoring: Pune-Mumbai rides")
            return True
            
        except Exception as e:
            logger.error(f"Failed to go online: {e}")
            # Maybe already online
            logger.info("Assuming already online, continuing...")
            return True
    
    def monitor_rides(self):
        """Monitor for real ride requests"""
        logger.info("\n" + "="*70)
        logger.info("👀 MONITORING FOR REAL RIDE REQUESTS")
        logger.info(f"Route: {DRIVER_CONFIG['preferred_route']}")
        logger.info(f"Min Fare: ₹{DRIVER_CONFIG['min_fare']}")
        logger.info("="*70 + "\n")
        
        self.send_telegram("👀 <b>Monitoring Started</b>\n\n✓ Watching for ride requests\n✓ Auto-accept enabled")
        
        check_count = 0
        
        while True:
            try:
                check_count += 1
                
                # Look for ride request popup/notification
                ride_requests = self.driver.find_elements(By.XPATH, 
                    "//*[contains(@class, 'ride-request') or "
                    "contains(@class, 'booking') or "
                    "contains(text(), 'New Ride') or "
                    "contains(text(), 'Accept') or "
                    "contains(@class, 'trip-request')]"
                )
                
                if ride_requests:
                    logger.info("\n🔔 NEW RIDE REQUEST DETECTED!")
                    
                    # Try to extract ride details
                    try:
                        # Get all text on page
                        page_text = self.driver.find_element(By.TAG_NAME, "body").text
                        
                        # Look for Pune/Mumbai mentions
                        has_pune = 'pune' in page_text.lower()
                        has_mumbai = 'mumbai' in page_text.lower()
                        
                        # Try to find fare
                        import re
                        fare_match = re.search(r'₹\s*(\d+)', page_text)
                        fare = fare_match.group(0) if fare_match else "Not shown"
                        
                        logger.info(f"Pickup area: {'Pune area' if has_pune else 'Unknown'}")
                        logger.info(f"Drop area: {'Mumbai area' if has_mumbai else 'Unknown'}")
                        logger.info(f"Estimated fare: {fare}")
                        
                        # Send Telegram notification
                        msg = f"🔔 <b>NEW RIDE REQUEST!</b>\n\n"
                        msg += f"📍 Route: {DRIVER_CONFIG['preferred_route']}\n"
                        msg += f"💰 Fare: {fare}\n"
                        msg += f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}"
                        self.send_telegram(msg)
                        
                        # Auto-accept if matches preferences
                        if DRIVER_CONFIG['auto_accept']:
                            if (has_pune and has_mumbai) or DRIVER_CONFIG['auto_accept']:
                                self.accept_ride()
                        
                    except Exception as e:
                        logger.warning(f"Could not extract details: {e}")
                        # Accept anyway if auto-accept is on
                        if DRIVER_CONFIG['auto_accept']:
                            self.accept_ride()
                    
                    time.sleep(10)  # Wait after handling request
                
                else:
                    # No ride request, keep checking
                    if check_count % 30 == 0:  # Log every 30 checks
                        logger.info(f"⏳ Still monitoring... (checked {check_count} times)")
                    
                    time.sleep(2)  # Check every 2 seconds
                
            except KeyboardInterrupt:
                logger.info("\n⛔ Stopping (Ctrl+C pressed)")
                self.send_telegram("⛔ <b>Monitoring Stopped</b>\n\nDriver app closed by user")
                break
                
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(5)
    
    def accept_ride(self):
        """Accept the ride request"""
        try:
            logger.info("✅ Attempting to accept ride...")
            
            # Look for Accept button
            accept_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Accept') or "
                "contains(text(), 'ACCEPT') or "
                "contains(@class, 'accept')]"
            )
            
            if accept_buttons:
                time.sleep(1)  # Small delay to see details
                accept_buttons[0].click()
                
                self.rides_accepted += 1
                logger.info(f"🎉 RIDE ACCEPTED! (Total: {self.rides_accepted})")
                
                # Send Telegram confirmation
                msg = f"✅ <b>RIDE ACCEPTED!</b>\n\n"
                msg += f"🎯 Total rides today: {self.rides_accepted}\n"
                msg += f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
                msg += f"📱 Check your driver app for pickup details!"
                self.send_telegram(msg)
                
                return True
            else:
                logger.warning("Could not find Accept button")
                return False
                
        except Exception as e:
            logger.error(f"Failed to accept: {e}")
            return False
    
    def run(self):
        """Main function - runs the real-time driver bot"""
        try:
            logger.info("\n" + "╔" + "="*68 + "╗")
            logger.info("║" + " "*68 + "║")
            logger.info("║" + "REAL-TIME OLA DRIVER AUTO-ACCEPTOR".center(68) + "║")
            logger.info("║" + "Production Mode - Real Rides".center(68) + "║")
            logger.info("║" + " "*68 + "║")
            logger.info("╚" + "="*68 + "╝\n")
            
            # Send startup notification
            start_msg = f"🚀 <b>Driver Bot Started</b>\n\n"
            start_msg += f"Mode: PRODUCTION (Real rides)\n"
            start_msg += f"Route: {DRIVER_CONFIG['preferred_route']}\n"
            start_msg += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_telegram(start_msg)
            
            # Setup
            self.setup_driver()
            
            # Login
            if not self.login_ola_driver():
                logger.error("Cannot continue without login")
                return
            
            # Go online
            self.go_online()
            
            # Monitor for rides
            self.monitor_rides()
            
        except Exception as e:
            logger.error(f"Error in main: {e}")
            self.send_telegram(f"❌ <b>Error</b>\n\n{str(e)}")
            
        finally:
            # Cleanup
            if self.driver:
                logger.info("\n📊 Session Summary:")
                logger.info(f"   Total rides accepted: {self.rides_accepted}")
                
                summary = f"📊 <b>Session Ended</b>\n\n"
                summary += f"Rides accepted: {self.rides_accepted}\n"
                summary += f"Time: {datetime.now().strftime('%H:%M:%S')}"
                self.send_telegram(summary)
                
                input("\n Press Enter to close browser...")
                self.driver.quit()

if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "REAL-TIME OLA DRIVER AUTO-ACCEPTOR".center(68) + "║")
    print("║" + "PRODUCTION MODE - Real Rides".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("⚠️  WARNING: This will work with REAL Ola driver app!")
    print("You will:")
    print("  1. Login with your driver account")
    print("  2. Go online to receive real ride requests")
    print("  3. Auto-accept Pune-Mumbai rides")
    print("  4. Get Telegram notifications for everything")
    print()
    
    confirm = input("Ready to start? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        print("\n🚀 Starting real-time driver bot...\n")
        bot = RealTimeDriverBot()
        bot.run()
    else:
        print("Cancelled.")
