from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# Enable CORS for your Vercel site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This stores your apps in memory
apps_db = []

class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

# 1. Test Route (Open this in your browser)
@app.get("/")
def read_root():
    return {"status": "Boss IPA Backend is Online!"}

# 2. Get all apps
@app.get("/apps")
def get_apps():
    return apps_db

# 3. Add a new app
@app.post("/apps")
def add_app(app_data: AppModel):
    new_app = app_data.dict()
    new_app["id"] = len(apps_db) + 1
    apps_db.append(new_app)
    return {"message": "App added successfully", "app": new_app}

# 4. Delete an app
@app.delete("/apps/{app_id}")
def delete_app(app_id: int):
    global apps_db
    apps_db = [a for a in apps_db if a["id"] != app_id]
    return {"message": "Deleted"}
