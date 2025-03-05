from fastapi import APIRouter, HTTPException, status, Depends
from pymongo.errors import ServerSelectionTimeoutError
from app.database import get_collection
from app.models.user import LoginCredentials
from app.auth import pwd_context

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(credentials: LoginCredentials, collection=Depends(get_collection)):
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

@router.post("/login")
async def login(credentials: LoginCredentials, collection=Depends(get_collection)):
    try:
        user = await collection.find_one({"username": credentials.username})
        if not user or not pwd_context.verify(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return {"message": "Login successful", "username": user["username"]}
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )