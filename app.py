import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# --- CONFIGURATION ---
# Set MONGO_URI in Render -> Environment Variables
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
    # MongoDB uses _id which is an ObjectId
    apps_col.delete_one({'_id': ObjectId(app_id)})
    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
