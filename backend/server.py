from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid
from datetime import datetime
import json


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class SponsorshipRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    contact_name: str
    email: str
    phone: str = ""
    website: str = ""
    industry: str
    package_type: str
    budget: str = ""
    goals: str
    additional_info: str = ""
    status: str = "pending"  # pending, contacted, closed
    estimated_quote: int = 500
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SponsorshipRequestCreate(BaseModel):
    company_name: str
    contact_name: str
    email: str
    phone: str = ""
    website: str = ""
    industry: str
    package_type: str
    budget: str = ""
    goals: str
    additional_info: str = ""

# Admin Models
class AdminSponsorship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_name: str
    offer_name: str
    offer: str
    website: str = ""
    logo_url: str = ""
    media_url: str = ""
    release_date: str
    release_time: str
    status: str = "scheduled"  # scheduled, active, paused, expired
    created_by: str = "admin"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AdminSponsorshipCreate(BaseModel):
    business_name: str
    offer_name: str
    offer: str
    website: str = ""
    logo_url: str = ""
    media_url: str = ""
    release_date: str
    release_time: str

class UserAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: str
    email: str
    account_type: str = "free"  # free, premium
    industry: str = ""
    status: str = "active"  # active, suspended, deleted
    created_date: datetime = Field(default_factory=datetime.utcnow)

# Messaging Models
class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    sender_id: str
    sender_name: str
    recipient_id: str
    recipient_name: str
    content: str
    message_type: str = "text"  # text, image, file
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False
    delivered: bool = False

class MessageCreate(BaseModel):
    recipient_id: str
    content: str
    message_type: str = "text"

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    participants: List[str]  # List of user IDs
    participant_names: List[str]  # List of user names
    last_message: Optional[str] = ""
    last_message_timestamp: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(BaseModel):
    recipient_id: str
    recipient_name: str
    premium_granted_by: str = ""
    premium_granted_date: datetime = None

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Sponsorship endpoints
@api_router.post("/sponsorship", response_model=SponsorshipRequest)
async def create_sponsorship_request(input: SponsorshipRequestCreate):
    # Calculate estimated quote based on package type and industry
    estimated_quote = 500  # Base price
    
    if "Premium" in input.package_type:
        estimated_quote = 1500
    elif "Enterprise" in input.package_type:
        estimated_quote = 3000
    
    # Industry multipliers
    industry_multipliers = {
        'Technology': 1.2,
        'Financial Services': 1.3,
        'Healthcare': 1.1,
        'Real Estate': 1.1
    }
    
    multiplier = industry_multipliers.get(input.industry, 1.0)
    estimated_quote = int(estimated_quote * multiplier)
    
    sponsorship_dict = input.dict()
    sponsorship_obj = SponsorshipRequest(**sponsorship_dict, estimated_quote=estimated_quote)
    await db.sponsorship_requests.insert_one(sponsorship_obj.dict())
    return sponsorship_obj

@api_router.get("/sponsorship", response_model=List[SponsorshipRequest])
async def get_sponsorship_requests():
    requests = await db.sponsorship_requests.find().sort("timestamp", -1).to_list(1000)
    return [SponsorshipRequest(**request) for request in requests]

