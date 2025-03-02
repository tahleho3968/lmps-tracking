from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    devices_ref = db.collection("stolen_devices").stream()
    devices = [device.to_dict() for device in devices_ref]

    return render_template('dashboard.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True)
