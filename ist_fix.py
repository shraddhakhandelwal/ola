import re

# Read the file
with open('simple_ride_alerts.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add pytz import
content = content.replace(
    'import logging',
    'import logging\nimport pytz'
)

# Add IST timezone to __init__
content = content.replace(
    "        # Route configuration\n        self.route = \"Pune → Mumbai\"",
    "        # Timezone configuration - India Standard Time\n        self.ist = pytz.timezone('Asia/Kolkata')\n        \n        # Route configuration\n        self.route = \"Pune → Mumbai\""
)

# Replace all datetime.now() with datetime.now(self.ist)
content = re.sub(r'datetime\.now\(\)', 'datetime.now(self.ist)', content)

# Add IST suffix to time displays
content = re.sub(r"strftime\('%I:%M %p'\)\}", r"strftime('%I:%M %p')} IST", content)
content = re.sub(r"strftime\('%I:%M %p'\) \+", r"strftime('%I:%M %p')} IST +", content)

# Update the header
content = content.replace(
    '🚗 SIMPLE RIDE ALERTS - REAL-TIME NOTIFICATIONS',
    '🚗 SIMPLE RIDE ALERTS - REAL-TIME NOTIFICATIONS (IST)'
)

# Add timezone info to print statement
content = content.replace(
    'print(f"📱 Telegram: CONFIGURED ✅")',
    'print(f"📱 Telegram: CONFIGURED ✅")\n        print(f"🌏 Timezone: India Standard Time (IST)")'
)

# Update schedule times to mention IST
content = content.replace(
    '• 6:00 AM - Morning greeting',
    '• 6:00 AM IST - Morning greeting'
)

# Write back
with open('simple_ride_alerts.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ IST timezone added successfully!")
