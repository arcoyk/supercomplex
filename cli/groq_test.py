#!/usr/bin/env python3
import os
from groq import Groq
from datetime import datetime

# Const
MEMO_PATH = "memo.yaml"

# Initialize
messages = []
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


def save(path, t, mode='a'):
    with open(path, mode) as f:
        f.write(t)


def read(path):
    with open(path) as f:
        c = f.read()
    return c


def refine_memory():
    prompt = f"""
    This is a log of chat. Remove redundant logs.
    """
    mem = read(MEMO_PATH)
    prompt = f"{prompt}\n---------\n{mem}"
    mem = groq(prompt)
    print(f"\n\n\n\n\n\n UPDATED ================== \n\n {mem}")
    save(MEMO_PATH, mem, 'w')


def memorize():
    prompt = f"""
    Summarize the user's key personal and context-specific facts in a concise YAML format. 
    Focus on the user’s attributes, interests, or expressed feelings. 
    Exclude general knowledge or unrelated details. 
    Keep it brief and essential.
    Update or exclude [PREREQUISITE]
    """
    # Convert message history to readable format
    conversation = ""
    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"    
    prompt += conversation
    memo = groq(prompt)    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memo = f"\n{current_time} ----------------------\n{memo}"
    save(MEMO_PATH, memo)
    print("\n[memorized]\n" + memo)


def remember():
    mem = read(MEMO_PATH)
    rem = f"[PREREQUISITE] \n {mem}"
    print(rem)
    messages.append({"role": "system", "content": rem})


def main():    
    # Store conversation history
    print("Welcome to Groq CLI (Press Ctrl+C to exit)")
    remember()
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
        memorize()
        refine_memory()
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
