#!/bin/bash

echo "🚀 Start backend container via Docker Compose..."
docker-compose up -d --build

# Wacht een paar seconden tot backend draait
sleep 3

echo "🌐 Start Ngrok tunnel op je static domain..."
ngrok http --domain=wealthy-current-cat.ngrok-free.app 8000
