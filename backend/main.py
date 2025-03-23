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
    history = []
    response = chat_completion(message, history)
    print("Response sent:", response, "\n")
    return {"data": response}

