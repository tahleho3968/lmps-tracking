from flask import request
import os

UPLOAD_FOLDER = "stolen_images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    phone_number = request.form.get("phone_number")
    file = request.files['file']

    if file:
        image_path = os.path.join(UPLOAD_FOLDER, f"{phone_number}.jpg")
        file.save(image_path)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE stolen_devices SET image_path=? WHERE phone_number=?", (image_path, phone_number))
        conn.commit()
        conn.close()

        return jsonify({"message": "Image uploaded successfully"}), 200
    else:
        return jsonify({"message": "No file provided"}), 400
