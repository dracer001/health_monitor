import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) # Enables cross-origin requests for your frontend

DATA_FILE = 'history.json'

def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data_list):
    with open(DATA_FILE, 'w') as f:
        json.dump(data_list, f, indent=4)

@app.route('/api/v1/sensor-data', methods=['POST'])
def post_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    history = load_data()
    history.append(data)
    save_data(history)
    
    print(f"[*] Data Received: HR:{data.get('heart_rate')} SpO2:{data.get('spo2')} Temp:{data.get('temp')}")
    return jsonify({"status": "stored", "timestamp": data['timestamp']}), 201

@app.route('/api/v1/live', methods=['GET'])
def get_live():
    history = load_data()
    return jsonify(history[-1]) if history else ({}, 404)

@app.route('/api/v1/history', methods=['GET'])
def get_history():
    return jsonify(load_data())


@app.route('/api/v1/health', methods=['GET'])
def checkhealth():
    return {'status': 'active'}

if __name__ == '__main__':
    init_file()
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
