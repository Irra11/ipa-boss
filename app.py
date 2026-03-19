from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection (SYNC)
MONGO_URL = "mongodb+srv://roeunbora4455_db_user:wjEPJ4R8lJQCCT4s@cluster0.qoiwskv.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client["boss_ipa_db"]
collection = db["apps"]

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

# Root
@app.get("/")
def root():
    return {"message": "Boss IPA Backend Online"}

# GET ALL APPS
@app.get("/apps")
def get_apps():
    apps = []
    for app_item in collection.find():
        apps.append(app_helper(app_item))
    return apps

# ADD NEW APP
@app.post("/apps")
def add_app(app_data: AppModel):
    new_app = app_data.dict()
    result = collection.insert_one(new_app)
    return {"message": "Added", "id": str(result.inserted_id)}

# UPDATE APP
@app.put("/apps/{app_id}")
def update_app(app_id: str, app_data: AppModel):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection.update_one(
        {"_id": ObjectId(app_id)},
        {"$set": app_data.dict()}
    )

    if result.modified_count == 1:
        return {"message": "Updated successfully"}

    raise HTTPException(status_code=404, detail="App not found or no changes made")

# DELETE APP
@app.delete("/apps/{app_id}")
def delete_app(app_id: str):
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = collection.delete_one({"_id": ObjectId(app_id)})

    if result.deleted_count == 1:
        return {"message": "Deleted"}

    raise HTTPException(status_code=404, detail="App not found")
