import psycopg2
import numpy as np
import json
from openai import OpenAI
import os

client = OpenAI(api_key="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")

def get_database_connection():
    """Establish and return a database connection using environment variables."""
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME", "mydatabase"),
        user=os.getenv("DATABASE_USER", "myuser"),
        password=os.getenv("DATABASE_PASSWORD", "mypassword"),
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", "5432")
    )

def create_table_if_not_exists(conn):
    """Create the 'events' table if it does not exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_description TEXT,
            embedding BYTEA
        );
    """)
    conn.commit()
    cursor.close()

def get_embedding(text):
    """Generate an embedding for the given text."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def insert_events(events, conn):
    """Insert events into the database."""
    cursor = conn.cursor()
    for category, event_list in events.items():
        for event in event_list:
            event_name = event["name"]
            event_date = event["date"]
            event_description = event["description"]
            
            embedding = get_embedding(event_description)
            embedding_binary = np.array(embedding, dtype=np.float32).tobytes()

            cursor.execute("""
                INSERT INTO events (event_name, event_date, event_description, embedding)
                VALUES (%s, %s, %s, %s)
            """, (event_name, event_date, event_description, embedding_binary))
    
    conn.commit()
    cursor.close()