import datetime
import json
import os
from chatbot.pathplanning import calculate_path
import gradio as gr
import tiktoken
from dotenv import load_dotenv
import openai
import re



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
        "Here are the details about the campus: "
        f"{json.dumps(campus_info, indent=2)}"
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
        log_filename = f'{log_folder}{time_stamp}.json'
    return log_filename


def store_history(history, log_folder):
    """Save conversation history to a log file."""
    log_file = get_log_filename(log_folder)
    with open(log_file, 'wt') as f:
        json.dump(history, f, indent=1)


def chat_completion(message):
    global history

    # Ensure system instruction is always first
    if not history or history[0]["role"] != "system":
        history.insert(0, system_instruction)

    # Append the user's message
    history.append({"role": "user", "content": message})

    # Debug: Print messages before API call
    print("Sending to API:", json.dumps(history, indent=2))

    try:
        # Controleer of het bericht om padinformatie vraagt
        if "pad" in message or "route" in message:
            try :
                # Zoek naar de combinatie "van <start> naar <bestemming>"
                match = re.search(r"(pad van|route van)\s+([a-zA-Z0-9\s]+)\s+(naar)\s+([a-zA-Z0-9\s]+)", message)
        
                if match:
                    start = match.group(2).strip()  # Startlocatie
                    destination = match.group(4).strip()  # Bestemming

                    # Bereken het pad
                    path_info = calculate_path(start, destination)

                    # Maak een mooie reactie
                    response = f"Het pad van {start} naar {destination} is als volgt: {path_info['path']}.\n" \
                            f"De totale afstand is {path_info['total_distance']}."
                    return response
            except:
                response = "Sorry, ik kan de start- en bestemminglocaties niet herkennen in je bericht. \nHier is een lijst met alle mogelijke locaties Corda 1, Corda 2, Corda 3, Corda 4, Corda 5, Corda 6, Corda 7, Corda 8, Corda 9, Corda A, Corda B, Corda C, Corda D, Corda bar, Bushalte, Treinstation"
                return response
        else:
            # Standaard ChatGPT reactie
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                extra_headers={
                    "HTTP-Referer": "https://pxl-research.be/",
                    "X-Title": "PXL Smart ICT"
                }
            ).choices[0].message.content

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Er is een fout opgetreden bij het ophalen van het antwoord van OpenAI."

    # Voeg de reactie van de chatbot toe aan de geschiedenis
    history.append({"role": "assistant", "content": response})

    # Bewaar de geschiedenis in een logbestand
    store_history(history, "logs/")

    return response


