import asyncio
import base64
import contextlib
import datetime
import os
import json
import wave
import itertools

from IPython.display import display, Audio
from google import genai

MODEL = "models/gemini-2.0-flash-exp"

def get_api_key():
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    return api_key

async def chat_with_gemini():
    os.environ['GOOGLE_API_KEY'] = get_api_key()
    
    client = genai.Client(
        http_options={
            'api_version': 'v1alpha',
            'url': 'generativelanguage.googleapis.com',
        }
    )

    config = {
        "generation_config": {"response_modalities": ["TEXT"]}
    }

    async with client.aio.live.connect(model=MODEL, config=config) as session:
        message = "Hello? Gemini are you there?"
        print("> ", message, "\n")
        await session.send(message, end_of_turn=True)

        # For text responses, When the model's turn is complete it breaks out of the loop.
        async for response in session:
            model_turn = response.server_content.model_turn
            for part in model_turn.parts:
                print("- ", part.text)

if __name__ == "__main__":
    asyncio.run(chat_with_gemini())
