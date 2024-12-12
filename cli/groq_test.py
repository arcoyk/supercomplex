#!/usr/bin/env python3
import os
from groq import Groq

def main():
    # Initialize the Groq client
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    # Store conversation history
    messages = []
    
    print("Welcome to Groq CLI (Press Ctrl+C to exit)")
    
    try:
        while True:
            # Get user input
            user_input = input("user > ")
            
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Create a chat completion
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="mixtral-8x7b-32768",
                temperature=0.7,
            )
            
            # Get and print response
            response = chat_completion.choices[0].message.content
            print("groq >", response)
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response})
            
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
