from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from models import MessageCreate, MessageResponse, ChatCreate, ChatResponse
from routes.auth import get_current_user
from main import db

router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

# Helper function to convert ObjectId to string
def convert_objectid(document):
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document

# Chat Routes
@router.post("/", response_model=ChatResponse)
async def create_chat(chat: ChatCreate, current_user: dict = Depends(get_current_user)):
    # Check if chat already exists between participants
    existing_chat = await db.chats.find_one({
        "participants": {"$all": chat.participants},
        "chat_type": "private"
    })
    
    if existing_chat:
        return convert_objectid(existing_chat)
    
    # Create new chat
    chat_dict = chat.dict()
    chat_dict["created_at"] = datetime.utcnow()
    chat_dict["updated_at"] = datetime.utcnow()
    
    result = await db.chats.insert_one(chat_dict)
    created_chat = await db.chats.find_one({"_id": result.inserted_id})
    return convert_objectid(created_chat)

@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    chats = await db.chats.find({"participants": user_id}).to_list(100)
    return [convert_objectid(chat) for chat in chats]

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Check if user is participant
    user_id = str(current_user["_id"])
    if user_id not in chat["participants"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this chat"
        )
    
    return convert_objectid(chat)

@router.delete("/{chat_id}")
async def delete_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Check if user is participant
    user_id = str(current_user["_id"])
    if user_id not in chat["participants"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this chat"
        )
    
    await db.chats.delete_one({"_id": ObjectId(chat_id)})
    return {"message": "Chat deleted successfully"}

# Message Routes
@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(chat_id: str, message: MessageCreate, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Create message
    message_dict = message.dict()
    message_dict["chat_id"] = chat_id
    message_dict["sender_id"] = str(current_user["_id"])
    message_dict["created_at"] = datetime.utcnow()
    message_dict["updated_at"] = datetime.utcnow()
    
    result = await db.messages.insert_one(message_dict)
    
    # Update last message in chat
    await db.chats.update_one(
        {"_id": ObjectId(chat_id)},
        {
            "$set": {
                "last_message": message.content,
                "last_message_time": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    created_message = await db.messages.find_one({"_id": result.inserted_id})
    return convert_objectid(created_message)

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(chat_id: str, current_user: dict = Depends(get_current_user), limit: int = 50):
    if not ObjectId.is_valid(chat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chat ID"
        )
    
    chat = await db.chats.find_one({"_id": ObjectId(chat_id)})
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Check if user is participant
    user_id = str(current_user["_id"])
    if user_id not in chat["participants"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this chat"
        )
    
    messages = await db.messages.find({"chat_id": chat_id}).sort("created_at", -1).limit(limit).to_list(limit)
    return [convert_objectid(message) for message in messages]

@router.put("/{chat_id}/messages/{message_id}/read")
async def mark_message_as_read(chat_id: str, message_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(message_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message ID"
        )
    
    message = await db.messages.find_one({"_id": ObjectId(message_id)})
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    await db.messages.update_one(
        {"_id": ObjectId(message_id)},
        {"$set": {"is_read": True, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Message marked as read"}
