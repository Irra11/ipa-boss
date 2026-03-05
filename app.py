from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import uvicorn

app = FastAPI()

# Enable CORS for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URL = "mongodb+srv://roeunbora4455_db_user:wjEPJ4R8lJQCCT4s@cluster0.qoiwskv.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["boss_ipa_db"]
collection = db["apps"]

class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

def app_helper(app_item) -> dict:
    return {
        "id": str(app_item["_id"]),
        "title": app_item.get("title", ""),
        "description": app_item.get("description", ""),
        "tag": app_item.get("tag", ""),
        "image": app_item.get("image", ""),
        "download_url": app_item.get("download_url", ""),
    }

@app.get("/")
async def root():
    return {"message": "Boss IPA Backend Online"}

# GET ALL APPS
@app.get("/apps")
async def get_apps():
    apps = []
    async for app_item in collection.find():
        apps.append(app_helper(app_item))
    return apps

# ADD NEW APP
@app.post("/apps")
async def add_app(app_data: AppModel):
    new_app = app_data.dict()
    result = await collection.insert_one(new_app)
    return {"message": "Added", "id": str(result.inserted_id)}

# UPDATE/EDIT APP
@app.put("/apps/{app_id}")
async def update_app(app_id: str, app_data: AppModel):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    update_result = await collection.update_one(
        {"_id": ObjectId(app_id)}, 
        {"$set": app_data.dict()}
    )
    
    if update_result.modified_count == 1:
        return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="App not found or no changes made")

# DELETE APP
@app.delete("/apps/{app_id}")
async def delete_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    delete_result = await collection.delete_one({"_id": ObjectId(app_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="App not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
