# 🚗 Ola/Uber Ride Automation - Production Ready Setup

## Complete Real-Time Working System for Pune to Mumbai Daily Rides

This is a **production-ready, real-time** ride automation system with OTP login, notifications, monitoring, and scheduling.

---

## ✨ NEW: Enhanced Features

### 🔥 Real-Time Capabilities
- ✅ **Actual OTP Login** - Real phone number and OTP verification
- 📧 **Email Notifications** - Get notified via email (Gmail/SMTP)
- 📱 **SMS Notifications** - SMS alerts via Twilio
- 📊 **Live Statistics** - Track booking success rate and history
- 🎨 **Colored Output** - Beautiful terminal interface
- 🔄 **Smart Retry Logic** - Automatic retry with exponential backoff
- 📸 **Screenshot Evidence** - Auto-save booking confirmations
- 🛡️ **Anti-Detection** - Advanced browser fingerprint protection

---

## 🚀 One-Command Setup

### Quick Start (Automated):

```bash
chmod +x setup.sh start.sh test_setup.sh
./setup.sh
```

This will:
1. ✅ Check Python 3.8+
2. ✅ Install Chrome/Chromium
3. ✅ Create virtual environment
4. ✅ Install all dependencies
5. ✅ Setup configuration files
6. ✅ Create necessary directories

---

## 📋 Step-by-Step Manual Setup

### Step 1: Install Dependencies

```bash
# Make scripts executable
chmod +x setup.sh start.sh test_setup.sh

# Run automated setup
./setup.sh
```

### Step 2: Configure Your Details

Edit `config.json`:

```json
{
  "platform": "ola",
  "pickup_location": "Pune Railway Station, Pune, Maharashtra",
  "drop_location": "Mumbai Central, Mumbai, Maharashtra",
  "phone_number": "+919876543210",  // YOUR PHONE
  "daily_schedule": {
    "enabled": true,
    "booking_time": "08:00",  // When to book daily
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }
}
```

### Step 3: Setup Notifications (Optional)

Edit `.env` for email/SMS:

```bash
# Email (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Generate from Google Account

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Ola/Uber
OLA_PHONE=+919876543210
```

### Step 4: Test Everything

```bash
./test_setup.sh
```

You should see:
```
✓ PASS: Python 3.10
✓ PASS: All required packages installed
✓ PASS: config.json is valid JSON
✓ PASS: Route configured: Pune → Mumbai
✓ PASS: Chrome found
✅ All tests passed!
```

---

## 🎯 Usage - Multiple Ways

### Option 1: Interactive Menu (Easiest)

```bash
./start.sh
```

Choose from menu:
1. Test setup
2. Book ride now
3. Start daily scheduler
4. View/edit config
5. Install as service

### Option 2: One-Time Booking (Manual)

```bash
source venv/bin/activate
python enhanced_ride_automation.py
```

**What happens:**
1. Opens Chrome browser
2. Goes to Ola website
3. Asks for OTP (you enter it)
4. Fills pickup: Pune Railway Station
5. Fills drop: Mumbai Central
6. Selects ride type
7. Books the ride
8. Takes screenshots
9. Sends notifications

### Option 3: Daily Automated Booking

```bash
source venv/bin/activate
python enhanced_scheduler.py
```

**What happens:**
- Runs in background
- Books ride at 8:00 AM daily (configurable)
- Retries 3 times if fails
- Sends email/SMS notifications
- Logs everything
- Shows live statistics

### Option 4: Run as Linux Service (Background)

```bash
./start.sh
# Choose option 6

# Then manage with:
sudo systemctl status ride-automation
sudo systemctl stop ride-automation
sudo systemctl start ride-automation
sudo journalctl -u ride-automation -f  # View logs
```

---

## 📊 Real-Time Monitoring

### View Live Statistics

The scheduler shows:

