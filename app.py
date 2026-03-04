from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URL = "mongodb+srv://irra_admin@admin:IaRlmLx6xMAmVzRg@cluster0.fftupvp.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["boss_ipa_db"]
collection = db["apps"]

# Data Model
class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

# Helper to convert MongoDB format to JSON
def app_helper(app_item) -> dict:
    return {
        "id": str(app_item["_id"]),
        "title": app_item["title"],
        "description": app_item["description"],
        "tag": app_item["tag"],
        "image": app_item["image"],
        "download_url": app_item["download_url"],
    }

@app.get("/")
async def root():
    return {"message": "Connected to MongoDB & Online"}

# 1. GET ALL APPS FROM DATABASE
@app.get("/apps")
async def get_apps():
    apps = []
    async for app_item in collection.find():
        apps.append(app_helper(app_item))
    return apps

# 2. ADD APP TO DATABASE
@app.post("/apps")
async def add_app(app_data: AppModel):
    new_app = app_data.dict()
    result = await collection.insert_one(new_app)
    return {"message": "App added to MongoDB", "id": str(result.inserted_id)}

# 3. DELETE APP FROM DATABASE
@app.delete("/apps/{app_id}")
async def delete_app(app_id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(app_id)})
    if delete_result.deleted_count == 1:
        return {"message": "App deleted"}
    raise HTTPException(status_code=404, detail="App not found")
