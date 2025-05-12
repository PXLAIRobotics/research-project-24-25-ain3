from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from database import delete_admin_from_table, authenticate_admin, create_default_admin, create_admin, get_database_connection, create_events_table_if_not_exists, create_admins_table_if_not_exists, insert_events
import json
import numpy as np
import os
import bcrypt
from typing import Dict, List
from chatbot.input_sanitizer import topic_modelling
from auth import create_access_token
from auth import verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload



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
def get_events(user=Depends(get_current_user)):
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
def add_event(request: EventRequest, user=Depends(get_current_user)):
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
async def delete_event(request: DeleteEventRequest, user=Depends(get_current_user)):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

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
def register_admin(credentials: AdminCredentials, user=Depends(get_current_user)):
    try:
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
            access_token = create_access_token(data={"sub": credentials.email})
            return {
                "status": "success",
                "message": "Login successful",
                "access_token": access_token,
                "token_type": "bearer"
            }

        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
    except HTTPException as e:
        # Laat FastAPI bekende HTTP-fouten zoals 401 behandelen
        raise e

    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admins")
def list_admins(user=Depends(get_current_user)):
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM admins;")
        rows = cursor.fetchall()
        conn.close()

        admins = [{"name": row[0], "email": row[1]} for row in rows]
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
class DeleteAdminRequest(BaseModel):
    username: str
    email: str
    
@app.post("/delete-admin")
async def delete_admin(request: DeleteAdminRequest, user=Depends(get_current_user)):
    try:
        email_lower = request.email.lower()
        delete_admin_from_table(email_lower)
        return {"status": "success", "message": f"Admin {request.username} deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete admin: {str(e)}")


@app.get("/logs")
async def getLogs(user=Depends(get_current_user)):
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
async def clearLogs(user=Depends(get_current_user)):
    logs_folder = "logs"
    try:
        for log_file in os.listdir(logs_folder):
            file_path = os.path.join(logs_folder, log_file)
            if log_file.endswith(".json") and os.path.isfile(file_path):
                os.remove(file_path)
        
        print("All log files cleared.")
        return {"message": "Logs cleared successfully."}
    
    except Exception as e:
        print("Error clearing logs:", e)
        raise HTTPException(status_code=500, detail="Failed to clear logs.")