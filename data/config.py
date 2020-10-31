import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
POINTS = int(os.getenv('POINTS'))
ADMIN_ID = os.getenv('ADMIN_ID')
admins = [
]

REDIS_HOST = os.getenv("REDIS_HOST", "redis://localhost")
