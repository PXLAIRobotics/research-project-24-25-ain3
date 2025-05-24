from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from chatbot.pathplanning import calculate_path
from database import get_database_connection, create_table_if_not_exists, insert_events, get_embedding, clear_event_table, delete_event
import json
import numpy as np
import os
from typing import Dict, List
from chatbot.input_sanitizer import topic_modelling
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
import base64
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)



@app.on_event("startup")
def startup_event():
    """Initialize the database and insert events on app startup."""
    conn = get_database_connection()
    create_table_if_not_exists(conn)
    conn.close()

@app.get("/pixie")
async def generateResponse(message: str):
    print("Message received:", message)
    response = chat_completion(message)
    bad_topic_warning = topic_modelling(message)
    if bad_topic_warning:
        return {"data": response, "endChat": bad_topic_warning} 
    print("Response sent:", response, "\n")
    return {"data": response, "endChat": ""}

class Event(BaseModel):
    name: str
    date: str  # In 'YYYY-MM-DD' format
    description: str

class EventRequest(BaseModel):
    campus_name: str
    events: Dict[str, List[Event]]
    
@app.get("/allEvents")
def get_events():
    try:
        conn = get_database_connection()
        create_table_if_not_exists(conn)

        cursor = conn.cursor()
        cursor.execute("SELECT id, event_name, event_date, event_description FROM events")
        rows = cursor.fetchall()

        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "event_name": row[1],
                "event_date": row[2],
                "event_description": row[3]
            })

        conn.close()
        return {"status": "success", "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/events")
def add_event(request: EventRequest):
    try:
        conn = get_database_connection()
        create_table_if_not_exists(conn)

        insert_events(request.events, conn)

        conn.commit()
        conn.close()

        return {"status": "success", "campus": request.campus_name, "events": request.events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class DeleteEventRequest(BaseModel):
    name: str
    
@app.post("/delete-event")
async def delete_event(request: DeleteEventRequest):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        # Verwijder het event met de juiste naam
        cursor.execute("DELETE FROM events WHERE event_name = %s", (request.name,))
        conn.commit()
        conn.close()

        return {"status": "success", "message": f"Event '{request.name}' deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/logs")
async def getLogs():
    logs_data = []
    print("Request received")
    
    for log in os.listdir("logs"):  # List all files in the "logs" directory
        if log.endswith(".json"):  # Only process JSON log files
            with open(os.path.join("logs", log), "r") as f:
                log_content = json.load(f)
                logs_data.append(log_content)
                print("Sending logs")

    return {"logs": logs_data}

@app.post("/clear-logs")
async def clearLogs():
    logs_folder = "logs"
    try:
        # Loop through all files in the logs folder
        for log_file in os.listdir(logs_folder):
            file_path = os.path.join(logs_folder, log_file)
            if log_file.endswith(".json") and os.path.isfile(file_path):
                os.remove(file_path)  # Delete the log file
        
        print("All log files cleared.")
        return {"message": "Logs cleared successfully."}
    
    except Exception as e:
        print("Error clearing logs:", e)
        raise HTTPException(status_code=500, detail="Failed to clear logs.")


class ImageData(BaseModel):
    image: str

# Init face analyzer
app_face = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app_face.prepare(ctx_id=0)

# Laden van referentiebeelden (bijv. admin.jpg)
known_faces = {}
def load_known_faces():
    import os
    for file in os.listdir("known_faces"):
        img = cv2.imread(f"known_faces/{file}")
        faces = app_face.get(img)
        if faces:
            known_faces[file.split(".")[0]] = faces[0].embedding

load_known_faces()

@app.post("/facial-recognition")
def recognize_face(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])
    np_img = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    faces = app_face.get(frame)
    if not faces:
        return { "label": None }

    emb = faces[0].embedding
    best_label = None
    best_dist = float("inf")

    for label, known_emb in known_faces.items():
        dist = np.linalg.norm(emb - known_emb)
        if dist < best_dist:
            best_dist = dist
            best_label = label

    if best_dist < 1.0:  # drempelwaarde, meestal rond 0.8-1.0
        return { "label": best_label }

    return { "label": None }

