import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
POINTS = int(os.getenv('POINTS'))
ADMIN_ID = os.getenv('ADMIN_ID', 309275950)
admins = [
]

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI", 'mongodb://localhost:27021'))
