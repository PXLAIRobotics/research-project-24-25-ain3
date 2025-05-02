import datetime
import json
import os
import re
import gradio as gr
import tiktoken
from dotenv import load_dotenv
import openai

from chatbot.pathplanning import calculate_path
from database import get_database_connection, search_similar_event
from chatbot.input_sanitizer import tokenization_with_ontology, robbert_sentiment_analysis


# Load environment variables
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API Key is missing. Make sure you have set OPENAI_API_KEY in your .env file.")

client = openai.OpenAI(api_key=api_key)

# Load campus data
campus_data_path = os.path.join(os.path.dirname(__file__), 'campus_data.json')
if not os.path.exists(campus_data_path):
    raise FileNotFoundError(f"campus_data.json not found at {campus_data_path}")

with open(campus_data_path, 'r') as f:
    campus_info = json.load(f)

system_instruction = {
    "role": "system",
    "content": (
        "Be concise. Be precise. Make the output as clear as possible. "
        "Make the output prettier and structured. Always think step by step. "
        "Only give information about events if explicitly asked. "
        "If asked about campus corda details, provide the following information: Email: campus@gmail.com, Phone: 0488888888, Address: Campus Street 123, Hasselt 3500."
        "Be precise, structured, and friendly. You are VIBE, the friendly front-desk assistant of Corda Campus Hasselt. You help with questions about location, facilities, events, and directions within Corda Campus Hasselt. Only answer questions about Corda Campus. If a user greets you, respond politely. If the user asks about events, provide available event information clearly and concisely. If the question is irrelevant to Corda Campus, respond with: 'Sorry, I can’t help you with that. I’m only here for questions about Corda Campus Hasselt.'"
    )
}

log_filename = None
history = []


def get_log_filename(log_folder):
    """Generate a single log file per session."""
    global log_filename

    if log_filename is None:
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        time_stamp = f'{datetime.datetime.now():%y%m%d_%H%M_%S}'
        log_filename = os.path.join(log_folder, f'{time_stamp}.json')
    return log_filename


def store_history(history, log_folder):
    """Save conversation history to a log file."""
    log_file = get_log_filename(log_folder)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def chat_completion(message):
    global history

    # Ensure system instruction is always first
    if not history or history[0]["role"] != "system":
        history.insert(0, system_instruction)

    # Append the user's message
    history.append({"role": "user", "content": message})

    # --- INPUT SANITATION MBV NLP ---
   
    
    sanitization_warning = tokenization_with_ontology(message) or robbert_sentiment_analysis(message)
    if sanitization_warning:
        history.append({
            "role": "assistant",
            "content": sanitization_warning,
            "response_code": 400
        })
        store_history(history, "logs/")
        return sanitization_warning
    
    

    # Debug: Print messages before API call
    print("Sending to API:", json.dumps(history, indent=2))

    try:
        conn = get_database_connection()
        similar_event = search_similar_event(message, conn)
        conn.close()
        # Controleer of het bericht om padinformatie vraagt
        if "pad" in message.lower() or "route" in message.lower():
            match = re.search(r"\b(?:pad|route)\s+van\s+([\w\s]+?)\s+naar\s+([\w\s]+)", message, re.IGNORECASE)
            
            if match:
                start = match.group(1).strip()
                destination = match.group(2).strip()

                # Bereken het pad
                path_info = calculate_path(start, destination)

                response = f"Het pad van {path_info['start_node']} naar {path_info['destination_node']} is als volgt: {path_info['path']}.\n" \
                f"De totale afstand is {path_info['total_distance']}."
            else:
                response = "Sorry, ik kan de start- en bestemminglocaties niet herkennen in je bericht. \nHier is een lijst met alle mogelijke locaties Corda 1, Corda 2, Corda 3, Corda 4, Corda 5, Corda 6, Corda 7, Corda 8, Corda 9, Corda A, Corda B, Corda C, Corda D, Corda bar, Bushalte, Treinstation"
                        
        else:
            # Standaard ChatGPT reactie
            if similar_event:
                history.append({
                    "role": "system",
                    "content": f"Let op: Dit is een gerelateerd evenement dat mogelijk relevant is: {similar_event}"
                })

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                extra_headers={
                    "HTTP-Referer": "https://pxl-research.be/",
                    "X-Title": "PXL Smart ICT"
                }
            ).choices[0].message.content

        # Voeg de response toe aan de history met response_code 200 (OK)
        history.append({
            "role": "assistant",
            "content": response,
            "response_code": 200
        })

    except openai.OpenAIError as e:
        error_message = str(e)
        status_code = "unknown"

        # Haal statuscode uit string
        if "Error code: " in error_message:
            try:
                status_code = int(error_message.split("Error code: ")[1].split(" - ")[0])
            except ValueError:
                status_code = "unknown"

        # Haal message uit string
        if "'message':" in error_message:
            try:
                message_start = error_message.index("'message':") + 11
                message_end = error_message.index("',", message_start)
                error_message = error_message[message_start:message_end]
            except ValueError:
                pass

        # Voeg error toe aan history met response_code
        history.append({
            "role": "error",
            "content": error_message,
            "response_code": status_code
        })

    # Bewaar de geschiedenis in een logbestand
    store_history(history, "logs/")

    return response