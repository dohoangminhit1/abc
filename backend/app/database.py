from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
mongo_uri = "mongodb+srv://minh:minh@cbd.zumeo.mongodb.net/?retryWrites=true&w=majority&appName=cbd"
MONGO_URI = os.getenv("MONGO_URI", mongo_uri)
client = AsyncIOMotorClient(MONGO_URI)
database = client["shopacc"]
collection = database["shopacc"]
