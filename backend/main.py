from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from chatbot.pixie import chat_completion
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/pixie")
async def generateResponse(message: str):
    print("Message received:", message)
    response = chat_completion(message)
    print("Response sent:", response, "\n")
    return {"data": response}

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
