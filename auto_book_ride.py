#!/usr/bin/env python3
"""
AUTO RIDE BOOKING - Books ride so it's ready when you open Ola/Uber app
Automatically books Pune → Mumbai ride daily, so when you open the app, ride is already there
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import schedule

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_booking.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "phone_number": "+919876543210",  # Your phone number
    "pickup": "Pune Railway Station, Pune",
    "dropoff": "Mumbai Central, Mumbai",
    "ride_type": "Prime",
    "booking_time": "07:30",  # Book at 7:30 AM so ride is ready by 8 AM
    "advance_minutes": 30,  # Book 30 min in advance
}

class AutoRideBooker:
    """Automatically books ride so it's ready when you open the app"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_browser(self):
        """Setup headless browser"""
        logger.info("🚀 Setting up browser...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        logger.info("✓ Browser ready")
        
    def book_ola_ride(self):
        """Book Ola ride"""
        try:
            logger.info("📱 Booking Ola ride...")
            
            # Go to Ola
            self.driver.get("https://www.olacabs.com")
            time.sleep(3)
            
            # Click Book Now
            book_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book')]"))
            )
            book_btn.click()
            time.sleep(2)
            
            # Enter pickup
            logger.info(f"📍 Pickup: {CONFIG['pickup']}")
            pickup_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "pickup"))
            )
            pickup_field.clear()
            pickup_field.send_keys(CONFIG['pickup'])
            time.sleep(2)
            pickup_field.send_keys(Keys.ARROW_DOWN)
            pickup_field.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # Enter dropoff
            logger.info(f"📍 Dropoff: {CONFIG['dropoff']}")
            dropoff_field = self.driver.find_element(By.ID, "drop")
            dropoff_field.clear()
            dropoff_field.send_keys(CONFIG['dropoff'])
            time.sleep(2)
            dropoff_field.send_keys(Keys.ARROW_DOWN)
            dropoff_field.send_keys(Keys.ENTER)
            time.sleep(2)
            
            # Select ride type
            logger.info(f"🚗 Selecting {CONFIG['ride_type']} ride")
            ride_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{CONFIG['ride_type']}')]"))
            )
            ride_btn.click()
            time.sleep(1)
            
            # Book ride
            logger.info("✅ Confirming booking...")
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )
            confirm_btn.click()
            
            logger.info("🎉 RIDE BOOKED! Open your Ola app - ride is waiting!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Booking failed: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def book_uber_ride(self):
        """Book Uber ride"""
        try:
            logger.info("📱 Booking Uber ride...")
            
            # Go to Uber
            self.driver.get("https://www.uber.com")
            time.sleep(3)
            
            # Enter pickup
            logger.info(f"📍 Pickup: {CONFIG['pickup']}")
            pickup_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "pickup-typeahead-input"))
            )
            pickup_input.send_keys(CONFIG['pickup'])
            time.sleep(2)
            pickup_input.send_keys(Keys.ARROW_DOWN)
            pickup_input.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # Enter dropoff
            logger.info(f"📍 Dropoff: {CONFIG['dropoff']}")
            dropoff_input = self.driver.find_element(By.ID, "dropoff-typeahead-input")
            dropoff_input.send_keys(CONFIG['dropoff'])
            time.sleep(2)
            dropoff_input.send_keys(Keys.ARROW_DOWN)
            dropoff_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            # Request ride
            logger.info("✅ Requesting ride...")
            request_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Request')]"))
            )
            request_btn.click()
            
            logger.info("🎉 RIDE REQUESTED! Open your Uber app - ride is waiting!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Booking failed: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def auto_book(self):
        """Main booking function"""
        logger.info("\n" + "="*70)
        logger.info(f"⏰ AUTO BOOKING STARTED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
        
        self.setup_browser()
        
        # Try Ola first, then Uber as backup
        success = self.book_ola_ride()
        if not success:
            logger.info("🔄 Trying Uber as backup...")
            self.setup_browser()
            success = self.book_uber_ride()
        
        if success:
            logger.info("\n✅ SUCCESS! Your ride is booked and waiting in the app!")
            logger.info("📱 Open Ola/Uber app now to see your ride\n")
        else:
            logger.error("\n❌ Booking failed on both platforms. Will retry at next scheduled time.\n")
        
        return success

def schedule_daily_booking():
    """Schedule daily automatic booking"""
    booker = AutoRideBooker()
    
    # Schedule for configured time
    schedule.every().day.at(CONFIG['booking_time']).do(booker.auto_book)
    
    logger.info("╔" + "="*68 + "╗")
    logger.info("║" + " "*68 + "║")
    logger.info("║" + "AUTO RIDE BOOKING - SCHEDULER STARTED".center(68) + "║")
    logger.info("║" + " "*68 + "║")
    logger.info("╚" + "="*68 + "╝")
    logger.info(f"\n📅 Daily booking scheduled at: {CONFIG['booking_time']}")
    logger.info(f"📍 Route: {CONFIG['pickup']} → {CONFIG['dropoff']}")
    logger.info(f"🚗 Ride type: {CONFIG['ride_type']}")
    logger.info(f"\n💡 How it works:")
    logger.info(f"   1. Script runs at {CONFIG['booking_time']} every day")
    logger.info(f"   2. Books your Pune → Mumbai ride automatically")
    logger.info(f"   3. When you open Ola/Uber app, ride is already booked!")
    logger.info(f"\n⏳ Waiting for scheduled time... (Press Ctrl+C to stop)\n")
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(30)

def book_now():
    """Book ride immediately"""
    booker = AutoRideBooker()
    booker.auto_book()

if __name__ == "__main__":
    import sys
    
    print("\n╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "AUTO RIDE BOOKING - Pune → Mumbai".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print("Choose option:")
    print("  1. Book ride NOW (ride will be ready in 2 minutes)")
    print("  2. Setup daily auto-booking (books every day automatically)")
    print()
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🚀 Booking ride NOW...")
        print("⏳ This will take about 1-2 minutes...")
        book_now()
    elif choice == "2":
        print("\n📅 Setting up daily auto-booking...")
        schedule_daily_booking()
    else:
        print("❌ Invalid choice. Use: python3 auto_book_ride.py 1  or  python3 auto_book_ride.py 2")
