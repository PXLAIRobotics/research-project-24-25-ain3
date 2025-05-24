from fastapi import FastAPI
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import onnxruntime
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from numpy.linalg import norm
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = Path(__file__).resolve().parent
onnx_path = base_dir / "models" / "recognition_model.onnx"
known_faces_dir = base_dir / "known_faces"

if not onnx_path.exists():
    raise FileNotFoundError(f"ONNX model not found at {onnx_path}")

if not known_faces_dir.exists():
    raise FileNotFoundError(f"'known_faces' folder not found at {known_faces_dir}")

session = onnxruntime.InferenceSession(str(onnx_path))
known_face_encodings = []
known_face_labels = []

class ImagePayload(BaseModel):
    image: str

def preprocess_image(pil_img):
    img = pil_img.resize((112, 112))
    img = np.array(img).astype(np.float32)
    img = (img - 127.5) / 128.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, 0)
    return img

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def normalize_embedding(emb):
    norm_val = np.linalg.norm(emb)
    if norm_val == 0:
        return emb
    return emb / norm_val

def load_known_faces():
    global known_face_encodings, known_face_labels
    known_face_encodings.clear()
    known_face_labels.clear()

    embeddings_per_label = {}

    for file in os.listdir(known_faces_dir):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            # Groeperen op basis van naam vóór underscore, bv "Anna_1.jpg" -> "Anna"
            label = file.rsplit(".", 1)[0].split('_')[0]
            path = known_faces_dir / file
            try:
                img = Image.open(path).convert("RGB")
                tensor = preprocess_image(img)
                embedding = session.run(None, {session.get_inputs()[0].name: tensor})[0]
                embedding = normalize_embedding(embedding[0])

                embeddings_per_label.setdefault(label, []).append(embedding)
                print(f"[INFO] Loaded known face: {label} from file {file}")
            except Exception as e:
                print(f"[ERROR] Failed to process {file}: {e}")

    # Gemiddelde embedding per persoon
    for label, embs in embeddings_per_label.items():
        mean_emb = np.mean(embs, axis=0)
        mean_emb = normalize_embedding(mean_emb)
        known_face_encodings.append(mean_emb)
        known_face_labels.append(label)

    print(f"[INFO] Total known faces loaded (grouped): {len(known_face_encodings)}")


# Laad bekende gezichten bij opstart
load_known_faces()

@app.post("/facial-recognition")
async def facial_login(data: ImagePayload):
    try:
        base64_str = data.image.split(",")[1] if "," in data.image else data.image
        image_data = base64.b64decode(base64_str)
        pil_img = Image.open(BytesIO(image_data)).convert("RGB")
        input_tensor = preprocess_image(pil_img)

        inputs = {session.get_inputs()[0].name: input_tensor}
        embeddings = session.run(None, inputs)[0]
        embeddings = normalize_embedding(embeddings[0])

        threshold = 0.3  # Pas deze waarde aan indien nodig (lager = makkelijker matchen, hoger = strenger)
        for i, known_emb in enumerate(known_face_encodings):
            sim = cosine_similarity(embeddings, known_emb)
            print(f"[DEBUG] Similarity with {known_face_labels[i]}: {sim:.4f}")
            if sim > threshold:
                print(f"[INFO] Face recognized as {known_face_labels[i]}")
                return {"label": known_face_labels[i]}
        print("[INFO] Face not recognized")
        return {"label": None}

    except Exception as e:
        print(f"[Error] Facial login error: {e}")
        return {"label": None, "error": str(e)}
