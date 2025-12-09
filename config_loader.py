"""
Configuration Loader - Loads sensitive data from .env file
"""
import os
from pathlib import Path

def load_config():
    """Load configuration from .env file"""
    config = {}
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    else:
        # Fallback to environment variables
        config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN', '')
        config['TELEGRAM_CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID', '')
        config['OLA_CLIENT_ID'] = os.getenv('OLA_CLIENT_ID', '')
        config['OLA_CLIENT_SECRET'] = os.getenv('OLA_CLIENT_SECRET', '')
    
    return config

def get_telegram_config():
    """Get Telegram configuration"""
    config = load_config()
    return {
        'bot_token': config.get('TELEGRAM_BOT_TOKEN'),
        'chat_id': config.get('TELEGRAM_CHAT_ID')
    }

def get_ola_config():
    """Get Ola API configuration"""
    config = load_config()
    return {
        'client_id': config.get('OLA_CLIENT_ID'),
        'client_secret': config.get('OLA_CLIENT_SECRET')
    }
