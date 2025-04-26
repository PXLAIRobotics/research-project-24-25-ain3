from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from chatbot.pathplanning import calculate_path
from database import get_database_connection, create_table_if_not_exists, insert_events, get_embedding, clear_event_table
import json
import numpy as np
import os
from psycopg2.extensions import AsIs
from typing import Dict, List


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
    print("Response sent:", response, "\n")
    return {"data": response}

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
    
@app.post("/delete-events")
def delete_events():
    try:
        conn = get_database_connection()
        clear_event_table(conn)
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Events table cleared."}
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