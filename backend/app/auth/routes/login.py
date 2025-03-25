from fastapi import APIRouter, HTTPException, status, Depends
from pymongo.errors import ServerSelectionTimeoutError
from app.database import get_shopacc_collection
from app.models.user import LoginCredentials
from app.pwd_hash import pwd_context
from app.auth.utils import create_access_token

router = APIRouter()

@router.post("/login")
async def login(credentials: LoginCredentials, collection=Depends(get_shopacc_collection)):
    try:
        user = await collection.find_one({"username": credentials.username})
        if not user or not pwd_context.verify(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        access_token = create_access_token(data = {"sub": user["username"]})
        # refresh_token = create_access_token(data = {"sub": user["username"]})
        
        return {"access_token": access_token,
                
                "token_type": "bearer",
                "message": "Login successful",
                "username": user["username"]}
 
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )