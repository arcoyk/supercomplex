#!/usr/bin/env python3
import os
import json
from groq import Groq
from datetime import datetime
import pathlib

class GroqCLI:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.messages = []
        self.memories_file = pathlib.Path.home() / '.groq_memories.json'
        self.load_memories()

    def load_memories(self):
        if self.memories_file.exists():
            with open(self.memories_file, 'r') as f:
                self.memories = json.load(f)
        else:
            self.memories = []
            self.save_memories()

    def save_memories(self):
        with open(self.memories_file, 'w') as f:
            json.dump(self.memories, f, indent=2)

    def check_memories(self, user_input):
        # Ask Groq to check if the input relates to any existing memories
        memory_check_messages = [
            {"role": "system", "content": "You are a memory analyzer. Given the user's input and a list of memories, determine if any memories are relevant. Respond with only the relevant memories in a brief, natural way. If no memories are relevant, respond with 'No relevant memories.'"},
            {"role": "user", "content": f"User input: {user_input}\n\nMemories: {json.dumps(self.memories, indent=2)}"}
        ]
        
        completion = self.client.chat.completions.create(
            messages=memory_check_messages,
            model="mixtral-8x7b-32768",
            temperature=0.7,
        )
        
        return completion.choices[0].message.content

    def analyze_for_memories(self, conversation):
        # Ask Groq to analyze the conversation for memorable information
        memory_analysis_messages = [
            {"role": "system", "content": "You are a memory analyzer. Analyze the conversation and extract any important personal information, preferences, or significant details worth remembering. If you find something worth remembering, format it as a brief, clear statement. If nothing is worth remembering, respond with 'Nothing to memorize.'"},
            {"role": "user", "content": f"Analyze this conversation for memorable information: {json.dumps(conversation, indent=2)}"}
        ]
        
        completion = self.client.chat.completions.create(
            messages=memory_analysis_messages,
            model="mixtral-8x7b-32768",
            temperature=0.7,
        )
        
        memory_content = completion.choices[0].message.content
        if memory_content != "Nothing to memorize.":
            new_memory = {
                "content": memory_content,
                "timestamp": datetime.now().isoformat(),
                "conversation_context": conversation
            }
            self.memories.append(new_memory)
            self.save_memories()

    def run(self):
        print("Welcome to Groq CLI (Press Ctrl+C to exit)")
        
        try:
            while True:
                # Get user input
                user_input = input("user > ")
                
                # Check memories
                relevant_memories = self.check_memories(user_input)
                if relevant_memories != "No relevant memories.":
                    print("groq > Remembering:", relevant_memories)
                
                # Add user message to history
                self.messages.append({"role": "user", "content": user_input})
                
                # If there are relevant memories, include them in the context
                if relevant_memories != "No relevant memories.":
                    context_message = {"role": "system", "content": f"Relevant context from previous conversations: {relevant_memories}"}
                    completion_messages = [context_message] + self.messages
                else:
                    completion_messages = self.messages
                
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
                self.analyze_for_memories(self.messages[-2:])  # Analyze just the last exchange
                
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    cli = GroqCLI()
    cli.run()
