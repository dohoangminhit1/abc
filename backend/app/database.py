from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://minh:minh@cbd.zumeo.mongodb.net/?retryWrites=true&w=majority&appName=cbd")

client = AsyncIOMotorClient(MONGO_URI)

database_shopacc = client["shopacc"]
database_tuoi = client["tuoi"]

def get_shopacc_collection():
    return database_shopacc["shopacc"]

def get_tuoi_collection():
    return database_tuoi["tuoi"]
