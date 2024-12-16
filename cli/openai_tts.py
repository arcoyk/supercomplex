from openai import OpenAI
import pygame.mixer as pm
import time
import os

OUTPUT_PATH = "voice.mp3"

class Nova:
    def __init__(self):
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key)
        pm.init()
    
    def play(self, text):
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="nova",
            input=text,
        ) as res:
            res.stream_to_file(OUTPUT_PATH)
        pm.music.load(OUTPUT_PATH)
        pm.music.play()        
        while pm.music.get_busy():
            time.sleep(0.1)

# Example usage
if __name__ == "__main__":
    tts = Nova()
    tts.play("hello, here is Nova at your service!")