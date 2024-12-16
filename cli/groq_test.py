#!/usr/bin/env python3
import os
from groq import Groq
from datetime import datetime
MEMO_PATH = "memo.yaml"
messages = []
client = Groq(api_key=os.environ["GROQ_API_KEY"])


def groq(prompt, messages=[], role="assistant"):
    messages.append({"role": role, "content": prompt})
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )
    content = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": content})
    return messages


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


def refine_memory():
    mem = read(MEMO_PATH)
    prompt = f"""
Remove redundancy from this log. Output in YAML
--------------------------------------------------
{mem}
"""
    print(prompt)
    mem = groq(prompt)
    save(MEMO_PATH, mem[-1]["content"], mode="w")


def memorize():
    prompt = f"""
Summarize the user's key personal and context-specific facts in a concise YAML format. 
Focus on the user’s attributes, interests, or expressed feelings. 
Exclude general knowledge or unrelated details. 
Keep it brief and essential.
    """
    memo = groq(prompt, messages=messages)
    memo = memo[-1]["content"]
    print(memo)
    memo = block(memo, current_time())
    save(MEMO_PATH, memo)


def remember():
    mem = read(MEMO_PATH)
    prompt = f"""
This is memory you have.
Use this memory ONLY when you think needed.
===========================================
{mem}
===========================================
    """
    messages.append({"role": "system", "content": prompt})


def show_messages():
    print("\n\n\n\n\n\n")
    for m in messages:
        print(f"{m['role']}: {m['content']}\nv\nv\nv\n")
    print("\n\n\n\n\n\n")


def add_guide():
    prompt = """
You're a kind and smart assistant.
- Answer in 3 words.
- Think deep.
Start conversation
"""
    messages.append({"role": "system", "content": prompt})


def inference(n=3):
    prompt = f"""
Carefully consider if there are any missing perspectives, and improve the response if there are.
"""
    for i in range(n):
        print(f"{i}/{n} ================= INFERENCE")
        groq(prompt, messages, "user")
        print(messages[-1]["content"])


def init_all():
    print("Welcome to Groq CLI (Press Ctrl+C to exit)")
    add_guide()
    remember()


def main():
    init_all()
    try:
        while True:
            user_input = input("\nuser > ")
            groq(user_input, messages, "user")
            inference()
            # show_messages()
            print("\ngroq >", messages[-1]["content"])
    except KeyboardInterrupt:
        memorize()
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
