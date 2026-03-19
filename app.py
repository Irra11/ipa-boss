from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
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
# serverSelectionTimeoutMS=5000 is REQUIRED so the app doesn't hang on Free Plans
MONGO_URL = "mongodb+srv://roeunbora4455_db_user:wjEPJ4R8lJQCCT4s@cluster0.qoiwskv.mongodb.net/?appName=Cluster0"

try:
    # We use the standard MongoClient because it works best with the WSGI bridge
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client["boss_ipa_db"]
    collection = db["apps"]
except Exception as e:
    print(f"Database connection setup error: {e}")

# Model
class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

# Helper
def app_helper(app_item) -> dict:
    return {
        "id": str(app_item["_id"]),
        "title": app_item.get("title", ""),
        "description": app_item.get("description", ""),
        "tag": app_item.get("tag", ""),
        "image": app_item.get("image", ""),
        "download_url": app_item.get("download_url", ""),
    }

# Root route - This will work even on Free Accounts
@app.get("/")
def root():
    return {
        "message": "Boss IPA Backend Online",
        "status": "Running",
        "note": "If /apps shows a Database Error, your Free Account is blocking MongoDB."
    }

# GET ALL APPS
@app.get("/apps")
def get_apps():
    try:
        apps = []
        # This will trigger the timeout error if on a free plan
        for app_item in collection.find():
            apps.append(app_helper(app_item))
        return apps
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# ADD NEW APP
@app.post("/apps")
def add_app(app_data: AppModel):
    try:
        new_app = app_data.model_dump() 
        result = collection.insert_one(new_app)
        return {"message": "Added", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# UPDATE APP
@app.put("/apps/{app_id}")
def update_app(app_id: str, app_data: AppModel):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    try:
        result = collection.update_one(
            {"_id": ObjectId(app_id)},
            {"$set": app_data.model_dump()}
        )
        if result.modified_count == 1:
            return {"message": "Updated successfully"}
        raise HTTPException(status_code=404, detail="App not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE APP
@app.delete("/apps/{app_id}")
def delete_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    try:
        result = collection.delete_one({"_id": ObjectId(app_id)})
        if result.deleted_count == 1:
            return {"message": "Deleted"}
        raise HTTPException(status_code=404, detail="App not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