```
📊 BOOKING STATISTICS
╔═══════════════════╦════════╗
║ Metric            ║ Value  ║
╠═══════════════════╬════════╣
║ Total Bookings    ║ 15     ║
║ Successful        ║ 14     ║
║ Failed            ║ 1      ║
║ Success Rate      ║ 93.33% ║
║ Last Booking      ║ 2025-12-08 08:00:15 ║
║ Next Booking      ║ 2025-12-09 08:00:00 ║
╚═══════════════════╩════════╝

📋 RECENT BOOKING HISTORY
╔═════════════════════╦══════════╦══════════╦═══════════════════╗
║ Time                ║ Status   ║ Attempts ║ Route             ║
╠═════════════════════╬══════════╬══════════╬═══════════════════╣
║ 2025-12-08 08:00:15 ║ ✓ SUCCESS║ 1        ║ Pune → Mumbai     ║
╚═════════════════════╩══════════╩══════════╩═══════════════════╝
```

### Check Logs

```bash
# Automation logs
tail -f ride_automation.log

# Scheduler logs
tail -f enhanced_scheduler.log

# Service logs (if running as service)
sudo journalctl -u ride-automation -f
```

### View Screenshots

```bash
ls -lh screenshots/
# ola_before_booking_20251208_080015.png
# ola_confirmation_20251208_080025.png
```

---

## 🔧 Configuration Reference

### config.json Fields

| Field | Description | Example |
|-------|-------------|---------|
| `platform` | Service to use | `"ola"` or `"uber"` |
| `pickup_location` | Starting point (full address) | `"Pune Railway Station, Pune, Maharashtra"` |
| `drop_location` | Destination (full address) | `"Mumbai Central, Mumbai, Maharashtra"` |
| `phone_number` | Your phone for OTP | `"+919876543210"` |
| `ride_type` | Category | `"Mini"`, `"Prime"`, `"SUV"` |
| `headless_mode` | Hide browser window | `true` or `false` |
| `daily_schedule.enabled` | Enable automation | `true` or `false` |
| `daily_schedule.booking_time` | When to book (24h) | `"08:00"` |
| `daily_schedule.days` | Active days | `["monday", "tuesday", ...]` |
| `notifications.email_enabled` | Enable email alerts | `true` or `false` |
| `notifications.sms_enabled` | Enable SMS alerts | `true` or `false` |
| `retry.max_attempts` | Retry count | `3` |

---

## 📧 Setting Up Notifications

### Email Notifications (Gmail)

1. **Enable 2-Step Verification** in your Google Account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → "Ride Automation"
   - Copy the 16-character password

3. **Add to `.env`**:
```bash
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Your app password
```

4. **Enable in `config.json`**:
```json
"notifications": {
  "email_enabled": true,
  "email": "your-email@gmail.com"
}
```

### SMS Notifications (Twilio)

1. **Sign up** at https://www.twilio.com/
2. **Get free trial** ($15 credit)
3. **Get credentials** from Dashboard
4. **Add to `.env`**:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

5. **Enable in `config.json`**:
```json
"notifications": {
  "sms_enabled": true,
  "sms_number": "+919876543210"
}
```

---

## 🛠️ Troubleshooting

### Issue: "ChromeDriver not found"

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

### Issue: "Login failed"

**Solution:**
1. Run with `headless_mode: false` to see browser
2. Check phone number format: `+91XXXXXXXXXX`
3. Ensure you enter correct OTP within time

### Issue: "Elements not found"

**Solution:**
Website may have changed. Update selectors in code or:
1. Enable debug mode: `"keep_browser_open": true`
2. Take screenshot and report issue

### Issue: Scheduler not running at correct time

**Solution:**
```bash
# Check system time
date

# Check timezone
timedatectl

# Adjust if needed
sudo timedatectl set-timezone Asia/Kolkata
```

### Issue: Booking fails every time

**Checklist:**
- [ ] Internet connection stable?
- [ ] Chrome browser installed?
- [ ] Phone number correct in config?
- [ ] Logged into Ola/Uber account?
- [ ] Route exists (Pune → Mumbai)?
- [ ] Check logs for specific error

---

## 📁 Complete File Structure

```
ola/
├── enhanced_ride_automation.py  # Main automation script (PRODUCTION)
├── enhanced_scheduler.py        # Scheduler with monitoring
├── ride_automation.py           # Basic version (legacy)
├── scheduler.py                 # Basic scheduler (legacy)
├── config.json                  # Your configuration ⚙️
├── requirements.txt             # Python dependencies
├── .env                         # Credentials (create from .env.example)
├── .env.example                 # Template
├── .gitignore                   # Git ignore rules
├── setup.sh                     # Automated setup script 🚀
├── start.sh                     # Interactive menu
├── test_setup.sh               # Test and validate
├── ride-automation.service      # Systemd service file
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup (this file)
├── venv/                        # Virtual environment
├── screenshots/                 # Booking screenshots 📸
├── logs/                        # Log files 📝
├── ride_automation.log         # Automation logs
├── enhanced_scheduler.log      # Scheduler logs
└── booking_stats.json          # Statistics database
```

