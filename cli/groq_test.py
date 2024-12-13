#!/usr/bin/env python3
import os
from groq import Groq
from datetime import datetime

# Const
MEMO_PATH = "memo.yaml"
GUIDE_PATH = "guide.yaml"

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


def save(path, t, mode="a"):
    with open(path, mode) as f:
        f.write(t)


def read(path):
    with open(path) as f:
        c = f.read()
    return c


def block(content, title, s="----------------"):
    return f"\n[{title}]{s}\n{content}"


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def memorize():
    prompt = f"""
    Summarize the user's key personal and context-specific facts in a concise YAML format. 
    Focus on the user’s attributes, interests, or expressed feelings. 
    Exclude general knowledge or unrelated details. 
    Keep it brief and essential.
    """
    # Convert message history to readable format
    conversation = ""
    for msg in messages:
        if msg["role"] == "system":
            continue
        conversation += f"{msg['role']}: {msg['content']}\n"
    prompt += conversation
    memo = groq(prompt)
    memo = block(memo, current_time())
    save(MEMO_PATH, memo)


def remember():
    guide = read(GUIDE_PATH)
    mem = f"[USE THIS MEMORY ONLY WHEN NEEDED] {read(MEMO_PATH)}"
    messages.append({"role": "system", "content": guide})
    messages.append({"role": "system", "content": mem})
    print(guide, mem)


# Add capability to choose proper memory on-the-fly on-demand.
# This feature maybe a part of function calling / function selecting features.

def main():    
    # Store conversation history
    print("Welcome to Groq CLI (Press Ctrl+C to exit)")
    remember()
    try:
        while True:
            user_input = input("\nuser > ")
            messages.append({"role": "user", "content": user_input})
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="mixtral-8x7b-32768",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            print("\ngroq >", response)
            messages.append({"role": "assistant", "content": response})
    except KeyboardInterrupt:
        memorize()
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
