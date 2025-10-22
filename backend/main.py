from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="WhatsApp Chat Clone API",
    description="Backend API for WhatsApp Chat Clone application",
    version="1.0.0"
)

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

@app.on_event("startup")
async def startup_db_client():
    print("Connected to MongoDB")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
