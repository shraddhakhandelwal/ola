"""
Scheduler Script for Daily Ride Automation
Runs the ride booking script at scheduled times every day
"""

import schedule
import time
import json
import logging
from datetime import datetime
from ride_automation import RideBookingAutomation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

class RideScheduler:
    def __init__(self, config_file='config.json'):
        """Initialize the scheduler"""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_file} not found!")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in {self.config_file}")
            raise
    
    def book_ride_job(self):
        """Job that runs at scheduled time"""
        logging.info("=" * 60)
        logging.info(f"Starting scheduled ride booking at {datetime.now()}")
        logging.info("=" * 60)
        
        try:
            # Create automation instance
            automation = RideBookingAutomation(self.config_file)
            
            # Retry logic
            retry_config = self.config.get('retry', {})
            max_attempts = retry_config.get('max_attempts', 3)
            wait_time = retry_config.get('wait_between_attempts', 300)
            
            success = False
            for attempt in range(1, max_attempts + 1):
                logging.info(f"Booking attempt {attempt}/{max_attempts}")
                
                success = automation.run()
                
                if success:
                    logging.info("✓ Ride booked successfully!")
                    break
                else:
                    logging.warning(f"✗ Attempt {attempt} failed")
                    if attempt < max_attempts:
                        logging.info(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
            
            if not success:
                logging.error("All booking attempts failed!")
                self.send_notification("Ride Booking Failed", 
                                     f"Failed to book ride after {max_attempts} attempts")
            else:
                self.send_notification("Ride Booked Successfully", 
                                     f"Your ride from {self.config['pickup_location']} to {self.config['drop_location']} has been booked!")
                
        except Exception as e:
            logging.error(f"Error in scheduled job: {e}")
            self.send_notification("Ride Booking Error", f"An error occurred: {str(e)}")
    
    def send_notification(self, subject, message):
        """Send notification (placeholder - implement email/SMS as needed)"""
        notification_config = self.config.get('notifications', {})
        
        if notification_config.get('enabled', False):
            # Log notification (you can implement email/SMS here)
            logging.info(f"NOTIFICATION: {subject} - {message}")
            
            # TODO: Implement actual email/SMS notification
            # Example using smtplib for email:
            # import smtplib
            # from email.mime.text import MIMEText
            # ...
    
    def setup_schedule(self):
        """Setup the daily schedule"""
        daily_config = self.config.get('daily_schedule', {})
        
        if not daily_config.get('enabled', False):
            logging.warning("Daily schedule is disabled in config")
            return False
        
        booking_time = daily_config.get('booking_time', '08:00')
        days = daily_config.get('days', [])
        
        # Schedule for specified days
        day_mapping = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        scheduled_count = 0
        for day in days:
            day_lower = day.lower()
            if day_lower in day_mapping:
                day_mapping[day_lower].at(booking_time).do(self.book_ride_job)
                scheduled_count += 1
                logging.info(f"✓ Scheduled for {day.capitalize()} at {booking_time}")
            else:
                logging.warning(f"Invalid day: {day}")
        
        if scheduled_count == 0:
            logging.error("No valid days scheduled!")
            return False
        
        logging.info(f"Successfully scheduled {scheduled_count} day(s)")
        return True
    
    def run(self):
        """Run the scheduler"""
        print("=" * 60)
        print("Ride Booking Scheduler Started")
        print("=" * 60)
        
        if not self.setup_schedule():
            logging.error("Failed to setup schedule")
            return
        
        logging.info("Scheduler is running... Press Ctrl+C to stop")
        
        # Display next run time
        next_run = schedule.next_run()
        if next_run:
            logging.info(f"Next scheduled run: {next_run}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("\nScheduler stopped by user")
        except Exception as e:
            logging.error(f"Scheduler error: {e}")

def main():
    """Entry point for scheduler"""
    try:
        scheduler = RideScheduler()
        scheduler.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
