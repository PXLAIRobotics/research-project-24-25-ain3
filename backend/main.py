from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from database import get_database_connection, create_table_if_not_exists, insert_events
import json
import os
from typing import Dict, List
from chatbot.input_sanitizer import topic_modelling
from fastapi.responses import FileResponse
from gtts import gTTS
import uuid
import re
import html
from faster_whisper import WhisperModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

whisperModel = WhisperModel("small", compute_type="int8")




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
    

def clean_text(text: str) -> str:
    # Decode HTML entities zoals &amp; -> &
    text = html.unescape(text)

    # Verwijder alle HTML-tags
    text = re.sub(r'<[^>]+>', '', text)

    # Verwijder Markdown-symbolen zoals **, *, __, _
    text = re.sub(r'[*_`#\-~]', '', text)

    # Verwijder dubbele of overbodige spaties
    text = re.sub(r'\s+', ' ', text).strip()

    return text

@app.get("/tts")
async def tts(text: str = Query(..., min_length=1)):
    """
    Endpoint om tekst om te zetten naar spraak en terug te sturen als MP3-bestand.
    """
    clean = clean_text(text)

    filename = f"/tmp/{uuid.uuid4()}.mp3"
    tts = gTTS(text=clean, lang='nl')
    tts.save(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    contents = await audio.read()
    with open("temp_audio.wav", "wb") as f:
        f.write(contents)

    # Voeg 'language' toe en eventueel 'beam_size' voor betere kwaliteit
    segments, _ = whisperModel.transcribe("temp_audio.wav", language="nl", beam_size=5)
    transcript = "".join([segment.text for segment in segments])
    return {"text": transcript}