from fastapi import APIRouter, HTTPException, status, Depends
from pymongo.errors import ServerSelectionTimeoutError
from app.database import get_shopacc_collection
from app.models.user import LoginCredentials
from app.auth.utils import pwd_context
from app.auth.utils import create_access_token

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(credentials: LoginCredentials, collection=Depends(get_shopacc_collection)):
    try:
        if await collection.find_one({"username": credentials.username}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        hashed_password = pwd_context.hash(credentials.password)
        user_doc = {
            "username": credentials.username,
            "password": hashed_password,
        }
        await collection.insert_one(user_doc)
        return {"message": "User registered successfully", "username": credentials.username}
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )
