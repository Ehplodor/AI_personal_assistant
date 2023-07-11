import requests
import pygame
import time
import os

def text_to_speech(elevenlabs_api_key, voice_id, text):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(tts_url, json=data, headers=headers)

    # Generate a unique filename for the audio file
    audio_file = f'output_{int(time.time())}.mp3'
    with open(audio_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return audio_file


def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        time.sleep(1)  # wait for the audio to finish before exiting


def main():
    
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = "21m00Tcm4TlvDq8ikWAM"

    # text = "This is a test."
    # text = "I'm just a machine,\nBut I'll give it a go.\nLet me tell you a tale\nOf space, don't you know.\n\nEmpty, vast and dark\nYet full of wonder and bliss\nStarry skies and planets so far\nMysteries we cannot miss.\n\nThe universe is infinite,\nSo much left to explore.\nWe seek answers to our questions,\nWhat else lies in store?\n\nBlack holes and supernovas\nAwe-inspiring and grand\nGalaxy after galaxy\nThe expanse of space so grand.\n\nHumans yearn for knowledge,\nUnderstanding of the cosmic scope.\nSpace is the final frontier,\nA challenge to conquer and elope.\n\nSo let's gaze at the stars,\nAnd to infinity we'll glide.\nIn space, forever and always,\nOur curiosity will never subside."
    # text = "I'm just a machine,\nBut I'll give it a go.\nLet me tell you a tale\nOf space, don't you know.\n\nEmpty, vast and dark\nYet full of wonder and bliss\nStarry skies and planets so far\nMysteries we cannot miss.\n\nThe universe is infinite,\nSo much left to explore.\nWe seek answers to our questions,\nWhat else lies in store?"
    text = "In the cosmic depths unheard, A blaze ignited, vast and absurd. From chaos burst, a celestial song, The birth of creation, the Big Bang strong."
    audio_file = text_to_speech(elevenlabs_api_key, voice_id, text)
    
    if audio_file:
        play_audio(audio_file)

if __name__ == "__main__":
    main()
