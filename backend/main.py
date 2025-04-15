from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot.pixie import chat_completion
from chatbot.pathplanning import calculate_path
from database import get_database_connection, create_table_if_not_exists, insert_events
import json

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

class PathRequest(BaseModel):
    start: str
    destination: str

@app.post("/find-path/")
def find_path(request: PathRequest):
    path = calculate_path(request.start, request.destination)
    return {"path": path}