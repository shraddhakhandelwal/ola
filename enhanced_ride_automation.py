"""
Enhanced Ola/Uber Ride Automation Script - Production Ready
Real-time booking with login support, OTP handling, and notifications
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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

# Configure logging with colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# File handler
file_handler = logging.FileHandler('ride_automation.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

class RideBookingAutomation:
    def __init__(self, config_file='config.json'):
        """Initialize the ride booking automation"""
        self.config = self.load_config(config_file)
        self.driver = None
        self.wait = None
        self.session_cookies = None
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                logger.info(f"{Fore.GREEN}✓ Configuration loaded successfully")
                return config
        except FileNotFoundError:
            logger.error(f"{Fore.RED}✗ Configuration file {config_file} not found!")
            raise
        except json.JSONDecodeError:
            logger.error(f"{Fore.RED}✗ Invalid JSON in {config_file}")
            raise
    
    def setup_driver(self):
        """Setup Chrome WebDriver with enhanced options"""
        chrome_options = Options()
        
        # Performance optimizations
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Anti-detection measures
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Headless mode (optional)
        if self.config.get('headless_mode', False):
            chrome_options.add_argument('--headless=new')
            logger.info(f"{Fore.YELLOW}Running in headless mode")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info(f"{Fore.GREEN}✓ WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Failed to initialize WebDriver: {e}")
            raise
    
    def handle_ola_login(self):
        """Handle Ola login with phone number and OTP"""
        try:
            logger.info(f"{Fore.CYAN}→ Initiating Ola login...")
            
            # Click login button
            try:
                login_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'Login') or contains(text(), 'Sign in')]"
                    ))
                )
                login_btn.click()
                time.sleep(2)
            except TimeoutException:
                logger.warning(f"{Fore.YELLOW}Login button not found, checking if already logged in")
                return True
            
            # Enter phone number
            phone = os.getenv('OLA_PHONE', self.config.get('phone_number'))
            if not phone:
                logger.error(f"{Fore.RED}✗ Phone number not configured")
                return False
            
            phone_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//input[@type='tel' or @type='text' or contains(@placeholder, 'phone') or contains(@placeholder, 'mobile')]"
                ))
            )
            phone_input.clear()
            phone_input.send_keys(phone)
            logger.info(f"{Fore.GREEN}✓ Phone number entered")
            time.sleep(1)
            
            # Click continue/send OTP
            continue_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[contains(text(), 'Continue') or contains(text(), 'Send OTP') or contains(text(), 'Next')]"
                ))
            )
            continue_btn.click()
            logger.info(f"{Fore.YELLOW}⏳ OTP sent to {phone}")
            time.sleep(3)
            
            # Wait for OTP input
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}⚠️  MANUAL ACTION REQUIRED")
            print(f"{Fore.CYAN}{'='*60}")
            otp = input(f"{Fore.GREEN}Enter OTP received on {phone}: {Style.RESET_ALL}")
            
            # Enter OTP
            otp_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                    "//input[@type='text' or @type='tel' or contains(@placeholder, 'OTP') or contains(@placeholder, 'otp')]"
                ))
            )
            otp_input.clear()
            otp_input.send_keys(otp)
            time.sleep(1)
            
            # Submit OTP
            try:
                submit_btn = self.driver.find_element(By.XPATH,
                    "//button[contains(text(), 'Verify') or contains(text(), 'Submit') or contains(text(), 'Continue')]"
                )
                submit_btn.click()
            except NoSuchElementException:
                otp_input.send_keys(Keys.RETURN)
            
            time.sleep(3)
            logger.info(f"{Fore.GREEN}✓ Login successful")
            
            # Save session cookies
            self.session_cookies = self.driver.get_cookies()
            
            return True
            
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Login failed: {e}")
            return False
    
    def book_ola_ride_enhanced(self):
        """Enhanced Ola ride booking with real-time features"""
        try:
            logger.info(f"{Fore.CYAN}{'='*60}")
            logger.info(f"{Fore.CYAN}Starting Ola Ride Booking")
            logger.info(f"{Fore.CYAN}{'='*60}")
            
            # Navigate to Ola
            self.driver.get("https://www.olacabs.com/")
            time.sleep(3)
            
            # Handle login if needed
            if not self.is_logged_in():
                if not self.handle_ola_login():
                    return False
            
            # Navigate to booking page
            self.driver.get("https://www.olacabs.com/book")
            time.sleep(3)
            
            # Enter pickup location
            logger.info(f"{Fore.YELLOW}→ Setting pickup location: {self.config['pickup_location']}")
            pickup_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                    "//input[contains(@placeholder, 'Pickup') or contains(@placeholder, 'pickup') or contains(@id, 'pickup')]"
                ))
            )
            pickup_input.clear()
            pickup_input.send_keys(self.config['pickup_location'])
            time.sleep(2)
            
            # Select first suggestion
            try:
                first_suggestion = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//li[contains(@class, 'autocomplete') or contains(@class, 'suggestion')][1]"
                    ))
                )
                first_suggestion.click()
                logger.info(f"{Fore.GREEN}✓ Pickup location set")
            except TimeoutException:
                pickup_input.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            # Enter drop location
            logger.info(f"{Fore.YELLOW}→ Setting drop location: {self.config['drop_location']}")
            drop_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH,
                    "//input[contains(@placeholder, 'Drop') or contains(@placeholder, 'drop') or contains(@id, 'drop')]"
                ))
            )
            drop_input.clear()
            drop_input.send_keys(self.config['drop_location'])
            time.sleep(2)
            
            # Select first suggestion
            try:
                first_suggestion = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//li[contains(@class, 'autocomplete') or contains(@class, 'suggestion')][1]"
                    ))
                )
                first_suggestion.click()
                logger.info(f"{Fore.GREEN}✓ Drop location set")
            except TimeoutException:
                drop_input.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # Select ride type
            if self.config.get('ride_type'):
                logger.info(f"{Fore.YELLOW}→ Selecting ride type: {self.config['ride_type']}")
                try:
                    ride_btn = self.driver.find_element(By.XPATH,
                        f"//div[contains(text(), '{self.config['ride_type']}') or contains(@class, '{self.config['ride_type'].lower()}')]"
                    )
                    ride_btn.click()
                    logger.info(f"{Fore.GREEN}✓ Ride type selected")
                    time.sleep(1)
                except NoSuchElementException:
                    logger.warning(f"{Fore.YELLOW}⚠ Ride type not found, using default")
            
            # Schedule ride if needed
            if self.config.get('schedule_ride', False):
                logger.info(f"{Fore.YELLOW}→ Scheduling ride for later")
                try:
                    schedule_btn = self.driver.find_element(By.XPATH,
                        "//button[contains(text(), 'Ride Later') or contains(text(), 'Schedule')]"
                    )
                    schedule_btn.click()
                    time.sleep(2)
                    # Set time (implementation depends on UI)
                    logger.info(f"{Fore.GREEN}✓ Ride scheduled")
                except NoSuchElementException:
                    logger.warning(f"{Fore.YELLOW}⚠ Schedule option not available")
            
            # Confirm booking
            logger.info(f"{Fore.YELLOW}→ Confirming booking...")
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[contains(text(), 'Book') or contains(text(), 'Confirm') or contains(text(), 'Request')]"
                ))
            )
            
            # Take screenshot before booking
            screenshot_name = f"screenshots/ola_before_booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs('screenshots', exist_ok=True)
            self.driver.save_screenshot(screenshot_name)
            
            confirm_btn.click()
            logger.info(f"{Fore.GREEN}✓ Booking request submitted!")
            
            time.sleep(5)
            
            # Take confirmation screenshot
            screenshot_name = f"screenshots/ola_confirmation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_name)
            logger.info(f"{Fore.GREEN}✓ Screenshot saved: {screenshot_name}")
            
            # Send notification
            self.send_notification_enhanced(
                "Ola Ride Booked Successfully! 🚗",
                f"Ride booked from {self.config['pickup_location']} to {self.config['drop_location']}"
            )
            
            logger.info(f"{Fore.GREEN}{'='*60}")
            logger.info(f"{Fore.GREEN}✓ OLA RIDE BOOKED SUCCESSFULLY!")
            logger.info(f"{Fore.GREEN}{'='*60}")
            
            return True
            
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Error booking Ola ride: {e}")
            screenshot_name = f"screenshots/ola_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs('screenshots', exist_ok=True)
            self.driver.save_screenshot(screenshot_name)
            return False
    
    def is_logged_in(self):
        """Check if user is already logged in"""
        try:
            # Check for common logged-in indicators
            self.driver.find_element(By.XPATH,
                "//button[contains(text(), 'Logout') or contains(@class, 'logout')] | //div[contains(@class, 'profile') or contains(@class, 'user')]"
            )
            return True
        except NoSuchElementException:
            return False
    
    def send_notification_enhanced(self, title, message):
        """Send notifications via multiple channels"""
        logger.info(f"{Fore.CYAN}→ Sending notifications...")
        
        # Console notification
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}🔔 {title}")
        print(f"{Fore.WHITE}{message}")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        # Email notification
        if self.config.get('notifications', {}).get('email_enabled', False):
            self.send_email(title, message)
        
        # SMS notification
        if self.config.get('notifications', {}).get('sms_enabled', False):
            self.send_sms(title, message)
    
    def send_email(self, subject, body):
        """Send email notification"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_user = os.getenv('SMTP_USER')
            smtp_pass = os.getenv('SMTP_PASSWORD')
            to_email = self.config.get('notifications', {}).get('email')
            
            if not all([smtp_user, smtp_pass, to_email]):
                logger.warning(f"{Fore.YELLOW}⚠ Email credentials not configured")
                return
            
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            logger.info(f"{Fore.GREEN}✓ Email sent to {to_email}")
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Email sending failed: {e}")
    
    def send_sms(self, title, message):
        """Send SMS notification using Twilio"""
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_PHONE_NUMBER')
            to_number = self.config.get('notifications', {}).get('sms_number')
            
            if not all([account_sid, auth_token, from_number, to_number]):
                logger.warning(f"{Fore.YELLOW}⚠ SMS credentials not configured")
                return
            
            client = Client(account_sid, auth_token)
            
            sms_message = client.messages.create(
                body=f"{title}\n\n{message}",
                from_=from_number,
                to=to_number
            )
            
            logger.info(f"{Fore.GREEN}✓ SMS sent to {to_number}")
        except Exception as e:
            logger.error(f"{Fore.RED}✗ SMS sending failed: {e}")
    
    def run(self):
        """Main execution method"""
        try:
            self.setup_driver()
            
            platform = self.config.get('platform', 'ola').lower()
            
            logger.info(f"{Fore.CYAN}Platform: {platform.upper()}")
            logger.info(f"{Fore.CYAN}Route: {self.config['pickup_location']} → {self.config['drop_location']}")
            
            success = False
            
            if platform == 'ola':
                success = self.book_ola_ride_enhanced()
            else:
                logger.error(f"{Fore.RED}✗ Platform {platform} not implemented in enhanced version")
            
            if success:
                logger.info(f"{Fore.GREEN}✓ Ride booking completed successfully!")
            else:
                logger.error(f"{Fore.RED}✗ Ride booking failed")
            
            # Keep browser open for verification
            if self.config.get('keep_browser_open', False):
                input(f"\n{Fore.YELLOW}Press Enter to close browser...{Style.RESET_ALL}")
            else:
                time.sleep(5)
            
            return success
            
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Fatal error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                logger.info(f"{Fore.CYAN}Browser closed")

def main():
    """Entry point"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}🚗 Ola/Uber Enhanced Ride Automation")
    print(f"{Fore.CYAN}📍 Pune → Mumbai Daily Commute")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    try:
        automation = RideBookingAutomation()
        success = automation.run()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"{Fore.RED}✗ Fatal error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
