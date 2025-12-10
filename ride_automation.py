"""
Ola/Uber Ride Automation Script
Automates booking rides from Pune to Mumbai on a daily basis
"""

import os
import json
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ride_automation.log'),
        logging.StreamHandler()
    ]
)

class RideBookingAutomation:
    def __init__(self, config_file='config.json'):
        """Initialize the ride booking automation"""
        self.config = self.load_config(config_file)
        self.driver = None
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file {config_file} not found!")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {config_file}")
            raise
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        
        # Uncomment for headless mode (no browser window)
        # chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent to avoid detection
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def book_ola_ride(self):
        """Automate Ola ride booking"""
        try:
            logging.info("Starting Ola ride booking...")
            
            # Navigate to Ola web booking
            self.driver.get("https://www.olacabs.com/")
            time.sleep(3)
            
            # Click on "Book a Ride" or similar button
            try:
                book_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book') or contains(text(), 'Ride')]"))
                )
                book_button.click()
                time.sleep(2)
            except TimeoutException:
                logging.warning("Book button not found, proceeding...")
            
            # Enter pickup location
            pickup_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter pickup location' or contains(@placeholder, 'Pickup') or contains(@placeholder, 'pickup')]"))
            )
            pickup_input.clear()
            pickup_input.send_keys(self.config['pickup_location'])
            time.sleep(2)
            
            # Select first suggestion
            first_suggestion = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'suggestion') or contains(@class, 'autocomplete')]//li[1]"))
            )
            first_suggestion.click()
            time.sleep(1)
            
            # Enter drop location
            drop_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter drop location' or contains(@placeholder, 'Drop') or contains(@placeholder, 'drop')]"))
            )
            drop_input.clear()
            drop_input.send_keys(self.config['drop_location'])
            time.sleep(2)
            
            # Select first suggestion
            first_suggestion = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'suggestion') or contains(@class, 'autocomplete')]//li[1]"))
            )
            first_suggestion.click()
            time.sleep(2)
            
            # Look for "Ride Later" option if scheduling is needed
            if self.config.get('schedule_ride', False):
                try:
                    ride_later = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ride Later') or contains(text(), 'Schedule')]")
                    ride_later.click()
                    time.sleep(2)
                    # Set time and date based on config
                    # This part depends on Ola's UI structure
                except NoSuchElementException:
                    logging.warning("Ride Later option not found")
            
            # Select ride type (if specified)
            if self.config.get('ride_type'):
                try:
                    ride_type_button = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{self.config['ride_type']}')]")
                    ride_type_button.click()
                    time.sleep(1)
                except NoSuchElementException:
                    logging.warning(f"Ride type {self.config['ride_type']} not found")
            
            # Click Book/Confirm button
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book') or contains(text(), 'Confirm') or contains(text(), 'Continue')]"))
            )
            confirm_button.click()
            
            logging.info("Ola ride booking initiated successfully!")
            
            # Wait for booking confirmation
            time.sleep(5)
            
            # Take screenshot
            screenshot_name = f"ola_booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_name)
            logging.info(f"Screenshot saved: {screenshot_name}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error booking Ola ride: {e}")
            screenshot_name = f"ola_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_name)
            return False
    
    def book_uber_ride(self):
        """Automate Uber ride booking"""
        try:
            logging.info("Starting Uber ride booking...")
            
            # Navigate to Uber web booking
            self.driver.get("https://www.uber.com/global/en/ride/")
            time.sleep(3)
            
            # Enter pickup location
            pickup_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "pickup-input"))
            )
            pickup_input.clear()
            pickup_input.send_keys(self.config['pickup_location'])
            time.sleep(2)
            
            # Select first suggestion
            first_suggestion = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@role='option'][1]"))
            )
            first_suggestion.click()
            time.sleep(1)
            
            # Enter drop location
            drop_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "drop-input"))
            )
            drop_input.clear()
            drop_input.send_keys(self.config['drop_location'])
            time.sleep(2)
            
            # Select first suggestion
            first_suggestion = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@role='option'][1]"))
            )
            first_suggestion.click()
            time.sleep(2)
            
            # Select ride option
            if self.config.get('ride_type'):
                try:
                    ride_option = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{self.config['ride_type']}')]")
                    ride_option.click()
                    time.sleep(1)
                except NoSuchElementException:
                    logging.warning(f"Ride type {self.config['ride_type']} not found")
            
            # Click Request/Book button
            request_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Request') or contains(text(), 'Book')]"))
            )
            request_button.click()
            
            logging.info("Uber ride booking initiated successfully!")
            
            # Wait for booking confirmation
            time.sleep(5)
            
            # Take screenshot
            screenshot_name = f"uber_booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_name)
            logging.info(f"Screenshot saved: {screenshot_name}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error booking Uber ride: {e}")
            screenshot_name = f"uber_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_name)
            return False
    
    def run(self):
        """Main execution method"""
        try:
            self.setup_driver()
            
            platform = self.config.get('platform', 'ola').lower()
            
            if platform == 'ola':
                success = self.book_ola_ride()
            elif platform == 'uber':
                success = self.book_uber_ride()
            elif platform == 'both':
                # Try Ola first, then Uber if Ola fails
                success = self.book_ola_ride()
                if not success:
                    logging.info("Ola booking failed, trying Uber...")
                    success = self.book_uber_ride()
            else:
                logging.error(f"Unknown platform: {platform}")
                return False
            
            if success:
                logging.info("✓ Ride booking completed successfully!")
            else:
                logging.error("✗ Ride booking failed")
            
            # Keep browser open for manual verification (optional)
            if self.config.get('keep_browser_open', False):
                input("Press Enter to close browser...")
            
            return success
            
        except Exception as e:
            logging.error(f"Error in main execution: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Browser closed")

def main():
    """Entry point for the script"""
    print("=" * 60)
    print("Ola/Uber Ride Automation - Pune to Mumbai")
    print("=" * 60)
    
    try:
        automation = RideBookingAutomation()
        automation.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
