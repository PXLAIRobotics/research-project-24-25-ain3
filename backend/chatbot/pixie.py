import datetime
import json
import os

import gradio as gr
import tiktoken
from dotenv import load_dotenv
import openai



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

    # Debug: Print messages before API call
    print("Sending to API:", json.dumps(history, indent=2))

    try:
        # OpenAI API aanroepen
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            extra_headers={
                "HTTP-Referer": "https://pxl-research.be/",
                "X-Title": "PXL Smart ICT"
            }
        )
        
        # Haal het gegenereerde antwoord op
        response_message = response.choices[0].message.content if response.choices else "No response received."
        
        # Voeg de response toe aan de history met response_code 200 (OK)
        history.append({
            "role": "assistant",
            "content": response_message,
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

    # Opslaan in logbestand
    store_history(history, "logs/")

    return response_message if 'response_message' in locals() else "Er is een fout opgetreden."
