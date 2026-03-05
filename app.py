from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIXED CONNECTION STRING
# If your username is "irra_admin@admin", the "@" must be changed to "%40"
MONGO_URL = "mongodb+srv://roeunbora4455_db_user:YiQws47REHYXR161@cluster0.4havjl6.mongodb.net/boss_ipa_db?retryWrites=true&w=majority"

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
    return {"message": "Connected to MongoDB & Online"}

@app.get("/apps")
async def get_apps():
    apps = []
    try:
        async for app_item in collection.find():
            apps.append(app_helper(app_item))
        return apps
    except Exception as e:
        return {"error": str(e)}

@app.post("/apps")
async def add_app(app_data: AppModel):
    new_app = app_data.dict()
    result = await collection.insert_one(new_app)
    return {"message": "App added", "id": str(result.inserted_id)}

@app.delete("/apps/{app_id}")
async def delete_app(app_id: str):
    try:
        delete_result = await collection.delete_one({"_id": ObjectId(app_id)})
        if delete_result.deleted_count == 1:
            return {"message": "App deleted"}
        raise HTTPException(status_code=404, detail="App not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# THIS ENSURES RENDER CAN SET THE PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
