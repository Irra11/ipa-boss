from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Enable CORS so Vercel can talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple Data Store (In a real app, use MongoDB or PostgreSQL)
# Note: Render's free tier resets disk, so this is for demo. 
# For permanent storage, connect a free MongoDB Atlas URI.
apps_db = [
    {
        "id": 1,
        "title": "YouTube Premium",
        "description": "Premium Unlocked",
        "tag": "PRO UNLOCKED",
        "image": "https://play-lh.googleusercontent.com/6am0i3walYwNLc08QOOhRJttQENNGkhlKajXSERf3JnPVRQczIyxw2w3DxeMRTOSdsY=s48-rw",
        "download_url": "https://github.com/Irra11/appname-install/releases/download/v1.0.0/YouTube-BossIPA.ipa"
    }
]

class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

ADMIN_PASSWORD = "1111" # Change this!

@app.get("/apps")
def get_apps():
    return apps_db

@app.post("/apps")
def add_app(app_data: AppModel, password: str = Header(None)):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    new_app = app_data.dict()
    new_app["id"] = len(apps_db) + 1
    apps_db.append(new_app)
    return {"message": "App added successfully"}

@app.delete("/apps/{app_id}")
def delete_app(app_id: int, password: str = Header(None)):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    global apps_db
    apps_db = [a for a in apps_db if a["id"] != app_id]
    return {"message": "Deleted"}
