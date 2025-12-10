"""
Ola API-Based Ride Automation
Uses official Ola API for reliable booking
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize
init(autoreset=True)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ola_api_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OlaAPIAutomation:
    """Ola API-based ride booking automation"""
    
    # Ola API Configuration
    API_BASE_URL = "https://devapi.olacabs.com/v1"
    
    def __init__(self, config_file='config.json'):
        """Initialize with config"""
        self.config = self.load_config(config_file)
        
        # Load API credentials (OAuth2 Client Credentials)
        self.client_id = os.getenv('OLA_CLIENT_ID', '7387ed63-a1f3-4601-bba3-a659a56c912d')
        self.client_secret = os.getenv('OLA_CLIENT_SECRET', 'd5e90dc30ed34261ba79bdcb83af705c')
        self.access_token = None
        
        # Setup session
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Get OAuth2 access token
        self._authenticate()
        
        logger.info(f"{Fore.GREEN}✓ Ola API client initialized")
        logger.info(f"{Fore.CYAN}Client ID: {self.client_id[:20]}...")
    
    def _authenticate(self):
        """Authenticate using OAuth2 client credentials flow"""
        try:
            auth_url = f"{self.API_BASE_URL}/oauth2/token"
            
            payload = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'booking.create booking.read'
            }
            
            logger.info(f"{Fore.CYAN}→ Authenticating with Ola API...")
            response = requests.post(auth_url, data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                
                # Update session headers with access token
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                
                logger.info(f"{Fore.GREEN}✓ Authentication successful")
                return True
            else:
                logger.warning(f"{Fore.YELLOW}⚠ OAuth2 failed ({response.status_code}), using direct credentials")
                # Fallback: Use client credentials directly
                self.session.headers.update({
                    'X-Client-Id': self.client_id,
                    'X-Client-Secret': self.client_secret
                })
                return True
                
        except Exception as e:
            logger.warning(f"{Fore.YELLOW}⚠ Authentication error: {e}, using direct credentials")
            # Fallback: Use client credentials directly
            self.session.headers.update({
                'X-Client-Id': self.client_id,
                'X-Client-Secret': self.client_secret
            })
            return True
    
    def load_config(self, config_file):
        """Load configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Failed to load config: {e}")
            raise
    
    def get_ride_estimate(self, pickup_lat, pickup_lng, drop_lat, drop_lng):
        """Get ride estimate from Ola API"""
        try:
            endpoint = f"{self.API_BASE_URL}/products"
            
            params = {
                'pickup_lat': pickup_lat,
                'pickup_lng': pickup_lng,
                'drop_lat': drop_lat,
                'drop_lng': drop_lng,
                'category': self.config.get('ride_type', 'prime').lower()
            }
            
            logger.info(f"{Fore.CYAN}→ Fetching ride estimates...")
            response = self.session.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"{Fore.GREEN}✓ Ride estimates received")
                return data
            else:
                logger.error(f"{Fore.RED}✗ API Error: {response.status_code}")
                logger.error(f"{Fore.RED}Response: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Error getting estimate: {e}")
            return None
    
    def book_ride(self, pickup_lat, pickup_lng, drop_lat, drop_lng):
        """Book a ride using Ola API"""
        try:
            endpoint = f"{self.API_BASE_URL}/bookings"
            
            booking_data = {
                'pickup_lat': pickup_lat,
                'pickup_lng': pickup_lng,
                'drop_lat': drop_lat,
                'drop_lng': drop_lng,
                'pickup_mode': 'NOW',
                'category': self.config.get('ride_type', 'prime').lower(),
                'customer_id': self.config.get('customer_id', 'default_customer')
            }
            
            logger.info(f"{Fore.CYAN}→ Submitting booking request...")
            logger.info(f"{Fore.CYAN}From: {self.config['pickup_location']}")
            logger.info(f"{Fore.CYAN}To: {self.config['drop_location']}")
            
            response = self.session.post(endpoint, json=booking_data)
            
            if response.status_code in [200, 201]:
                booking_response = response.json()
                logger.info(f"{Fore.GREEN}✓ BOOKING SUCCESSFUL!")
                logger.info(f"{Fore.GREEN}Booking ID: {booking_response.get('booking_id', 'N/A')}")
                
                # Save booking details
                self.save_booking_details(booking_response)
                
                return booking_response
            else:
                logger.error(f"{Fore.RED}✗ Booking failed: {response.status_code}")
                logger.error(f"{Fore.RED}Response: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Error booking ride: {e}")
            return None
    
    def geocode_address(self, address):
        """Convert address to coordinates using geocoding"""
        try:
            # For demo purposes, using hardcoded coordinates
            # In production, use Google Maps Geocoding API or similar
            
            # Pune Railway Station coordinates
            if 'pune' in address.lower() and ('railway' in address.lower() or 'station' in address.lower()):
                return {'lat': 18.5284, 'lng': 73.8721}
            
            # Mumbai Central coordinates
            if 'mumbai' in address.lower() and 'central' in address.lower():
                return {'lat': 18.9685, 'lng': 72.8205}
            
            # Generic Pune coordinates
            if 'pune' in address.lower():
                return {'lat': 18.5204, 'lng': 73.8567}
            
            # Generic Mumbai coordinates
            if 'mumbai' in address.lower():
                return {'lat': 19.0760, 'lng': 72.8777}
            
            logger.warning(f"{Fore.YELLOW}⚠ Using default coordinates for: {address}")
            return {'lat': 18.5204, 'lng': 73.8567}
            
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Geocoding error: {e}")
            return None
    
    def save_booking_details(self, booking_data):
        """Save booking details to file"""
        try:
            booking_file = f"bookings/booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs('bookings', exist_ok=True)
            
            with open(booking_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'booking_data': booking_data,
                    'route': {
                        'from': self.config['pickup_location'],
                        'to': self.config['drop_location']
                    }
                }, f, indent=2)
            
            logger.info(f"{Fore.GREEN}✓ Booking details saved: {booking_file}")
            
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Failed to save booking: {e}")
    
    def send_notification(self, title, message):
        """Send notifications"""
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}🔔 {title}")
        print(f"{Fore.WHITE}{message}")
        print(f"{Fore.GREEN}{'='*70}\n")
        
        # Email/SMS notifications
        if self.config.get('notifications', {}).get('email_enabled'):
            self.send_email(title, message)
        
        if self.config.get('notifications', {}).get('sms_enabled'):
            self.send_sms(title, message)
    
    def send_email(self, subject, body):
        """Send email notification"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            smtp_user = os.getenv('SMTP_USER')
            smtp_pass = os.getenv('SMTP_PASSWORD')
            to_email = self.config.get('notifications', {}).get('email')
            
            if not all([smtp_user, smtp_pass, to_email]):
                return
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = to_email
            
            with smtplib.SMTP(os.getenv('SMTP_HOST', 'smtp.gmail.com'), 
                            int(os.getenv('SMTP_PORT', 587))) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            logger.info(f"{Fore.GREEN}✓ Email sent to {to_email}")
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Email failed: {e}")
    
    def send_sms(self, title, message):
        """Send SMS notification"""
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_PHONE_NUMBER')
            to_number = self.config.get('notifications', {}).get('sms_number')
            
            if not all([account_sid, auth_token, from_number, to_number]):
                return
            
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=f"{title}\n\n{message}",
                from_=from_number,
                to=to_number
            )
            
            logger.info(f"{Fore.GREEN}✓ SMS sent to {to_number}")
        except Exception as e:
            logger.error(f"{Fore.RED}✗ SMS failed: {e}")
    
    def run(self):
        """Main execution"""
        try:
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.GREEN}🚗 Ola API-Based Ride Booking")
            print(f"{Fore.CYAN}{'='*70}\n")
            
            # Get coordinates
            pickup_coords = self.geocode_address(self.config['pickup_location'])
            drop_coords = self.geocode_address(self.config['drop_location'])
            
            if not pickup_coords or not drop_coords:
                logger.error(f"{Fore.RED}✗ Failed to geocode addresses")
                return False
            
            # Get estimate first
            estimate = self.get_ride_estimate(
                pickup_coords['lat'], pickup_coords['lng'],
                drop_coords['lat'], drop_coords['lng']
            )
            
            if estimate:
                logger.info(f"{Fore.CYAN}Estimated fare: ₹{estimate.get('estimated_fare', 'N/A')}")
            
            # Book the ride
            booking = self.book_ride(
                pickup_coords['lat'], pickup_coords['lng'],
                drop_coords['lat'], drop_coords['lng']
            )
            
            if booking:
                # Send success notification
                self.send_notification(
                    "✅ Ola Ride Booked Successfully!",
                    f"Booking ID: {booking.get('booking_id', 'N/A')}\n"
                    f"From: {self.config['pickup_location']}\n"
                    f"To: {self.config['drop_location']}\n"
                    f"Type: {self.config.get('ride_type', 'Prime')}\n\n"
                    f"Check your Ola app for driver details!"
                )
                
                logger.info(f"{Fore.GREEN}✓ Ride booking completed successfully!")
                return True
            else:
                logger.error(f"{Fore.RED}✗ Ride booking failed")
                self.send_notification(
                    "❌ Ola Ride Booking Failed",
                    f"Failed to book ride from {self.config['pickup_location']} "
                    f"to {self.config['drop_location']}. Please check logs."
                )
                return False
                
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Fatal error: {e}")
            return False

def main():
    """Entry point"""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}🚗 Ola API Automation - Pune to Mumbai")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    try:
        automation = OlaAPIAutomation()
        success = automation.run()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"{Fore.RED}✗ Fatal error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
