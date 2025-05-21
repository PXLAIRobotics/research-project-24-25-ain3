from fastapi import FastAPI
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import face_recognition
from pathlib import Path

app = FastAPI()

# Load known face encodings at startup
known_face_encodings = []
known_face_labels = []

class ImagePayload(BaseModel):
    image: str

@app.on_event("startup")
def load_reference_faces():
    try:
        base_dir = Path(__file__).resolve().parent
        image_path = base_dir / "assets" / "admin.jpg"  # Adjusted path
        if not image_path.exists():
            raise FileNotFoundError(f"Reference image not found at {image_path}")

        admin_image = face_recognition.load_image_file(str(image_path))
        encodings = face_recognition.face_encodings(admin_image)
        if not encodings:
            raise ValueError("No face found in reference image.")

        known_face_encodings.append(encodings[0])
        known_face_labels.append("admin@gmail.com")

        print("[Startup] Admin face encoding loaded.")
    except Exception as e:
        print(f"[Startup Error] Failed to prepare reference face: {e}")

@app.post("/facial-login")
async def facial_login(data: ImagePayload):
    try:
        # Decode base64 image
        image_data = base64.b64decode(data.image.split(",")[1])
        image = Image.open(BytesIO(image_data)).convert("RGB")

        # Convert PIL image to numpy array for face_recognition
        np_image = face_recognition.load_image_file(BytesIO(image_data))

        unknown_encodings = face_recognition.face_encodings(np_image)
        if not unknown_encodings:
            return {"label": None}

        match = face_recognition.compare_faces(known_face_encodings, unknown_encodings[0])
        if True in match:
            matched_index = match.index(True)
            return {"label": known_face_labels[matched_index]}
        else:
            return {"label": None}

    except Exception as e:
        print(f"[Error] Facial login error: {e}")
        return {"label": None}
