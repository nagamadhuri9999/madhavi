from pymongo import MongoClient
from datetime import datetime
from flask import Flask,request,render_template,jsonify
from flask_cors import CORS

client=MongoClient('mongodb+srv://madhuri:madhu9999@rockstars.37gdo.mongodb.net/?retryWrites=true&w=majority&appName=rockstars')
db=client['makeskilled']
collection=db['iotdata-test']
alertsCollection=db['alerts']
devicesCollection=db['devices']

api=Flask(__name__)
CORS(api)

@api.route('/')
def homePage():
    return jsonify({"message":"API Server Running"}), 200

@api.route('/alert', methods=['GET'])
def createAlert():
    """Store data in MongoDB using GET method."""
    type1 = request.args.get('type')
    message1 = request.args.get('message')

    if not type1 or not message1:
        return jsonify({"error": "Missing 'type' or 'message' query parameter."}), 400

    # Insert data with timestamp
    data = {
        "type": type1,
        "message": message1,
        "timestamp": datetime.utcnow()  # Add current UTC timestamp
    }
    result = alertsCollection.insert_one(data)
    data["_id"] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization

    return jsonify({"message": "Alert stored successfully", "data": data}), 201

@api.route('/store', methods=['GET'])
def store_data():
    """Store data in MongoDB using GET method."""
    label = request.args.get('label')
    value = request.args.get('value')

    if not label or not value:
        return jsonify({"error": "Missing 'label' or 'value' query parameter."}), 400

    try:
        value = float(value)  # Convert value to numeric
    except ValueError:
        return jsonify({"error": "'value' must be a numeric type."}), 400

    # Insert data with timestamp
    data = {
        "label": label,
        "value": value,
        "timestamp": datetime.utcnow()  # Add current UTC timestamp
    }
    result = collection.insert_one(data)
    data["_id"] = str(result.inserted_id)  # Convert ObjectId to string for JSON serialization

    return jsonify({"message": "Data stored successfully", "data": data}), 201

@api.route('/get-data', methods=['GET'])
def get_data():
    """Retrieve data from MongoDB."""
    # Retrieve data and convert ObjectId to string if necessary
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

@api.route('/get-alerts', methods=['GET'])
def get_alerts():
    """Retrieve data from MongoDB."""
    # Retrieve data and convert ObjectId to string if necessary
    data = list(alertsCollection.find({}, {"_id": 0}))
    return jsonify(data)

@api.route('/get-devices', methods=['GET'])
def get_devices():
    """Retrieve all devices and their states."""
    try:
        devices = list(devicesCollection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=2000,debug=True)