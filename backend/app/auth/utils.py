from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os, uuid, time
from app.redis import get_redis

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))  
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy() 
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({
        "exp": int(expire.timestamp()),
        "type": "access",
        "jti": str(uuid.uuid4())
    })
    encoded_access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_access_token


async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS))
    payload.update({
        "exp": int(expire.timestamp()),
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })
    encoded_refresh_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # Lưu refresh token vào Redis
    redis = get_redis()
    user_key = f"user_refresh:{payload['sub']}" 
    old_jti = await redis.get(user_key)
    if old_jti:
        await redis.delete(f"refresh:{old_jti}") 
    ttl = int(expire.timestamp() - time.time())
    await redis.setex(f"refresh:{payload['jti']}", ttl, encoded_refresh_token)
    await redis.setex(user_key, ttl, payload['jti']) 

    return encoded_refresh_token

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY, 
            algorithms=JWT_ALGORITHM
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def revoke_jti(jti: str, exp: int):
    """Store revoked token JTI in Redis with expiration"""
    redis = get_redis()
    current_time = int(time.time())
    ttl = max(exp - current_time, 1)
    await redis.setex(f"revoked:{jti}", ttl, "1")

async def is_token_revoked(jti: str):
    """Check if a token's JTI is revoked in Redis"""
    redis = get_redis()
    return bool(await redis.get(f"revoked:{jti}"))