# 🚀 QUICK START GUIDE - Get Running in 5 Minutes!

## ⚡ Super Fast Setup (3 Commands)

```bash
# 1️⃣ Install everything
./setup.sh

# 2️⃣ Test it works
./test_setup.sh

# 3️⃣ Start using it
./start.sh
```

That's it! You're done! 🎉

---

## 🎯 What Each Command Does

### Command 1: `./setup.sh`
Installs:
- ✅ Python dependencies
- ✅ Chrome browser (if needed)
- ✅ Virtual environment
- ✅ Creates folders
- ✅ Sets up config files

**Time:** 2-3 minutes

### Command 2: `./test_setup.sh`
Checks:
- ✅ Python version
- ✅ All packages installed
- ✅ Chrome browser found
- ✅ Configuration valid
- ✅ Scripts executable

**Time:** 10 seconds

### Command 3: `./start.sh`
Shows menu:
```
1) Test setup
2) Book ride now ← Try this first!
3) Start daily scheduler
4) View configuration
5) Edit configuration
6) Install as service
7) Exit
```

**Time:** Interactive

---

## 📝 Before First Use - Edit Config

```bash
nano config.json
```

Change these 3 things:

```json
{
  "pickup_location": "YOUR PICKUP ADDRESS IN PUNE",
  "drop_location": "YOUR DROP ADDRESS IN MUMBAI", 
  "phone_number": "+91XXXXXXXXXX"
}
```

Save: `Ctrl+X`, then `Y`, then `Enter`

---

## 🧪 Test It (First Time)

```bash
# Start interactive menu
./start.sh

# Choose option 2: "Book a ride now"
# This will:
# 1. Open Chrome
# 2. Go to Ola website
# 3. Ask you to enter OTP
# 4. Try to book a ride
# 5. Show you if it worked
```

**Watch what happens!** This helps you understand the process.

---

## 🔄 Daily Automation

Once testing works:

```bash
./start.sh

# Choose option 3: "Start daily scheduler"

# It will book rides automatically at your set time!
# Press Ctrl+C to stop
```

---

## 📧 Add Notifications (Optional)

### Email Notifications:

```bash
nano .env
```

Add:
```bash
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Then in `config.json`:
```json
"notifications": {
  "email_enabled": true,
  "email": "your-email@gmail.com"
}
```

### SMS Notifications:

Sign up at [Twilio.com](https://www.twilio.com) (free $15 credit)

Add to `.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+1234567890
```

In `config.json`:
```json
"notifications": {
  "sms_enabled": true,
  "sms_number": "+91XXXXXXXXXX"
}
```

---

## 🎬 See It In Action

```bash
./demo.sh
```

This shows you:
- How the system works
- What notifications look like
- Sample statistics
- All available commands

---

## 🆘 Something Not Working?

### Issue: Setup fails

**Solution:**
```bash
# Update package manager
sudo apt-get update

# Install Python
sudo apt-get install python3 python3-pip python3-venv

# Try setup again
./setup.sh
```

### Issue: Chrome not found

**Solution:**
```bash
# Install Chromium
sudo apt-get install chromium-browser

# Or download Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### Issue: Can't enter OTP

**Solution:**
1. Set `"headless_mode": false` in config.json
2. Set `"keep_browser_open": true`
3. Run again - you'll see the browser and have time to enter OTP

### Issue: Booking fails

**Check:**
- ✅ Internet connection working?
- ✅ Phone number correct format: `+91XXXXXXXXXX`?
- ✅ Pickup/drop addresses complete and valid?
- ✅ Did you enter OTP correctly?

---

## 📊 Monitor Your Bookings

```bash
# Watch live logs
tail -f ride_automation.log

# See scheduler activity
tail -f enhanced_scheduler.log

# View screenshots
ls -lh screenshots/

# Check statistics
cat booking_stats.json
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Commute (Weekdays)

**config.json:**
```json
{
  "daily_schedule": {
    "enabled": true,
    "booking_time": "08:00",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }
}
```

### Use Case 2: Weekend Only

**config.json:**
```json
{
  "daily_schedule": {
    "days": ["saturday", "sunday"]
  }
}
```

### Use Case 3: Specific Days

**config.json:**
```json
{
  "daily_schedule": {
    "days": ["monday", "wednesday", "friday"]
  }
}
```

---

## 🔧 Advanced: Run as Background Service

This makes it run automatically when your computer starts!

```bash
./start.sh

# Choose option 6: "Install as system service"

# Then control with:
sudo systemctl status ride-automation  # Check status
sudo systemctl stop ride-automation    # Stop it
sudo systemctl start ride-automation   # Start it
sudo journalctl -u ride-automation -f  # View logs
```

---

## ⏱️ Timeline: What to Expect

**First Day:**
- Setup: 5 minutes
- Configuration: 2 minutes
- First test booking: 5 minutes
- **Total: ~12 minutes**

**Ongoing:**
- Daily: Fully automatic (0 minutes of your time!)
- Just check your phone for ride confirmation

---

## 🎓 Learning Path

**Day 1:** Setup and test one manual booking  
**Day 2:** Enable scheduler, watch it run once  
**Day 3:** Add notifications  
**Week 2:** Install as service for auto-start  
**Week 3:** Fully automated, hands-off! 🎉

---

## 💡 Pro Tips

1. **Test on weekend first** - Less critical if something goes wrong
2. **Start with visible browser** - Set `headless_mode: false` initially
3. **Check logs daily** - First week, verify everything
4. **Always have backup plan** - Manual booking ready
5. **Update config carefully** - Test after each change

---

## 📞 Quick Reference Card

```
┌─────────────────────────────────────────┐
│  QUICK COMMANDS                         │
├─────────────────────────────────────────┤
│  Setup:       ./setup.sh                │
│  Test:        ./test_setup.sh           │
│  Start:       ./start.sh                │
│  Demo:        ./demo.sh                 │
│                                         │
│  Book Now:    python enhanced_ride_automation.py │
│  Schedule:    python enhanced_scheduler.py       │
│                                         │
│  Logs:        tail -f *.log             │
│  Config:      nano config.json          │
└─────────────────────────────────────────┘
```

---

## ✅ Success Checklist

After following this guide:

- [ ] Ran `./setup.sh` successfully
- [ ] Ran `./test_setup.sh` - all tests passed
- [ ] Edited `config.json` with my locations
- [ ] Tested one manual booking (option 2 in menu)
- [ ] Saw Chrome open and try to book
- [ ] Entered OTP successfully
- [ ] Got confirmation or saw error message
- [ ] Understand the process

**If all checked:** You're ready for daily automation! 🎉

---

## 🚀 Next Steps

1. **Start daily automation:**
   ```bash
   ./start.sh
   # Choose option 3
   ```

2. **Or install as service:**
   ```bash
   ./start.sh
   # Choose option 6
   ```

3. **Relax!** The system handles your daily bookings! ☕

---

## 📚 More Help

- **Full details:** See `SETUP_GUIDE.md`
- **Overview:** See `README.md`
- **Demo:** Run `./demo.sh`
- **Logs:** Check `*.log` files

---

**🎊 You're all set! Happy automated commuting! 🚗💨**

*Last updated: December 8, 2025*
