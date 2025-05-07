from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from database import delete_admin_from_table, authenticate_admin, create_default_admin, create_admin, get_database_connection, create_events_table_if_not_exists, create_admins_table_if_not_exists, insert_events
import json
import numpy as np
import os
import bcrypt
from typing import Dict, List
from chatbot.input_sanitizer import topic_modelling

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
    create_events_table_if_not_exists(conn)
    create_admins_table_if_not_exists(conn)
    conn.close()

    create_default_admin()

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
        create_events_table_if_not_exists(conn)

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
        create_events_table_if_not_exists(conn)

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
    

class AdminCredentials(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register-admin")
def register_admin(credentials: AdminCredentials):
    try:
        # E-mail opslaan in lowercase
        email_lower = credentials.email.lower()
        
        conn = get_database_connection()
        create_admin(credentials.username, email_lower, credentials.password, conn)
        conn.close()
        
        return {"status": "success", "message": f"Admin {credentials.username} created."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class LoginCredentials(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(credentials: LoginCredentials):
    try:
        # Zet e-mail in lowercase om te vergelijken
        email_lower = credentials.email.lower()
        
        conn = get_database_connection()
        auth_result = authenticate_admin(email_lower, credentials.password, conn)
        conn.close()

        if auth_result["authenticated"]:
            return {"status": "success", "message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
    except HTTPException as e:
        # Laat FastAPI bekende HTTP-fouten zoals 401 behandelen
        raise e

    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admins")
def list_admins():
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM admins;")
        rows = cursor.fetchall()
        conn.close()

        admins = [{"name": row[0], "email": f"{row[1]}"} for row in rows]
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class DeleteAdminRequest(BaseModel):
    email: str
    
@app.post("/delete-admin")
async def delete_admin(request: DeleteAdminRequest):
    try:
        # Zet e-mail in lowercase
        email_lower = request.email.lower()

        delete_admin_from_table(email_lower)
        
        return {"status": "success", "message": f"Admin {email_lower} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete admin: {str(e)}")


@app.get("/logs")
async def getLogs():
    logs_data = []
    print("Request received")
    
    for log_filename in os.listdir("logs"):
        if log_filename.endswith(".json"):
            log_path = os.path.join("logs", log_filename)
            try:
                with open(log_path, "r") as f:
                    log_content = json.load(f)
                    logs_data.append(log_content)
                    print(f"Loaded {log_filename}")
            except json.JSONDecodeError:
                print(f"Skipping malformed log file: {log_filename}")
            except Exception as e:
                print(f"Error reading {log_filename}: {e}")

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