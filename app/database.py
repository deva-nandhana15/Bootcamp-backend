from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "taskmanager")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI not set in environment (.env)")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# collections
users_col = db["users"]
sections_col = db["sections"]
tasks_col = db["tasks"]
