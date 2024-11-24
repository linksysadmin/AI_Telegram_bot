import os

from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
TELEGRAM_CHANEL_ID = os.getenv("TELEGRAM_CHANEL_ID")
TELEGRAM_CHANEL_URL = os.getenv("TELEGRAM_CHANEL_URL", 'https://t.me/maks_hero_live')  # https://t.me/maks_hero_live
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
YKASSA_PAYMENT_TOKEN = os.getenv("YKASSA_PAYMENT_TOKEN")
STRIPE_PAYMENT_TOKEN = os.getenv("STRIPE_PAYMENT_TOKEN")
ADMIN_LIST = [5431876685, 7297304134, 438918925, 796204001]


# LeonardoAI
LEONARDO_AI_TOKEN = os.getenv("LEONARDO_AI_TOKEN")
# LumaAI
LUMA_API_TOKEN = os.getenv("LUMA_API_TOKEN")
# SunoAI
SUNO_COOKIE = os.getenv("SUNO_COOKIE")
SUNO_SESSION_ID = os.getenv("SUNO_SESSION_ID")
# HeiGenAI
HEIGEN_AI_TOKEN = os.getenv("HEIGEN_AI_TOKEN")


# For WEBHOOK
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEB_SERVER_HOST = '0.0.0.0'  # прослушивать все доступные интерфейсы внутри контейнера Docker
WEB_SERVER_PORT = 8080  # прослушивать порт 8080 внутри контейнера Docker

# Database and Redis
DATABASE = "sqlite+aiosqlite:///database.db"
REDIS_URL = 'redis://redis:6379/2'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, 'app', 'data', 'media')
LOCALES_DIR = os.path.join(BASE_DIR, 'app', 'data', 'locales')


DEBUG = False
