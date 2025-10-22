from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from models import UserResponse
from routes.auth import get_current_user
from main import db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Helper function to convert ObjectId to string
def convert_objectid(document):
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document

@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_user), skip: int = 0, limit: int = 100):
    users = await db.users.find().skip(skip).limit(limit).to_list(limit)
    return [convert_objectid(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return convert_objectid(user)

@router.get("/search/{query}", response_model=List[UserResponse])
async def search_users(query: str, current_user: dict = Depends(get_current_user), limit: int = 20):
    # Search by username or email
    users = await db.users.find({
        "$or": [
            {"username": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}},
            {"full_name": {"$regex": query, "$options": "i"}}
        ]
    }).limit(limit).to_list(limit)
    
    return [convert_objectid(user) for user in users]

@router.put("/me")
async def update_profile(user_data: dict, current_user: dict = Depends(get_current_user)):
    # Remove sensitive fields that shouldn't be updated
    user_data.pop("password", None)
    user_data.pop("email", None)
    user_data["updated_at"] = datetime.utcnow()
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": user_data}
    )
    
    updated_user = await db.users.find_one({"_id": current_user["_id"]})
    return convert_objectid(updated_user)

@router.put("/me/status")
async def update_status(status_data: dict, current_user: dict = Depends(get_current_user)):
    if "status" not in status_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status field is required"
        )
    
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"status": status_data["status"], "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Status updated successfully", "status": status_data["status"]}

@router.delete("/me")
async def delete_account(current_user: dict = Depends(get_current_user)):
    # Delete user's messages
    await db.messages.delete_many({"sender_id": str(current_user["_id"])})
    
    # Delete user's chats
    await db.chats.delete_many({"participants": str(current_user["_id"])})
    
    # Delete user account
    await db.users.delete_one({"_id": current_user["_id"]})
    
    return {"message": "Account deleted successfully"}
