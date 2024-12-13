#!/usr/bin/env python3
import os
from groq import Groq
from datetime import datetime
# Initialize the Groq client
client = Groq(api_key=os.environ["GROQ_API_KEY"])


def groq(prompt):
    messages = [{"role": "user", "content": prompt}]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="mixtral-8x7b-32768",
        temperature=1.0,
    )
    # Get and print response
    return chat_completion.choices[0].message.content


def save(path, t):
    with open(path, 'a') as f:
        f.write(t)


def memorize(messages):
    prompt = f"""
    Summarize the user's key personal and context-specific facts in a concise YAML format. 
    Focus on the user’s attributes, interests, or expressed feelings. 
    Exclude general knowledge or unrelated details. 
    Keep it brief and essential.
    """
    # Convert message history to readable format
    conversation = ""
    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"    
    prompt += conversation
    memo = groq(prompt)    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memo = f"\n{current_time} ----------------------\n{memo}"
    save("memo.yaml", memo)
    print("\n[memorized]\n" + memo)


def main():    
    # Store conversation history
    messages = []
    print("Welcome to Groq CLI (Press Ctrl+C to exit)")
    try:
        while True:
            # Get user input
            user_input = input("\nuser > ")
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="mixtral-8x7b-32768",
                temperature=0.7,
            )
            # Get and print response
            response = chat_completion.choices[0].message.content
            # Create a chat completion
            print("\ngroq >", response)
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response})
    except KeyboardInterrupt:
        memorize(messages)
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
