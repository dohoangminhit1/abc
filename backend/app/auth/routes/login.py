from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo.errors import ServerSelectionTimeoutError
from app.database import get_shopacc_collection
from datetime import datetime, timezone
from app.auth.utils import pwd_context
from app.auth.utils import create_access_token, create_refresh_token
from app.redis import get_redis
from app.auth.utils import revoke_jti
from dotenv import load_dotenv
import os
router = APIRouter()

load_dotenv()
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS', '7'))

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), collection=Depends(get_shopacc_collection)):
    try:
        user = await collection.find_one({"username": form_data.username})
        if not user or not pwd_context.verify(form_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        access_token = create_access_token(data={"sub": user["username"]})
        refresh_token = await create_refresh_token(data={"sub": user["username"]})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "message": "Login successful",
            "username": user["username"]
        }
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )