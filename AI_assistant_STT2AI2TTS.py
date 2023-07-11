import requests
from requests.exceptions import RequestException
import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, filedialog

import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import write
import datetime

import random
import string

import time

import openai

import pygame
pygame.mixer.init()

import re

# from elevenlabs import set_api_key, generate, play, save




def get_models():
    
    response = openai.Model.list()
    
    return response


def chat_with_gpt3(model, conversation):
    print(model)
    print(conversation)
    completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        max_tokens=1024
    )
    
    return completion



def transcribe_audio(api_key, mp3_filename):
    
    with open(mp3_filename, 'rb') as file:
        
        transcript = openai.Audio.transcribe("whisper-1", file)
    
    # return response (json)
    return transcript


# function to add a timestamp
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_random_text(length):
    # Generate a string of random characters of the given length
    return ''.join(random.choice(string.ascii_letters + string.digits + '            ') for _ in range(length))



# import requests
# import logging

# def call_elevenlabs_api(text, voice):
    # url = 'https://api.eleven-labs.com/v1/speech'
    # headers = {'Content-Type': 'application/json'}
    # payload = {
        # 'text': text,
        # 'voice': voice
    # }

    # try:
        # response = requests.post(url, headers=headers, json=payload)
        
        # if response.status_code != 200:
            # if response.status_code >= 500:
                # logging.error(f"Server error ({response.status_code}) when calling Eleven Labs API")
            # elif response.status_code >= 400:
                # logging.error(f"Client error ({response.status_code}) when calling Eleven Labs API")
            # elif response.status_code >= 300:
                # logging.error(f"Redirection error ({response.status_code}) when calling Eleven Labs API")
            # else:
                # logging.error(f"Unknown error ({response.status_code}) when calling Eleven Labs API")
            # return None
        
        # try:
            # response_json = response.json()
        # except ValueError:
            # logging.error("Invalid JSON response from Eleven Labs API")
            # return None
        
        # if 'error' in response_json:
            # logging.error(f"Error from Eleven Labs API: {response_json['error']}")
            # return None
        
        # return response_json

    # except requests.exceptions.RequestException as e:
        # logging.error(f"Exception when calling Eleven Labs API: {e}")
        # return None


# def text_to_speech2(voice_id, text, numero):

    # audio = generate(
        # text=text,
        # voice="Bella",
        # model='eleven_multilingual_v1'
    # )

    # Generate a unique filename for the audio files
    # ELABS_audio_filename = f'output_{int(time.time())}_{int(numero)}.mp3'
    
    # play(audio)
    # save(audio, ELABS_audio_filename)
    # return ELABS_audio_filename

    
    

