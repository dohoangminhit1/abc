from redis.asyncio import Redis
from dotenv import load_dotenv
import os
from fastapi import FastAPI

load_dotenv()

redis = None
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

async def connect_to_redis():
    global redis
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    await redis.ping()  # Kiểm tra kết nối
    print(f"Connected to Redis at {REDIS_URL}")

async def close_redis_connection():
    global redis
    if redis:
        await redis.close()
        print("Redis connection closed")

def get_redis():
    if not redis:
        raise RuntimeError("Redis connection not initialized")
    return redis