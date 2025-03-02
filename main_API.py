import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, request, jsonify
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure this file is in your directory
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-bucket-name.appspot.com'  # Replace with your Firebase bucket
})

db = firestore.client()
bucket = storage.bucket()

app = Flask(__name__)

# Report stolen device
@app.route('/report_stolen', methods=['POST'])
def report_stolen():
    data = request.json
    phone_number = data.get("phone_number")
    device_name = data.get("device_name")

    doc_ref = db.collection("stolen_devices").document(phone_number)
    doc_ref.set({
        "phone_number": phone_number,
        "device_name": device_name,
        "last_known_location": "Unknown",
        "last_active_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image_path": "None"
    })

    return jsonify({"message": "Device reported as stolen"}), 201

# Update real-time location
@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    phone_number = data.get("phone_number")
    location = data.get("location")

    doc_ref = db.collection("stolen_devices").document(phone_number)
    doc_ref.update({
        "last_known_location": location,
        "last_active_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return jsonify({"message": "Location updated"}), 200

# Retrieve stolen device data
@app.route('/get_device/<phone_number>', methods=['GET'])
def get_device(phone_number):
    doc_ref = db.collection("stolen_devices").document(phone_number)
    device = doc_ref.get()

    if device.exists:
        return jsonify(device.to_dict())
    else:
        return jsonify({"message": "Device not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