---

## 🎯 Real-World Usage Example

### Scenario: Daily Pune to Mumbai Commute

**Your requirement:**
- Travel from Pune to Mumbai every weekday
- Want ride booked at 8:00 AM
- Need confirmation via SMS

**Setup (5 minutes):**

```bash
# 1. Initial setup
./setup.sh

# 2. Edit config
nano config.json
# Set: pickup_location, drop_location, phone_number
# Set: booking_time to "08:00"
# Set: days to ["monday", "tuesday", "wednesday", "thursday", "friday"]

# 3. Setup SMS (optional)
nano .env
# Add Twilio credentials

# 4. Test
./test_setup.sh

# 5. Install as service (runs on boot)
./start.sh
# Choose option 6
```

**Result:**
- Every weekday at 8:00 AM
- System automatically books your ride
- You get SMS: "✅ Ride Booked Successfully!"
- If it fails, retries 2 more times
- All activity logged

---

## 🔒 Security Best Practices

1. **Never commit `.env`** - Contains credentials
2. **Use app passwords** - Not your main password
3. **Enable 2FA** - On Ola/Uber accounts
4. **Secure logs** - May contain phone numbers
5. **Regular updates**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🆘 Getting Help

### Check logs first:
```bash
tail -f ride_automation.log
tail -f enhanced_scheduler.log
```

### Run in debug mode:
```json
{
  "headless_mode": false,
  "keep_browser_open": true
}
```

### Test configuration:
```bash
./test_setup.sh
```

---

## 📈 Performance Tips

1. **Headless mode** - Faster, less resource usage:
   ```json
   "headless_mode": true
   ```

2. **Reduce retry wait time** - Faster retries:
   ```json
   "retry": {
     "wait_between_attempts": 180
   }
   ```

3. **Run as service** - Automatic start on boot
4. **Monitor stats** - Check `booking_stats.json`

---

## 🎉 Success Checklist

After setup, you should have:

- [x] All tests passing (`./test_setup.sh`)
- [x] Config file with your routes
- [x] Phone number configured
- [x] Chrome browser installed
- [x] One successful test booking
- [x] Scheduler running (optional)
- [x] Notifications working (optional)

---

## 🚀 Quick Commands Reference

```bash
# Setup
./setup.sh                    # Initial setup
./test_setup.sh              # Validate setup

# Run
./start.sh                    # Interactive menu
python enhanced_ride_automation.py  # One-time booking
python enhanced_scheduler.py        # Start scheduler

# Service (Linux)
sudo systemctl start ride-automation
sudo systemctl status ride-automation
sudo systemctl stop ride-automation
sudo journalctl -u ride-automation -f

# Logs
tail -f ride_automation.log
tail -f enhanced_scheduler.log
ls -lh screenshots/

# Maintenance
pip install --upgrade -r requirements.txt  # Update deps
git pull                                    # Update code
```

---

## 💡 Pro Tips

1. **Test before automating** - Run manual booking first
2. **Start with one day** - Test Monday only, then expand
3. **Check daily** - First week, verify bookings manually
4. **Backup plan** - Always have manual booking ready
5. **Monitor logs** - Watch for patterns in failures
6. **Update regularly** - Websites change, update code

---

## ⚖️ Legal & Ethical Notice

- ✅ **Educational purposes only**
- ⚠️ **May violate Terms of Service** of ride platforms
- ⚠️ **Use at your own risk**
- ⚠️ **Author not liable** for account suspension
- ✅ **Always verify bookings manually**
- ✅ **Have backup transportation plan**

---

## 🎊 You're All Set!

Your complete ride automation system is ready! 🚗💨

**Next:** Run `./start.sh` and choose an option to get started!

---

*Last Updated: December 8, 2025*
*Version: 2.0 - Production Ready*
