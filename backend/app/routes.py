from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError, DuplicateKeyError, ServerSelectionTimeoutError
from app.database import collection
from app.auth import pwd_context
from app.serializer import convert_doc, convert_doc_list
from typing import List, Optional

router = APIRouter()

# Enhanced Pydantic models with validation
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)
    que: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 30,
                "que": "Sample question"
            }
        }

class LoginCredentials(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "strongpassword123"
            }
        }

# CRUD Operations
@router.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    try:
        await collection.insert_one(item.model_dump())
        return {"message": "Item created", "item": item}
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.get("/items/")
async def read_items():
    try:
        items = await collection.find().to_list(length=100)
        return {"items": convert_doc_list(items)}
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.put("/items/{name}")
async def update_item(name: str, item: Item):
    try:
        updated_item = await collection.find_one_and_update(
            {"name": name},
            {"$set": item.model_dump()},
            return_document=ReturnDocument.AFTER
        )
        if updated_item:
            return {
                "message": "Item updated",
                "item": convert_doc(updated_item)
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {name} not found"
        )
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.delete("/items/{name}")
async def delete_item(name: str):
    try:
        deleted_item = await collection.delete_one({"name": name})
        if deleted_item.deleted_count:
            return {"message": f"Item {name} deleted successfully"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {name} not found"
        )
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

# Authentication routes
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(credentials: LoginCredentials):
    try:
        if await collection.find_one({"username": credentials.username}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        if await collection.find_one({"email": credentials.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = pwd_context.hash(credentials.password)
        user_doc = {
            "username": credentials.username,
            "email": credentials.email,
            "password": hashed_password,
        }
        await collection.insert_one(user_doc)
        return {
            "message": "User registered successfully",
            "username": credentials.username
        }
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.post("/login")
async def login(credentials: LoginCredentials):
    try:
        user = await collection.find_one({"username": credentials.username})
        if not user or not pwd_context.verify(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return {
            "message": "Login successful",
            "username": user["username"],
            "email": user["email"]
        }
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )
