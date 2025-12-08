# 🚗 Ola/Uber Ride Automation - Pune to Mumbai

Automate your daily ride bookings from Pune to Mumbai using Python and Selenium. This script helps you book rides on Ola or Uber automatically at scheduled times.

## ⚠️ Important Disclaimer

**This project is for educational purposes only.** Automated booking may violate the Terms of Service of Ola and Uber. Use at your own risk. The author is not responsible for any account suspension or legal issues.

## ✨ Features

- ✅ **Automated Ride Booking**: Book rides on Ola or Uber automatically
- 📅 **Daily Scheduling**: Set up recurring bookings at specific times
- 🔄 **Retry Mechanism**: Automatically retry if booking fails
- 📸 **Screenshot Capture**: Save screenshots of booking confirmations
- 📝 **Detailed Logging**: Track all actions and errors
- ⚙️ **Configurable**: Easy JSON-based configuration
- 🔔 **Notifications**: Get notified about booking status (customizable)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Internet connection
- Ola/Uber account (web-accessible)

## 🚀 Step-by-Step Installation

### Step 1: Clone or Download the Project

```bash
cd /workspaces/ola
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `selenium` - Web automation framework
- `webdriver-manager` - Automatic ChromeDriver management
- `schedule` - Job scheduling library
- `requests` - HTTP library
- `python-dotenv` - Environment variable management
- `beautifulsoup4` - HTML parsing

### Step 4: Configure Your Settings

Edit the `config.json` file with your preferences:

```json
{
  "platform": "ola",  // Options: "ola", "uber", or "both"
  "pickup_location": "Pune Railway Station, Pune",
  "drop_location": "Mumbai Central, Mumbai",
  "ride_type": "Prime",  // Options: "Mini", "Prime", "SUV" etc.
  "schedule_ride": false,
  "scheduled_time": "09:00",
  "keep_browser_open": false,
  "daily_schedule": {
    "enabled": true,
    "booking_time": "08:00",  // Time to book ride daily (24-hour format)
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  },
  "retry": {
    "enabled": true,
    "max_attempts": 3,
    "wait_between_attempts": 300  // 5 minutes in seconds
  }
}
```

### Step 5: (Optional) Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials if needed (for advanced features).

## 📖 Usage Guide

### Method 1: One-Time Manual Booking

Run the script once to book a ride immediately:

```bash
python ride_automation.py
```

The script will:
1. Open Chrome browser
2. Navigate to Ola/Uber website
3. Enter pickup and drop locations
4. Select ride type
5. Attempt to book the ride
6. Save a screenshot
7. Log all actions

### Method 2: Scheduled Daily Booking

Run the scheduler for automatic daily bookings:

```bash
python scheduler.py
```

The scheduler will:
1. Run in the background
2. Book rides at configured times
3. Retry if booking fails
4. Send notifications (if configured)
5. Log all activities

**To run scheduler in background (Linux/Mac):**

```bash
nohup python scheduler.py > scheduler_output.log 2>&1 &
```

**To stop background scheduler:**

```bash
# Find the process ID
ps aux | grep scheduler.py

# Kill the process
kill <PID>
```

### Method 3: Using Cron (Linux/Mac)

Set up a cron job for daily execution:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 8:00 AM
0 8 * * * cd /workspaces/ola && /workspaces/ola/venv/bin/python /workspaces/ola/ride_automation.py >> /workspaces/ola/cron.log 2>&1
```

### Method 4: Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (Daily at 8:00 AM)
4. Action: Start a program
5. Program: `C:\Path\To\Python\python.exe`
6. Arguments: `C:\Path\To\ride_automation.py`
7. Start in: `C:\Path\To\ola`

## 📁 Project Structure

```
ola/
├── ride_automation.py    # Main automation script
├── scheduler.py          # Daily scheduling script
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── ride_automation.log # Automation logs (created on run)
├── scheduler.log       # Scheduler logs (created on run)
└── venv/              # Virtual environment (created by you)
```

## 🔧 Configuration Options Explained

| Option | Description | Example |
|--------|-------------|---------|
| `platform` | Which service to use | `"ola"`, `"uber"`, `"both"` |
| `pickup_location` | Starting point | `"Pune Railway Station, Pune"` |
| `drop_location` | Destination | `"Mumbai Central, Mumbai"` |
| `ride_type` | Category of ride | `"Mini"`, `"Prime"`, `"SUV"` |
| `schedule_ride` | Book for later time | `true` or `false` |
| `keep_browser_open` | Debug mode | `true` or `false` |
| `daily_schedule.enabled` | Enable auto-scheduling | `true` or `false` |
| `daily_schedule.booking_time` | When to book | `"08:00"` (24-hour) |
| `daily_schedule.days` | Which days | Array of weekdays |
| `retry.max_attempts` | Retry count | `3` |

## 📊 Logs and Monitoring

### View Live Logs

```bash
# Watch automation logs
tail -f ride_automation.log

# Watch scheduler logs
tail -f scheduler.log
```

### Log Files

- `ride_automation.log` - Main script activities
- `scheduler.log` - Scheduler activities
- `*.png` - Screenshot files (timestamped)

## ❓ Troubleshooting

### Issue: ChromeDriver not found

**Solution:** The script auto-downloads ChromeDriver. Ensure you have internet connection.

```bash
pip install --upgrade webdriver-manager
```

### Issue: Elements not found on page

**Solution:** Website structure may have changed. Enable debug mode:

```json
"keep_browser_open": true
```

Then manually inspect the page elements.

### Issue: Booking fails repeatedly

**Solutions:**
1. Check if you're logged into Ola/Uber account
2. Verify pickup/drop locations are valid
3. Check internet connection
4. Try increasing wait times in the script
5. Run in non-headless mode to see what's happening

### Issue: Scheduler doesn't run

**Solution:** Check if time format is correct (24-hour) and timezone matches your system.

```bash
# Check system time
date
```

### Issue: Chrome keeps closing immediately

**Solution:** This is expected behavior. Set `keep_browser_open: true` for debugging.

## 🔒 Security Best Practices

1. **Never commit credentials** - Use `.env` file
2. **Keep logs secure** - They may contain sensitive info
3. **Use strong passwords** - For your Ola/Uber accounts
4. **Regular updates** - Keep dependencies updated

```bash
pip install --upgrade -r requirements.txt
```

## 🚀 Advanced Features

### Email Notifications

Add to `scheduler.py` in the `send_notification` method:

```python
import smtplib
from email.mime.text import MIMEText

def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'recipient@example.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email@gmail.com', 'your-app-password')
        server.send_message(msg)
```

### SMS Notifications

Use Twilio or similar service:

```bash
pip install twilio
```

## 🤝 Contributing

This is an educational project. Feel free to fork and customize for your needs.

## ⚖️ Legal Notice

- This tool is for **educational purposes only**
- Automated interactions may violate ToS of ride-sharing platforms
- Use responsibly and at your own risk
- The author assumes no liability for misuse

## 📞 Support

For issues:
1. Check the logs
2. Review troubleshooting section
3. Ensure configuration is correct
4. Test with `keep_browser_open: true`

## 🎯 Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit config.json with your locations

# 3. Test one-time booking
python ride_automation.py

# 4. Set up daily automation
python scheduler.py
```

---

**Happy Automated Commuting! 🚗💨**

*Remember: Always verify bookings manually and have a backup plan!*