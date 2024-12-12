#!/usr/bin/env python3
import os
import yaml
from groq import Groq
from datetime import datetime
import pathlib

class GroqCLI:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.messages = []
        self.memories_file = pathlib.Path.home() / '.groq_memories.yaml'
        self.load_memories()

    def load_memories(self):
        if self.memories_file.exists():
            try:
                with open(self.memories_file, 'r') as f:
                    self.memories = yaml.safe_load(f) or []
            except yaml.YAMLError:
                self.memories = []
        else:
            self.memories = []
        self.save_memories()

    def save_memories(self):
        with open(self.memories_file, 'w') as f:
            yaml.dump(self.memories, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def check_memories(self, user_input):
        if not self.memories:
            return "No memories stored yet."

        memory_check_messages = [
            {
                "role": "system",
                "content": """You are a memory analyzer. Given the user's input and stored memories, determine if any memories are relevant.
                If relevant memories exist, naturally incorporate them into a brief response.
                Focus on personal details, preferences, and important facts about the user.
                If no memories are relevant, respond with 'No relevant memories.'"""
            },
            {
                "role": "user",
                "content": f"Current input: '{user_input}'\n\nStored memories:\n" + 
                          "\n".join([f"- {m['content']} ({m['timestamp']})" for m in self.memories])
            }
        ]
        
        completion = self.client.chat.completions.create(
            messages=memory_check_messages,
            model="mixtral-8x7b-32768",
            temperature=0.5,
        )
        
        return completion.choices[0].message.content

    def analyze_for_memories(self, conversation):
        memory_analysis_messages = [
            {
                "role": "system",
                "content": """You are a memory analyzer. Analyze the conversation for important information about the user.
                Focus on:
                - Personal details (name, preferences, interests)
                - Important facts or experiences
                - Significant statements or opinions
                If you find something worth remembering, provide a clear, concise statement.
                If nothing is worth remembering, respond with 'Nothing to memorize.'"""
            },
            {
                "role": "user",
                "content": f"Analyze this exchange for memorable information:\nUser: {conversation[0]['content']}\nAssistant: {conversation[1]['content']}"
            }
        ]
        
        completion = self.client.chat.completions.create(
            messages=memory_analysis_messages,
            model="mixtral-8x7b-32768",
            temperature=0.5,
        )
        
        memory_content = completion.choices[0].message.content
        if memory_content.lower() != "nothing to memorize.":
            new_memory = {
                "content": memory_content,
                "timestamp": datetime.now().isoformat(),
                "conversation_context": [
                    {
                        "role": msg["role"],
                        "content": msg["content"]
                    } for msg in conversation
                ]
            }
            self.memories.append(new_memory)
            self.save_memories()
            return f"[Memorized] {memory_content}"
        return None

    def run(self):
        print("Welcome to Groq CLI with Memory (Press Ctrl+C to exit)")
        print("Memories are stored in:", self.memories_file)
        
        try:
            while True:
                user_input = input("user > ").strip()
                if not user_input:
                    continue

                # Check memories before responding
                relevant_memories = self.check_memories(user_input)
                if relevant_memories != "No relevant memories." and relevant_memories != "No memories stored yet.":
                    print("groq > [Memory] " + relevant_memories)

                # Add user message to history
                self.messages.append({"role": "user", "content": user_input})
                
                # Include memory context in the conversation
                completion_messages = self.messages.copy()
                if relevant_memories != "No relevant memories." and relevant_memories != "No memories stored yet.":
                    completion_messages.insert(0, {
                        "role": "system",
                        "content": f"Context from previous conversations: {relevant_memories}"
                    })
                
                # Create a chat completion
                chat_completion = self.client.chat.completions.create(
                    messages=completion_messages,
                    model="mixtral-8x7b-32768",
                    temperature=0.7,
                )
                
                # Get and print response
                response = chat_completion.choices[0].message.content
                print("groq >", response)
                
                # Add assistant response to history
                self.messages.append({"role": "assistant", "content": response})
                
                # Analyze conversation for memories after each exchange
                memory_result = self.analyze_for_memories(self.messages[-2:])
                if memory_result:
                    print("groq >", memory_result)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    cli = GroqCLI()
    cli.run()
