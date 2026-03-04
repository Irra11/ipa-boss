import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid

app = Flask(__name__)
CORS(app) # This allows the Javascript to talk to the API

# MongoDB Config
MONGO_URI = os.environ.get("MONGO_URI", "your_mongodb_uri")
client = MongoClient(MONGO_URI)
db = client['bossipa_db']
apps_col = db['apps']
orders_col = db['orders'] # New collection for orders/udid

# --- PAGES ---
@app.route('/')
def index():
    all_apps = list(apps_col.find().sort('_id', -1))
    return render_template('index.html', apps=all_apps)

@app.route('/admin')
def admin():
    all_apps = list(apps_col.find().sort('_id', -1))
    return render_template('admin.html', apps=all_apps)

# --- API ENDPOINTS (For your Javascript) ---

@app.route('/api/create-order', methods=['POST'])
def create_order():
    # This is what your frontend calls
    data = request.json
    order_id = str(uuid.uuid4())[:8] # Generate a short order ID
    
    new_order = {
        "order_id": order_id,
        "udid": data.get('udid'),
        "status": "pending"
    }
    orders_col.insert_one(new_order)
    
    return jsonify({"status": "success", "orderId": order_id})

# --- APP MANAGEMENT ---
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
