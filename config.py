import os

from dotenv import load_dotenv

load_dotenv()

# Database and Redis
DATABASE = "sqlite+aiosqlite:///database.db"
REDIS_URL = os.getenv("REDIS_URL")

# Telegram Bot
TELEGRAM_CHANEL_ID = os.getenv("TELEGRAM_CHANEL_ID")
TELEGRAM_CHANEL_URL = os.getenv("TELEGRAM_CHANEL_URL", 'https://t.me/maks_hero_live')  # https://t.me/maks_hero_live
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
ADMIN_LIST = [5431876685, 7297304134]

# LeonardoAI
LEONARDO_AI_TOKEN = os.getenv("LEONARDO_AI_TOKEN")


# For WEBHOOK
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
WEBHOOK_PATH = f'/{TELEGRAM_TOKEN}'
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))

DEBUG = os.getenv('DEBUG', True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'app', 'media_examples')
