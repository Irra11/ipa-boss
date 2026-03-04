import os
import uvicorn
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# IMPORTANT: Allow Vercel to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

apps_db = [] # This will clear every time Render sleeps. 

class AppModel(BaseModel):
    title: str
    description: str
    tag: str
    image: str
    download_url: str

@app.get("/")
def home():
    return {"status": "Backend is running!"}

@app.get("/apps")
def get_apps():
    return apps_db

@app.post("/apps")
def add_app(app_data: AppModel):
    new_app = app_data.dict()
    new_app["id"] = len(apps_db) + 1
    apps_db.append(new_app)
    return {"message": "Success"}

# This block is only for local testing, Render uses the Start Command
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
