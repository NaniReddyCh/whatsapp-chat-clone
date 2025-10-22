from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import socketio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="WhatsApp Chat Clone API",
    description="Backend API for WhatsApp Chat Clone application",
    version="1.0.0"
)

# Socket.IO server configuration
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    logger=True,
    engineio_logger=True
)

# Wrap FastAPI app with Socket.IO
app_asgi = socketio.ASGIApp(sio, app)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.whatsapp_clone

# Store active users
active_users = {}

@app.on_event("startup")
async def startup_db_client():
    print("Connected to MongoDB")
    print("Socket.IO server initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    print("Disconnected from MongoDB")

@app.get("/")
async def root():
    return {"message": "WhatsApp Chat Clone API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_established', {'sid': sid}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    # Remove user from active users
    user_id = active_users.pop(sid, None)
    if user_id:
        await sio.emit('user_offline', {'user_id': user_id})

@sio.event
async def user_online(sid, data):
    """
    Handle user coming online
    data: {'user_id': str, 'username': str}
    """
    user_id = data.get('user_id')
    username = data.get('username')
    
    if user_id:
        active_users[sid] = user_id
        print(f"User {username} ({user_id}) is now online")
        
        # Broadcast to all connected clients
        await sio.emit('user_online', {
            'user_id': user_id,
            'username': username
        })

@sio.event
async def user_offline(sid, data):
    """
    Handle user going offline
    data: {'user_id': str}
    """
    user_id = data.get('user_id')
    
    if user_id:
        active_users.pop(sid, None)
        print(f"User {user_id} is now offline")
        
        # Broadcast to all connected clients
        await sio.emit('user_offline', {
            'user_id': user_id
        })

@sio.event
async def send_message(sid, data):
    """
    Handle sending messages
    data: {
        'sender_id': str,
        'receiver_id': str,
        'message': str,
        'timestamp': str
    }
    """
    print(f"Message from {data.get('sender_id')} to {data.get('receiver_id')}: {data.get('message')}")
    
    # Save message to database
    message_data = {
        'sender_id': data.get('sender_id'),
        'receiver_id': data.get('receiver_id'),
        'message': data.get('message'),
        'timestamp': data.get('timestamp'),
        'read': False
    }
    
    try:
        result = await db.messages.insert_one(message_data)
        message_data['_id'] = str(result.inserted_id)
        
        # Emit receive_message event to the receiver
        await sio.emit('receive_message', message_data)
        
        # Confirm message sent to sender
        await sio.emit('message_sent', {
            'status': 'success',
            'message_id': str(result.inserted_id)
        }, room=sid)
        
    except Exception as e:
        print(f"Error saving message: {e}")
        await sio.emit('message_error', {
            'status': 'error',
            'message': str(e)
        }, room=sid)

@sio.event
async def typing(sid, data):
    """
    Handle typing indicator
    data: {'sender_id': str, 'receiver_id': str, 'is_typing': bool}
    """
    await sio.emit('typing', data)

@sio.event
async def message_read(sid, data):
    """
    Handle message read receipt
    data: {'message_id': str, 'reader_id': str}
    """
    message_id = data.get('message_id')
    
    try:
        from bson import ObjectId
        await db.messages.update_one(
            {'_id': ObjectId(message_id)},
            {'$set': {'read': True}}
        )
        
        await sio.emit('message_read', data)
    except Exception as e:
        print(f"Error updating message read status: {e}")

if __name__ == "__main__":
    import uvicorn
    # Use app_asgi instead of app to include Socket.IO
    uvicorn.run(app_asgi, host="0.0.0.0", port=8000, reload=True)
