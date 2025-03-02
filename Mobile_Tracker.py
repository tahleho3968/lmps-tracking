import geocoder
import time
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

PHONE_NUMBER = input("Enter your phone number with country code: ")

def get_location():
    g = geocoder.ip('me')
    return g.latlng if g.latlng else "Unknown"

while True:
    location = get_location()
    doc_ref = db.collection("stolen_devices").document(PHONE_NUMBER)
    doc_ref.update({
        "last_known_location": str(location),
        "last_active_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    print(f"Updated location for {PHONE_NUMBER}: {location}")
    time.sleep(30)  # Sends location update every 30 seconds
