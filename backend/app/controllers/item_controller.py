from fastapi import APIRouter, HTTPException, status, Depends
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from app.database import get_tuoi_collection
from app.models.item import Item
from app.serializer import convert_doc, convert_doc_list
from typing import List

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, collection=Depends(get_tuoi_collection)):
    try:
        await collection.insert_one(item.model_dump())
        return {"message": "Item created", "item": item}
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.get("/", response_model=List[Item])
async def read_items(collection=Depends(get_tuoi_collection)):
    try:
        items = await collection.find().to_list(length=100)
        return convert_doc_list(items)
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.put("/{name}")
async def update_item(name: str, item: Item, collection=Depends(get_tuoi_collection)):
    try:
        updated_item = await collection.find_one_and_update(
            {"name": name},
            {"$set": item.model_dump()},
            return_document=ReturnDocument.AFTER
        )
        if updated_item:
            return {"message": "Item updated", "item": convert_doc(updated_item)}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {name} not found"
        )
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

@router.delete("/{name}")
async def delete_item(name: str, collection=Depends(get_tuoi_collection)):
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