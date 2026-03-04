import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# --- CONFIGURATION ---
# IMPORTANT: Go to Render Dashboard -> Environment Variables
# Add a Key: MONGO_URI 
# Add the Value: (Your MongoDB Connection String)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://boraffcremix_db_user:33zxhpWWmgUWk0ce@cluster0.fftupvp.mongodb.net/?appName=Cluster0")

client = MongoClient(MONGO_URI)
db = client['bossipa_db']
apps_col = db['apps']

# --- ROUTES ---

@app.route('/')
def index():
    # Fetch all apps from MongoDB, newest first
    all_apps = list(apps_col.find().sort('_id', -1))
    return render_template('index.html', apps=all_apps)

@app.route('/admin')
def admin():
    all_apps = list(apps_col.find().sort('_id', -1))
    return render_template('admin.html', apps=all_apps)

@app.route('/add', methods=['POST'])
def add_app():
    # Get data from the Admin Form
    new_app = {
        "name": request.form.get('name'),
        "image_url": request.form.get('image_url'),
        "description": request.form.get('description'),
        "badge": request.form.get('badge'),
        "install_url": request.form.get('install_url')
    }
    apps_col.insert_one(new_app)
    return redirect(url_for('admin'))

@app.route('/delete/<app_id>')
def delete_app(app_id):
    # Delete using MongoDB ObjectId
    apps_col.delete_one({'_id': ObjectId(app_id)})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Render sets the PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
