import psycopg2
import numpy as np
import json
from openai import OpenAI
import os
from psycopg2.extensions import AsIs
import bcrypt
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    """Establish and return a database connection using environment variables."""
    return psycopg2.connect(
        dbname=os.environ["DATABASE_NAME"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        host=os.environ["DATABASE_HOST"],
        port=os.environ["DATABASE_PORT"]
    )

def create_events_table_if_not_exists(conn):
    """Create the 'events' table if it does not exist."""
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_description TEXT,
            embedding VECTOR(1536)
        );
    """)
    conn.commit()
    cursor.close()

def create_admins_table_if_not_exists(conn):
    """Create the 'admins' table if it does not exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_admin(username, email, password, conn):
    hashed = hash_password(password)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO admins (username, email, password_hash)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
    """, (username, email , hashed))
    conn.commit()
    cursor.close()

def authenticate_admin(email, password, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE email = %s;", (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        stored_hash = result[0]
        if check_password(password, stored_hash):
            return {"authenticated": True}
    return {"authenticated": False}

def create_default_admin():
    conn = get_database_connection()
    cursor = conn.cursor()

    username = os.getenv("DEFAULT_ADMIN_USERNAME")
    email = os.getenv("DEFAULT_ADMIN_EMAIL")
    password = os.getenv("DEFAULT_ADMIN_PASSWORD")

    if not username or not email or not password:
        print("Default admin credentials not set in .env file")
        return

    cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
    existing_admin = cursor.fetchone()

    if not existing_admin:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO admins (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password.decode('utf-8'))
        )
        print("Default admin account created.")
    else:
        print("Admin account already exists.")

    conn.commit()
    conn.close()

def delete_admin_from_table(email):
    print(f"Deleting admin with email: {email}")
    try:
        conn = get_database_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM admins WHERE email = %s", (email,))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error during delete admin operation: {e}")
        raise


def get_embedding(text):
    """Generate an embedding for the given text."""
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        print(f"Generated embedding (first 5 values): {embedding[:5]}")
        return list(embedding)
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def insert_events(events, conn):
    """Insert events into the database with embeddings."""
    try :
        cursor = conn.cursor()
        for category, event_list in events.items():
            for event in event_list:
                event_name = event.name
                event_date = event.date
                event_description = event.description

                embedding = get_embedding(f"{event_description} {event_date}")
                if embedding is None:
                    print(f"Skipping insert for event '{event_name}' due to missing embedding.")
                    continue

                cursor.execute("""
                    INSERT INTO events (event_name, event_date, event_description, embedding)
                    VALUES (%s, %s, %s, %s)
                """, (event_name, event_date, event_description, embedding))

        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error insterting event: {e}")
        return None

    

def search_similar_event(message, conn):
    """Search for the most similar event in the database based on the message embedding."""
    try:
        print("Generating embedding for the message...")
        embedding = get_embedding(message)
        if embedding is None:
            print("Failed to generate embedding for search.")
            return None

        cursor = conn.cursor()
        print("Executing database query...")
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
                "event_description": result[3] 
                   }

        print("No matching events found.")
        return None
    except Exception as e:
        print(f"Error in search_similar_event: {e}")
        raise
