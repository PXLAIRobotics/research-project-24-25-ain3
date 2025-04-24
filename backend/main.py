from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from chatbot.pathplanning import calculate_path
from database import get_database_connection, create_table_if_not_exists, insert_events, get_embedding
import json
import numpy as np
from psycopg2.extensions import AsIs



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

# Load JSON data
json_data = '''
{
    "campus_name": "Corda",
    "events": {
        "academic": [
            {
                "name": "Research Symposium",
                "date": "2025-04-10",       
                "description": "A symposium showcasing student research."
            }
        ],
        "cultural": [
            {
                "name": "Cultural Fest",
                "date": "2025-05-20",
                "description": "A festival celebrating diverse cultures."
            }
        ],
        "workshops": [
            {
                "name": "AI Workshop",
                "date": "2025-03-25",
                "description": "A workshop on artificial intelligence."
            }
        ],
        "social": [
            {
                "name": "Spring Gala",
                "date": "2025-04-15",
                "description": "A social gathering for students."
            }
        ]
    }
}
'''
data = json.loads(json_data)

@app.on_event("startup")
def startup_event():
    """Initialize the database and insert events on app startup."""
    conn = get_database_connection()
    create_table_if_not_exists(conn)
    insert_events(data["events"], conn)
    conn.close()

@app.get("/pixie")
async def generateResponse(message: str):
    print("Message received:", message)
    response = chat_completion(message)
    print("Response sent:", response, "\n")
    return {"data": response}

class Event(BaseModel):
    name: str
    date: str  # In 'YYYY-MM-DD' formaat
    description: str

@app.post("/events")
def add_event(event: Event):
    try:
        conn = get_database_connection()
        create_table_if_not_exists(conn)

        embedding = get_embedding(event.description)
        embedding_array = list(map(float, embedding))
        embedding_array = AsIs(f"ARRAY[{', '.join(map(str, embedding_array))}]")

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO events (event_name, event_date, event_description, embedding)
            VALUES (%s, %s, %s, %s)
        """, (event.name, event.date, event.description, embedding_array))

        conn.commit()
        cursor.close()
        conn.close()

        return {"status": "success", "event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))