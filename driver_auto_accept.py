#!/usr/bin/env python3
"""
AUTO RIDE ACCEPTOR FOR DRIVERS
Automatically accepts ride requests for Ola/Uber drivers
So you get more rides when you're online
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('driver_auto_accept.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Driver Configuration
DRIVER_CONFIG = {
    "phone_number": "+919876543210",  # Your driver phone number
    "auto_accept": True,  # Auto-accept rides
    "preferred_route": "Pune to Mumbai",  # Your preferred route
    "min_fare": 2000,  # Minimum fare to accept (in rupees)
    "max_distance": 200,  # Maximum distance to accept (in km)
    "accept_delay": 1,  # Seconds to wait before accepting (to check details)
}

# Telegram Configuration
TELEGRAM_CONFIG = {
    "bot_token": "8454418790:AAHy57BjdLadp1M_TUENDBJVtwWldtly-jc",
    "chat_id": "6411380646",
    "enabled": True
}

class DriverRideAcceptor:
    """Automatically accepts ride requests for drivers"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.rides_accepted = 0
    
    def send_telegram_notification(self, message):
        """Send notification to Telegram"""
        if not TELEGRAM_CONFIG['enabled']:
            return
        
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CONFIG['chat_id'],
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("📱 Telegram notification sent!")
            else:
                logger.warning(f"⚠ Telegram notification failed: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Telegram error: {e}")
        
    def setup_browser(self):
        """Setup browser for driver app"""
        logger.info("🚗 Setting up driver interface...")
        
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Keep visible so you can see what's happening
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        logger.info("✓ Browser ready")
        
    def login_driver_app(self, platform="ola"):
        """Login to driver app"""
        try:
            if platform == "ola":
                logger.info("📱 Logging into Ola Driver app...")
                self.driver.get("https://www.olacabs.com/driver")
            else:
                logger.info("📱 Logging into Uber Driver app...")
                self.driver.get("https://www.uber.com/drive")
            
            time.sleep(3)
            
            # Click login
            login_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
            )
            login_btn.click()
            time.sleep(2)
            
            # Enter phone number
            phone_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "phone"))
            )
            phone_field.send_keys(DRIVER_CONFIG['phone_number'])
            
            # Click send OTP
            otp_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send OTP')]")
            otp_btn.click()
            
            logger.info("📲 OTP sent to your phone. Please enter OTP in the browser...")
            
            # Wait for OTP entry and login (user enters manually)
            time.sleep(30)  # Give time to enter OTP
            
            logger.info("✓ Logged in successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            return False
    
    def go_online(self):
        """Set driver status to online/available"""
        try:
            logger.info("🟢 Going online...")
            
            # Find and click "Go Online" button
            online_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Go Online') or contains(text(), 'Available')]"))
            )
            online_btn.click()
            
            logger.info("✅ You are now ONLINE and ready to receive rides!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to go online: {e}")
            return False
    
    def check_for_ride_request(self):
        """Check if there's a new ride request"""
        try:
            # Look for ride request popup
            ride_request = self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'ride-request') or contains(text(), 'New Ride Request')]"
            )
            
            if ride_request:
                return True
            return False
            
        except:
            return False
    
    def get_ride_details(self):
        """Extract ride details from request"""
        try:
            details = {}
            
            # Get pickup location
            pickup = self.driver.find_element(By.XPATH, 
                "//div[contains(@class, 'pickup')]"
            ).text
            details['pickup'] = pickup
            
            # Get dropoff location
            dropoff = self.driver.find_element(By.XPATH,
                "//div[contains(@class, 'dropoff') or contains(@class, 'destination')]"
            ).text
            details['dropoff'] = dropoff
            
            # Get fare estimate
            try:
                fare = self.driver.find_element(By.XPATH,
                    "//div[contains(@class, 'fare') or contains(text(), '₹')]"
                ).text
                details['fare'] = fare
            except:
                details['fare'] = "Not shown"
            
            # Get distance
            try:
                distance = self.driver.find_element(By.XPATH,
                    "//div[contains(@class, 'distance') or contains(text(), 'km')]"
                ).text
                details['distance'] = distance
            except:
                details['distance'] = "Not shown"
            
            return details
            
        except Exception as e:
            logger.error(f"Could not get ride details: {e}")
            return None
    
    def should_accept_ride(self, details):
        """Decide if ride should be accepted based on preferences"""
        if not details:
            return True  # Accept if we can't get details
        
        # Check preferred route
        preferred = DRIVER_CONFIG['preferred_route'].lower()
        pickup = details.get('pickup', '').lower()
        dropoff = details.get('dropoff', '').lower()
        
        if preferred:
            if 'pune' in preferred and 'mumbai' in preferred:
                if ('pune' in pickup or 'pune' in dropoff) and ('mumbai' in pickup or 'mumbai' in dropoff):
                    logger.info("✅ Matches preferred route: Pune-Mumbai")
                    return True
        
        # Accept all rides if no specific preference
        return True
    
    def accept_ride(self):
        """Accept the ride request"""
        try:
            logger.info("✅ Accepting ride...")
            
            # Find and click accept button
            accept_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'Accept') or contains(@class, 'accept')]"
                ))
            )
            
            time.sleep(DRIVER_CONFIG['accept_delay'])  # Small delay to check details
            accept_btn.click()
            
            self.rides_accepted += 1
            logger.info(f"🎉 RIDE ACCEPTED! (Total today: {self.rides_accepted})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to accept ride: {e}")
            return False
    
    def monitor_for_rides(self, duration_hours=8):
        """Continuously monitor for ride requests"""
        logger.info(f"👀 Monitoring for ride requests (will run for {duration_hours} hours)...")
        logger.info(f"📍 Preferred route: {DRIVER_CONFIG['preferred_route']}")
        logger.info(f"💰 Minimum fare: ₹{DRIVER_CONFIG['min_fare']}")
        logger.info("")
        
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        while time.time() < end_time:
            try:
                # Check for new ride request
                if self.check_for_ride_request():
                    logger.info("\n🔔 NEW RIDE REQUEST RECEIVED!")
                    
                    # Get ride details
                    details = self.get_ride_details()
                    
                    if details:
                        logger.info(f"📍 Pickup: {details.get('pickup', 'N/A')}")
                        logger.info(f"📍 Dropoff: {details.get('dropoff', 'N/A')}")
                        logger.info(f"💰 Fare: {details.get('fare', 'N/A')}")
                        logger.info(f"📏 Distance: {details.get('distance', 'N/A')}")
                        
                        # Send Telegram notification
                        telegram_msg = f"🔔 <b>NEW RIDE REQUEST!</b>\n\n"
                        telegram_msg += f"📍 <b>Pickup:</b> {details.get('pickup', 'N/A')}\n"
                        telegram_msg += f"📍 <b>Dropoff:</b> {details.get('dropoff', 'N/A')}\n"
                        telegram_msg += f"💰 <b>Fare:</b> {details.get('fare', 'N/A')}\n"
                        telegram_msg += f"📏 <b>Distance:</b> {details.get('distance', 'N/A')}\n"
                        self.send_telegram_notification(telegram_msg)
                    
                    # Decide whether to accept
                    if DRIVER_CONFIG['auto_accept'] and self.should_accept_ride(details):
                        accepted = self.accept_ride()
                        
                        if accepted:
                            # Send acceptance notification
                            accept_msg = f"✅ <b>RIDE ACCEPTED!</b>\n\n"
                            accept_msg += f"📍 {details.get('pickup', 'N/A')} → {details.get('dropoff', 'N/A')}\n"
                            accept_msg += f"💰 {details.get('fare', 'N/A')}\n"
                            accept_msg += f"🎯 Total rides today: {self.rides_accepted}"
                            self.send_telegram_notification(accept_msg)
                    else:
                        logger.info("⏭️  Skipping this ride (doesn't match preferences)")
                        skip_msg = f"⏭️ <b>Ride Skipped</b>\n\n"
                        skip_msg += f"Reason: Doesn't match preferences"
                        self.send_telegram_notification(skip_msg)
                    
                    time.sleep(5)  # Wait before checking again
                else:
                    # No ride request, wait a bit
                    time.sleep(2)
                
            except KeyboardInterrupt:
                logger.info("\n⛔ Stopping monitor (Ctrl+C pressed)")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                time.sleep(5)
        
        logger.info(f"\n📊 Session Summary:")
        logger.info(f"   Total rides accepted: {self.rides_accepted}")
        logger.info(f"   Session duration: {duration_hours} hours")
    
    def run(self, platform="ola"):
        """Main function to run driver auto-acceptor"""
        logger.info("\n╔" + "="*68 + "╗")
        logger.info("║" + " "*68 + "║")
        logger.info("║" + "DRIVER AUTO RIDE ACCEPTOR".center(68) + "║")
        logger.info("║" + f"Platform: {platform.upper()}".center(68) + "║")
        logger.info("║" + " "*68 + "║")
        logger.info("╚" + "="*68 + "╝\n")
        
        # Send startup notification to Telegram
        startup_msg = f"🚗 <b>Driver App Started</b>\n\n"
        startup_msg += f"Platform: {platform.upper()}\n"
        startup_msg += f"Route: {DRIVER_CONFIG['preferred_route']}\n"
        startup_msg += f"Min Fare: ₹{DRIVER_CONFIG['min_fare']}\n"
        startup_msg += f"Status: Going online..."
        self.send_telegram_notification(startup_msg)
        
        # Setup
        self.setup_browser()
        
        # Login
        if not self.login_driver_app(platform):
            logger.error("Failed to login. Exiting.")
            error_msg = "❌ <b>Login Failed</b>\n\nCould not login to driver app"
            self.send_telegram_notification(error_msg)
            return
        
        # Go online
        if not self.go_online():
            logger.error("Failed to go online. Exiting.")
            error_msg = "❌ <b>Failed to Go Online</b>\n\nCould not set status to online"
            self.send_telegram_notification(error_msg)
            return
        
        # Send online notification
        online_msg = f"🟢 <b>NOW ONLINE!</b>\n\n"
        online_msg += f"Ready to receive ride requests\n"
        online_msg += f"Monitoring for Pune-Mumbai rides..."
        self.send_telegram_notification(online_msg)
        
        # Monitor for rides
        self.monitor_for_rides(duration_hours=8)
        
        # Send session summary
        summary_msg = f"📊 <b>Session Ended</b>\n\n"
        summary_msg += f"Total rides accepted: {self.rides_accepted}\n"
        summary_msg += f"Thank you for driving!"
        self.send_telegram_notification(summary_msg)
        
        # Cleanup
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    import sys
    
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "DRIVER AUTO RIDE ACCEPTOR".center(68) + "║")
    print("║" + "Automatically accepts ride requests".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("Select platform:")
    print("  1. Ola Driver")
    print("  2. Uber Driver")
    print()
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Enter choice (1 or 2): ").strip()
    
    platform = "ola" if choice == "1" else "uber"
    
    acceptor = DriverRideAcceptor()
    acceptor.run(platform)
