import motor.motor_asyncio
import os

MONGO_USER = os.getenv("MONGO_USER", "mongo_admin")
MONGO_PASS = os.getenv("MONGO_PASS", "password")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.library_db
books_collection = db.get_collection("books")
