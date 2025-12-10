"""
Enhanced Scheduler with Real-time Monitoring
Runs ride booking with retry logic, health checks, and notifications
"""

import schedule
import time
import json
import logging
import os
from datetime import datetime, timedelta
from enhanced_ride_automation import RideBookingAutomation
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

file_handler = logging.FileHandler('enhanced_scheduler.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

class EnhancedRideScheduler:
    def __init__(self, config_file='config.json'):
        """Initialize enhanced scheduler"""
        self.config_file = config_file
        self.config = self.load_config()
        self.booking_history = []
        self.stats = {
            'total_bookings': 0,
            'successful_bookings': 0,
            'failed_bookings': 0,
            'last_booking_time': None,
            'next_booking_time': None
        }
        
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Failed to load config: {e}")
            raise
    
    def book_ride_job(self):
        """Main booking job with retry logic"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}🚀 Starting Scheduled Ride Booking")
        print(f"{Fore.CYAN}⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        self.stats['total_bookings'] += 1
        
        try:
            automation = RideBookingAutomation(self.config_file)
            
            retry_config = self.config.get('retry', {})
            max_attempts = retry_config.get('max_attempts', 3)
            wait_time = retry_config.get('wait_between_attempts', 300)
            
            success = False
            
            for attempt in range(1, max_attempts + 1):
                logger.info(f"{Fore.YELLOW}→ Attempt {attempt}/{max_attempts}")
                
                success = automation.run()
                
                if success:
                    logger.info(f"{Fore.GREEN}✓ Booking successful on attempt {attempt}")
                    self.stats['successful_bookings'] += 1
                    self.stats['last_booking_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    self.booking_history.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'SUCCESS',
                        'attempts': attempt,
                        'route': f"{self.config['pickup_location']} → {self.config['drop_location']}"
                    })
                    
                    self.send_success_notification()
                    break
                else:
                    logger.warning(f"{Fore.YELLOW}✗ Attempt {attempt} failed")
                    if attempt < max_attempts:
                        logger.info(f"{Fore.CYAN}⏳ Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
            
            if not success:
                self.stats['failed_bookings'] += 1
                self.booking_history.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'FAILED',
                    'attempts': max_attempts,
                    'route': f"{self.config['pickup_location']} → {self.config['drop_location']}"
                })
                
                logger.error(f"{Fore.RED}✗ All {max_attempts} attempts failed!")
                self.send_failure_notification(max_attempts)
                
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Critical error in booking job: {e}")
            self.stats['failed_bookings'] += 1
        
        self.save_stats()
        self.display_stats()
    
    def send_success_notification(self):
        """Send success notification"""
        message = f"""
🎉 RIDE BOOKED SUCCESSFULLY!

📍 Route: {self.config['pickup_location']} → {self.config['drop_location']}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🚗 Platform: {self.config.get('platform', 'ola').upper()}
✅ Status: Confirmed

Check the app for driver details!
        """
        
        print(f"{Fore.GREEN}{message}")
        
        # Send via configured channels
        self.send_multi_channel_notification(
            "✅ Ride Booked Successfully!",
            message
        )
    
    def send_failure_notification(self, attempts):
        """Send failure notification"""
        message = f"""
❌ RIDE BOOKING FAILED

📍 Route: {self.config['pickup_location']} → {self.config['drop_location']}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Attempts: {attempts}
❌ Status: Failed

Please book manually or check configuration.
        """
        
        print(f"{Fore.RED}{message}")
        
        self.send_multi_channel_notification(
            "❌ Ride Booking Failed",
            message
        )
    
    def send_multi_channel_notification(self, title, message):
        """Send notification via email and SMS"""
        # This would use the automation class's notification methods
        logger.info(f"{Fore.CYAN}📧 Notification: {title}")
    
    def display_stats(self):
        """Display booking statistics"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 BOOKING STATISTICS")
        print(f"{Fore.CYAN}{'='*70}")
        
        stats_table = [
            ["Total Bookings", self.stats['total_bookings']],
            ["Successful", f"{Fore.GREEN}{self.stats['successful_bookings']}{Style.RESET_ALL}"],
            ["Failed", f"{Fore.RED}{self.stats['failed_bookings']}{Style.RESET_ALL}"],
            ["Success Rate", f"{self.get_success_rate()}%"],
            ["Last Booking", self.stats['last_booking_time'] or 'N/A'],
            ["Next Booking", schedule.next_run() or 'N/A']
        ]
        
        print(tabulate(stats_table, headers=["Metric", "Value"], tablefmt="grid"))
        
        if self.booking_history:
            print(f"\n{Fore.CYAN}📋 RECENT BOOKING HISTORY")
            print(f"{Fore.CYAN}{'-'*70}")
            
            recent = self.booking_history[-5:]  # Last 5 bookings
            history_table = []
            
            for booking in recent:
                status_colored = f"{Fore.GREEN}✓ SUCCESS{Style.RESET_ALL}" if booking['status'] == 'SUCCESS' else f"{Fore.RED}✗ FAILED{Style.RESET_ALL}"
                history_table.append([
                    booking['timestamp'],
                    status_colored,
                    booking['attempts'],
                    booking['route']
                ])
            
            print(tabulate(history_table, 
                          headers=["Time", "Status", "Attempts", "Route"], 
                          tablefmt="grid"))
        
        print(f"{Fore.CYAN}{'='*70}\n")
    
    def get_success_rate(self):
        """Calculate success rate"""
        if self.stats['total_bookings'] == 0:
            return 0
        return round((self.stats['successful_bookings'] / self.stats['total_bookings']) * 100, 2)
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            stats_data = {
                'stats': self.stats,
                'history': self.booking_history
            }
            
            with open('booking_stats.json', 'w') as f:
                json.dump(stats_data, f, indent=2)
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Failed to save stats: {e}")
    
    def load_stats(self):
        """Load statistics from file"""
        try:
            if os.path.exists('booking_stats.json'):
                with open('booking_stats.json', 'r') as f:
                    data = json.load(f)
                    self.stats = data.get('stats', self.stats)
                    self.booking_history = data.get('history', [])
                    logger.info(f"{Fore.GREEN}✓ Previous stats loaded")
        except Exception as e:
            logger.warning(f"{Fore.YELLOW}⚠ Could not load previous stats: {e}")
    
    def setup_schedule(self):
        """Setup booking schedule"""
        daily_config = self.config.get('daily_schedule', {})
        
        if not daily_config.get('enabled', False):
            logger.warning(f"{Fore.YELLOW}⚠ Daily schedule is disabled")
            return False
        
        booking_time = daily_config.get('booking_time', '08:00')
        days = daily_config.get('days', [])
        
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
                logger.info(f"{Fore.GREEN}✓ Scheduled: {day.capitalize()} at {booking_time}")
        
        if scheduled_count == 0:
            logger.error(f"{Fore.RED}✗ No valid days scheduled")
            return False
        
        logger.info(f"{Fore.GREEN}✓ Total schedules: {scheduled_count}")
        return True
    
    def run(self):
        """Run the scheduler"""
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}🚀 Enhanced Ride Booking Scheduler")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        # Load previous stats
        self.load_stats()
        
        if not self.setup_schedule():
            logger.error(f"{Fore.RED}✗ Failed to setup schedule")
            return
        
        next_run = schedule.next_run()
        print(f"{Fore.GREEN}✓ Scheduler is running...")
        print(f"{Fore.CYAN}⏰ Next run: {next_run}")
        print(f"{Fore.YELLOW}⚠️  Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{'='*70}")
            print(f"{Fore.YELLOW}⏹️  Scheduler stopped by user")
            print(f"{Fore.YELLOW}{'='*70}")
            self.display_stats()
        except Exception as e:
            logger.error(f"{Fore.RED}✗ Scheduler error: {e}")

def main():
    """Entry point"""
    try:
        scheduler = EnhancedRideScheduler()
        scheduler.run()
    except Exception as e:
        logger.error(f"{Fore.RED}✗ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