@api_router.get("/sponsorship/stats")
async def get_sponsorship_stats():
    total_requests = await db.sponsorship_requests.count_documents({})
    
    # Get industry breakdown
    pipeline = [
        {"$group": {"_id": "$industry", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    industry_stats = await db.sponsorship_requests.aggregate(pipeline).to_list(100)
    
    # Get package breakdown
    pipeline = [
        {"$group": {"_id": "$package_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    package_stats = await db.sponsorship_requests.aggregate(pipeline).to_list(100)
    
    return {
        "total_requests": total_requests,
        "industry_breakdown": industry_stats,
        "package_breakdown": package_stats
    }

# Admin endpoints (protected by admin authentication in production)
@api_router.post("/admin/sponsorship", response_model=AdminSponsorship)
async def create_admin_sponsorship(input: AdminSponsorshipCreate):
    sponsorship_dict = input.dict()
    sponsorship_obj = AdminSponsorship(**sponsorship_dict)
    await db.admin_sponsorships.insert_one(sponsorship_obj.dict())
    return sponsorship_obj

@api_router.get("/admin/sponsorship", response_model=List[AdminSponsorship])
async def get_admin_sponsorships():
    sponsorships = await db.admin_sponsorships.find().sort("timestamp", -1).to_list(1000)
    return [AdminSponsorship(**sponsorship) for sponsorship in sponsorships]

@api_router.post("/admin/user/{user_id}/upgrade")
async def admin_upgrade_user(user_id: str):
    # In production, this would update user in database
    result = {
        "user_id": user_id,
        "account_type": "premium",
        "upgraded_by": "admin",
        "upgrade_date": datetime.utcnow().isoformat()
    }
    return result

@api_router.post("/admin/user/{user_id}/downgrade")
async def admin_downgrade_user(user_id: str):
    result = {
        "user_id": user_id,
        "account_type": "free",
        "downgraded_by": "admin",
        "downgrade_date": datetime.utcnow().isoformat()
    }
    return result

@api_router.delete("/admin/user/{user_id}")
async def admin_delete_user(user_id: str):
    result = {
        "user_id": user_id,
        "status": "deleted",
        "deleted_by": "admin",
        "delete_date": datetime.utcnow().isoformat()
    }
    return result

@api_router.get("/admin/stats")
async def get_admin_stats():
    total_sponsorships = await db.admin_sponsorships.count_documents({})
    total_sponsorship_requests = await db.sponsorship_requests.count_documents({})
    
    return {
        "total_sponsorships": total_sponsorships,
        "total_sponsorship_requests": total_sponsorship_requests,
        "total_users": 1,  # Placeholder - in real app would count actual users
        "premium_users": 1,  # Placeholder
        "free_users": 0     # Placeholder
    }

# WebSocket Connection Manager for Real-time Messaging
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

# Messaging Endpoints
@api_router.post("/conversations", response_model=Conversation)
async def create_conversation(conversation_data: ConversationCreate, sender_id: str = "user"):
    # Check if conversation already exists between these users
    existing_conversation = await db.conversations.find_one({
        "participants": {"$all": [sender_id, conversation_data.recipient_id]}
    })
    
    if existing_conversation:
        return Conversation(**existing_conversation)
    
    # Create new conversation
    conversation = Conversation(
        participants=[sender_id, conversation_data.recipient_id],
        participant_names=[sender_id, conversation_data.recipient_name]
    )
    
    await db.conversations.insert_one(conversation.dict())
    return conversation

@api_router.get("/conversations", response_model=List[Conversation])
async def get_conversations(user_id: str = "user"):
    conversations = await db.conversations.find({
        "participants": user_id
    }).sort("updated_at", -1).to_list(100)
    
    return [Conversation(**conv) for conv in conversations]

@api_router.post("/messages", response_model=Message)
async def send_message(message_data: MessageCreate, sender_id: str = "user", sender_name: str = "User"):
    # Get or create conversation
    conversation = await db.conversations.find_one({
        "participants": {"$all": [sender_id, message_data.recipient_id]}
    })
    
    if not conversation:
        # Create new conversation
        new_conv = Conversation(
            participants=[sender_id, message_data.recipient_id],
            participant_names=[sender_name, message_data.recipient_id]
        )
        await db.conversations.insert_one(new_conv.dict())
        conversation_id = new_conv.id
    else:
        conversation_id = conversation["id"]
    
    # Create message
    message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        sender_name=sender_name,
        recipient_id=message_data.recipient_id,
        recipient_name=message_data.recipient_id,
        content=message_data.content,
        message_type=message_data.message_type
    )
    
    # Save message to database
    await db.messages.insert_one(message.dict())
    
    # Update conversation with last message
    await db.conversations.update_one(
        {"id": conversation_id},
        {
            "$set": {
                "last_message": message_data.content,
                "last_message_timestamp": message.timestamp,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Send real-time message to recipient if they're online
    message_data_json = json.dumps({
        "type": "new_message",
        "message": message.dict(),
        "conversation_id": conversation_id
    }, default=str)
    
    await manager.send_personal_message(message_data_json, message_data.recipient_id)
    
    return message

@api_router.get("/messages/{conversation_id}", response_model=List[Message])
async def get_messages(conversation_id: str, limit: int = 50):
    messages = await db.messages.find({
        "conversation_id": conversation_id
    }).sort("timestamp", 1).limit(limit).to_list(limit)
    
    return [Message(**msg) for msg in messages]

@api_router.put("/messages/{message_id}/read")
async def mark_message_read(message_id: str):
    await db.messages.update_one(
        {"id": message_id},
        {"$set": {"read": True}}
    )
    return {"status": "Message marked as read"}

# WebSocket endpoint for real-time messaging
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            await manager.send_personal_message(f"Echo: {data}", user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
