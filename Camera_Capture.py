import cv2
import cloudinary
import cloudinary.uploader

# ✅ Configure Cloudinary (Use your credentials)
cloudinary.config(
    cloud_name="dit87msf0",     # Your Cloudinary Cloud Name
    api_key="653767312626745",  # Your Cloudinary API Key
    api_secret="2UEbxxM0ZrmOqbbJxmqtxu9xBdc"  # Replace with new API Secret
)

def capture_image():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    
    if ret:
        image_path = "captured.jpg"
        cv2.imwrite(image_path, frame)
        camera.release()
        return image_path
    else:
        print("Failed to capture image")
        return None

def upload_image(image_path, phone_number):
    response = cloudinary.uploader.upload(image_path, public_id=f"stolen_images/{phone_number}")
    image_url = response["secure_url"]
    print(f"✅ Image uploaded successfully: {image_url}")
    return image_url

# User input for phone number
phone_number = input("Enter stolen device's phone number: ")
image_path = capture_image()

if image_path:
    image_url = upload_image(image_path, phone_number)

    # ✅ Update Firestore with the image URL
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    doc_ref = db.collection("stolen_devices").document(phone_number)
    doc_ref.update({"image_path": image_url})

    print("✅ Firestore updated successfully!")
