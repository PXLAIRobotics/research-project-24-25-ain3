import psycopg2
import numpy as np
import json
from openai import OpenAI
import os
from psycopg2.extensions import AsIs


client = OpenAI(api_key="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")

def get_database_connection():
    """Establish and return a database connection using environment variables."""
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME", "mydatabase"),
        user=os.getenv("DATABASE_USER", "myuser"),
        password=os.getenv("DATABASE_PASSWORD", "mypassword"),
        host=os.getenv("DATABASE_HOST", "postgres"),
        port=os.getenv("DATABASE_PORT", "5432")
    )

def create_table_if_not_exists(conn):
    """Create the 'events' table if it does not exist."""
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_description TEXT,
            embedding VECTOR(1536) -- Ensure the embedding column is of type VECTOR
        );
    """)


    cursor.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'events' AND column_name = 'embedding' AND data_type != 'vector'
            ) THEN
                ALTER TABLE events DROP COLUMN embedding;
                ALTER TABLE events ADD COLUMN embedding VECTOR(1536);
            END IF;
        END $$;
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
    for event_list in events.values():
        for event in event_list:
            event_name = event["name"]
            event_date = event["date"]
            event_description = event["description"]
            
            # Generate the embedding as a list of floats
            embedding = get_embedding(event_description)


            # Insert the event into the database
            cursor.execute("""
                INSERT INTO events (event_name, event_date, event_description, embedding)
                VALUES (%s, %s, %s, %s)
            """, (event_name, event_date, event_description, embedding))

    
    conn.commit()
    cursor.close()

def search_similar_event(message, conn):
    """Search for the most similar event in the database based on the message embedding."""
    try:
        print("Generating embedding for the message...")
        embedding = get_embedding(message)  # Embedding is already a list of floats
        print("Embedding generated successfully.")

        print("Executing database query...")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, event_name, event_date, event_description, 
                   embedding <-> %s::vector AS distance
            FROM events
            ORDER BY distance ASC
            LIMIT 1;
        """, (embedding,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            print("Query successful. Returning result.")
            return {
                "id": result[0],
                "event_name": result[1],
                "event_date": result[2],
                "event_description": result[3],
                "distance": result[4]
            }
        print("No matching events found.")
        return None
    except Exception as e:
        print(f"Error in search_similar_event: {e}")
        raise