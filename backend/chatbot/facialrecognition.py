from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)

# Load known face encodings
known_image = face_recognition.load_image_file("known_user.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

@app.route('/api/facial-login', methods=['POST'])
def facial_login():
    data = request.json
    if 'image' not in data:
        return jsonify({'success': False, 'error': 'No image provided'}), 400

    try:
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        image_np = np.array(image)

        # Encode face
        unknown_encodings = face_recognition.face_encodings(image_np)
        if not unknown_encodings:
            return jsonify({'success': False, 'error': 'No face detected'}), 400

        results = face_recognition.compare_faces([known_encoding], unknown_encodings[0])

        return jsonify({'success': True, 'match': results[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