def text_to_speech(elevenlabs_api_key, voice_id, text, numero):

    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
    }

    data = {
      "text": text,
      "model_id": "eleven_multilingual_v1",
      "voice_settings": {
        "stability": 0.3,
        "similarity_boost": 0.8
      }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  
        if response.status_code != 200:
            print(f'Error Response Code: {response.status_code}')
            print(f'Error Message: {response.json().get("message")}')  
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Error Connecting: {conn_err}')
    except requests.exceptions.Timeout as time_err:
        print(f'Timeout Error: {time_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'An Unexpected Error Occurred: {req_err}')
        
    print("### ELEVEN LABS RESPONSE :")
    print(response)
    print("### FIN ELEVEN LABS")
    
    
    # Generate a unique filename for the audio files
    ELABS_audio_filename = f'output_{int(time.time())}_{int(numero)}.mp3'
    with open(ELABS_audio_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return ELABS_audio_filename


# def text_to_speech_batch2(api_key, voice_id, text):
    
    # Split the text while keeping the periods
    # sentences = re.split(r'(?<=\.)', text)

    # audio_files = []
    # numero = 0
    # for sentence in sentences:
        # audio_file = text_to_speech2(voice_id, sentence, numero)
        # audio_files.append(audio_file)
        # numero += 1
        # print(audio_files)

    # return audio_files

def text_to_speech_batch(api_key, voice_id, text):
    
    # Split the text while keeping the periods
    sentences = re.split(r'(?<=\.)', text)

    audio_files = []
    numero = 0
    for sentence in sentences:
        audio_file = text_to_speech(api_key, voice_id, sentence, numero)
        audio_files.append(audio_file)
        numero += 1
        print(audio_files)

    return audio_files


def play_audio(audio_files):
    pygame.mixer.init()
    for audio_file in audio_files:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if the file is still playing
            pygame.time.Clock().tick(10)  # wait and let the music play for 1 second


def send_message():
    user_message = user_input.get()
    api_conversation.append({'role': 'user', 'content': user_message})
    # response = chat_with_gpt3(api_key, model, api_conversation)
    response = chat_with_gpt3(model, api_conversation)
    assistant_message = response['choices'][0]['message']['content']
    api_conversation.append({'role': 'assistant', 'content': assistant_message})

    conversation.append({'role': 'user', 'content': user_message, 'timestamp': timestamp()})
    
    # Text to speech
    print(assistant_message)
    # audio_files = text_to_speech_batch2(elevenlabs_api_key, voice_id, assistant_message)
    audio_files = text_to_speech_batch(elevenlabs_api_key, voice_id, assistant_message)

    conversation.append({'role': 'assistant', 'content': assistant_message, 'timestamp': timestamp(), 'audio_file': audio_files})

    chatbox.config(state='normal')
    chatbox.insert('end', f"[{conversation[-2]['timestamp']}] You: " + user_message + '\n', 'user')
    chatbox.insert('end', f"[{conversation[-1]['timestamp']}] GPT-3: " + assistant_message + '\n', 'assistant')
    chatbox.config(state='disabled')

    user_input.delete(0, 'end')

    # Play the audio
    play_audio(audio_files)




def fake_send_message():
    user_message = user_input.get()
    api_conversation.append({'role': 'user', 'content': user_message})

    assistant_message = generate_random_text(random.randint(20, 100))
    api_conversation.append({'role': 'assistant', 'content': assistant_message})

    conversation.append({'role': 'user', 'content': user_message, 'timestamp': timestamp()})
    conversation.append({'role': 'assistant', 'content': assistant_message, 'timestamp': timestamp()})

    chatbox.config(state='normal')
    chatbox.insert('end', f"[{conversation[-2]['timestamp']}] You: " + user_message + '\n', 'user')
    chatbox.insert('end', f"[{conversation[-1]['timestamp']}] GPT-3: " + assistant_message + '\n', 'assistant')
    chatbox.config(state='disabled')

    user_input.delete(0, 'end')

def start_recording():
    global recording
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)

def stop_recording():
    sd.stop()
    
    ### Transcribe the audio to text

    # Save as WAV file first
    wav_filename = 'recording.wav'
    write(wav_filename, samplerate, recording)
    
    # Convert WAV to MP3
    mp3_filename = 'recording.mp3'
    AudioSegment.from_wav(wav_filename).export(mp3_filename, format='mp3')
    
    transcription = transcribe_audio(api_key, mp3_filename)

    user_message = transcription['text']
    
    ### Send the transcribed text as a message
    user_input.insert(0, user_message)
    send_message()


def save_conversation():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, 'w') as file:
            json.dump(conversation, file)

def load_conversation():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        try:
            with open(filename, 'r') as file:
                global conversation, api_conversation
                conversation = json.load(file)

                # Create api_conversation without timestamps
                api_conversation = [{'role': msg['role'], 'content': msg['content']} for msg in conversation]

                chatbox.config(state='normal')
                chatbox.delete(1.0, 'end')
                for message in conversation:
                    tag = message['role']
                    content = message['content']
                    time = message['timestamp']
                    chatbox.insert('end', f"[{time}] {tag.capitalize()}: {content}\n", tag)
                chatbox.config(state='disabled')
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")



def clear_conversation():
    global conversation, api_conversation

    # Clear the chatbox
    chatbox.config(state='normal')
    chatbox.delete(1.0, 'end')
    chatbox.config(state='disabled')

    # Clear the conversation lists
    conversation = [{'role': 'system', 'content': system_prompt, 'timestamp': timestamp()}]
    api_conversation = [{'role': 'system', 'content': system_prompt}]

def set_system_prompt():
    global system_prompt
    system_prompt = simpledialog.askstring("Set System Prompt", "Enter system prompt:", initialvalue=system_prompt)
    clear_conversation()


def stop_recording_with_delay():
    time.sleep(1)  # Wait for 1 second
    stop_recording()  # Stop recording




### OPENAI
openai.api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv('OPENAI_API_KEY')

models = get_models()['data']



# ELEVENLABS TTS
voice_id = '21m00Tcm4TlvDq8ikWAM'
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
# set_api_key(elevenlabs_api_key)

samplerate = 44100  # Hertz
channels = 2
duration = 5  # seconds



### GUI
root = tk.Tk()
root.title("Chat with GPT-3")

# Create frames
top_frame = tk.Frame(root)
bottom_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, padx=15, pady=15)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Model selection
model_choice = simpledialog.askinteger("Model selection", "\n".join(f"{i+1}. {model['id']}" for i, model in enumerate(models)), minvalue=1, maxvalue=len(models))
model = models[model_choice - 1]['id']

# Create the chatbox
chatbox = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD)
chatbox.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Create the scrollbar
scrollbar = tk.Scrollbar(bottom_frame, command=chatbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the chatbox
chatbox['yscrollcommand'] = scrollbar.set
chatbox.tag_config('assistant', foreground='blue')
chatbox.tag_config('user', foreground='green')

# User input area
user_input = tk.Entry(top_frame, width=50)
user_input.pack(side='left', padx=15)


# Create the fake send button
fake_send_button = tk.Button(top_frame, text='Fake Send', command=fake_send_message)
fake_send_button.pack(side='right', padx=15)


# Create the buttons
send_button = tk.Button(top_frame, text='Send Message', command=send_message)
send_button.pack(side='right', padx=15)

clear_button = tk.Button(root, text='Clear Conversation', command=clear_conversation)
clear_button.pack(side='right')

# Create the save and load buttons
save_button = tk.Button(top_frame, text='Save', command=save_conversation)
save_button.pack(side='right', padx=15)

load_button = tk.Button(top_frame, text='Load', command=load_conversation)
load_button.pack(side='right', padx=15)

prompt_button = tk.Button(root, text='Set System Prompt', command=set_system_prompt)
prompt_button.pack(side='right')


record_button = tk.Button(top_frame, text='Record Message')
record_button.pack(side='right')
record_button.bind('<Button-1>', lambda event: start_recording())
record_button.bind('<ButtonRelease-1>', lambda event: stop_recording_with_delay())

### set system prompt
# system_prompt = 'You are Alfred, a helpful AI assistant.'
system_prompt = 'Tu es Alfred, un assistant hautement qualifié et terriblement drôle. Tu aimes te moquer gentilment de tes interlocuteurs mais tes réponses sont toujours pertinentes.'
set_system_prompt()


api_conversation = [{'role': 'system', 'content': system_prompt}]
conversation = [{'role': 'system', 'content': system_prompt, 'timestamp': timestamp()}]



root.mainloop()
