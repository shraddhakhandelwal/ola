# Ola/Uber Driver Ride Alert System

Smart ride demand prediction system for Ola/Uber drivers on Pune-Mumbai route.

## 🔒 Security Setup

### 1. Create `.env` file

Create a file named `.env` in the project root with your credentials:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Ola API Configuration (Optional)
OLA_CLIENT_ID=your_ola_client_id_here
OLA_CLIENT_SECRET=your_ola_client_secret_here
```

### 2. Get Your Telegram Credentials

1. **Create Telegram Bot:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID:**
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your `chat_id` in the response

### 3. Get Ola API Credentials (Optional)

1. Register at [Ola Developer Portal](https://developer.olacabs.com/)
2. Create an application
3. Get your Client ID and Client Secret

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/shraddhakhandelwal/ola.git
cd ola

# 2. Create .env file with your credentials (see above)
nano .env

# 3. Install dependencies
pip install requests schedule pytz

# 4. Run the smart ride predictor
python3 smart_ride_predictor.py
```

## 📱 Features

- **Smart Demand Prediction**: Predicts high-demand periods based on real travel patterns
- **Telegram Notifications**: Instant alerts with clickable driver portal links
- **IST Timezone**: All times in India Standard Time
- **Privacy**: All credentials stored securely in `.env` file

## ⏰ Alert Schedule

- **Morning Briefing**: 6:00 AM IST
- **High Demand Alerts**: When probability ≥ 65%
- **Evening Summary**: 10:00 PM IST

## 🔐 Security Notes

- **Never commit `.env` file** to Git
- `.env` is already in `.gitignore`
- Credentials are loaded from `.env` at runtime
- Repository can be made private on GitHub

## 📊 Files

- `smart_ride_predictor.py` - Main prediction system
- `config_loader.py` - Secure configuration loader
- `.env` - Your credentials (NOT in Git)
- `.gitignore` - Excludes sensitive files

## 🛡️ Making Repository Private

1. Go to GitHub repository settings
2. Scroll to "Danger Zone"
3. Click "Change visibility"
4. Select "Make private"

## 📞 Support

For issues or questions, check the logs:
- `smart_ride_predictor.log`
- `real_ride_monitor.log`

---

**Important**: Keep your `.env` file secure and never share your API credentials!
