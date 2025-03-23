import datetime
import json
import os

import gradio as gr
import tiktoken
from dotenv import load_dotenv
import openai

print("Test")

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

with open(os.path.join(os.path.dirname(__file__),'campus_data.json'), 'r') as f:
    campus_info = json.load(f)

system_instruction = {
    'role': 'assistant',
    'campus_info': campus_info,
    'content': 'Be concise. Be precise. '
                'make the output as clear as possible. '
                'make the output prettiers and structred. '
               'I would like you to take a deep breath before responding. '
               'Always think step by step. '
}

log_filename = None
history = []


def get_log_filename(log_folder):
    """Per sessie willen we 1 logfile krijgen"""
    global log_filename

    if log_filename is None:
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        time_stamp = f'{datetime.datetime.now():%y%m%d_%H%M_%S}'
        log_filename = f'{log_folder}{time_stamp}.json'
    return log_filename



def store_history(history, log_folder):
    """Sla de volledige history op in die ene logfile"""
    log_file = get_log_filename(log_folder)
    with open(log_file, 'wt') as f:
        json.dump(history, f, indent=1)


def chat_completion(message):
    global history

    if system_instruction not in history:
        # prepend system instructions
        history.insert(0, system_instruction)

    # append latest prompt
    history.append({'role': 'user', 'content': message})

    # clean up extra fields
    for event in history:
        for key in list(event):
            if key == 'role' or key == 'content':
                continue
            else:
                del event[key]

    # call the language model
    response = client.chat.completions.create(model='gpt-4o-mini',
                                                     messages=history,
                                                     extra_headers={
                                                         'HTTP-Referer': 'https://pxl-research.be/',
                                                         'X-Title': 'PXL Smart ICT'
                                                     })
    partial_message = response.choices[0].message.content if response.choices else ""


    # store in a log file
    history.append({'role': 'assistant', 'content': partial_message})
    store_history(history, 'logs/')

    return partial_message