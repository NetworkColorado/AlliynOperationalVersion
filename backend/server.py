from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime


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
