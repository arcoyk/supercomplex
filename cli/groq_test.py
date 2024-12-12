#!/usr/bin/env python3
import os
import yaml
from groq import Groq
import pathlib

class GroqCLI:
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.messages = []
        self.memories_file = pathlib.Path.home() / '.groq_memories.yaml'
        self.memories = []
        self.save_memories()  # Start fresh with empty memories

    def load_memories(self):
        if self.memories_file.exists():
            try:
                with open(self.memories_file, 'r') as f:
                    loaded_memories = yaml.safe_load(f)
                    if isinstance(loaded_memories, list):
                        self.memories = [m for m in loaded_memories if isinstance(m, str) and m.startswith('-')]
                    else:
                        self.memories = []
            except yaml.YAMLError:
                self.memories = []
        else:
            self.memories = []

    def save_memories(self):
        # Clean up memories before saving
        self.memories = [m for m in self.memories if isinstance(m, str) and m.startswith('-')]
        with open(self.memories_file, 'w') as f:
            yaml.dump(self.memories, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def check_memories(self, user_input):
        if not self.memories:
            return None

        memory_check_messages = [
            {
                "role": "system",
                "content": """You are a memory analyzer. Given the user's input and stored memories, determine if any memories are relevant.
                If relevant memories exist, incorporate them naturally into a brief response.
                If no memories are relevant, respond with 'No relevant memories.'"""
            },
            {
                "role": "user",
                "content": f"Current input: '{user_input}'\n\nStored memories:\n" + 
                          "\n".join(self.memories)
            }
        ]
        
        completion = self.client.chat.completions.create(
            messages=memory_check_messages,
            model="mixtral-8x7b-32768",
            temperature=0.5,
        )
        
        response = completion.choices[0].message.content
        return None if response == "No relevant memories." else response

    def analyze_for_memories(self, conversation):
        memory_analysis_messages = [
            {
                "role": "system",
                "content": """You are a memory analyzer. Extract important facts about the user as simple bullet points.
                If you find something worth remembering, format it as a bullet point starting with '- '.
                Focus on concrete facts like:
                - name (e.g., "- user's name is John")
                - preferences (e.g., "- likes pizza")
                - experiences (e.g., "- visited Paris three times")
                - relationships (e.g., "- has a sister named Mary")
                
                Only output bullet points for new, concrete information.
                If nothing new to remember, respond with 'Nothing to memorize.'"""
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
            # Split into individual bullet points and add new ones
            new_points = [point.strip() for point in memory_content.split('\n') 
                         if point.strip().startswith('-') and len(point.strip()) > 2]
            for point in new_points:
                if point not in self.memories:
                    self.memories.append(point)
            self.save_memories()

    def run(self):
        print("Welcome to Groq CLI (Press Ctrl+C to exit)")
        
        try:
            while True:
                user_input = input("user > ").strip()
                if not user_input:
                    continue

                # Add user message to history
                self.messages.append({"role": "user", "content": user_input})
                
                # Check memories silently and include in context
                relevant_memories = self.check_memories(user_input)
                completion_messages = self.messages.copy()
                if relevant_memories:
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
                
                # Silently analyze and store memories
                self.analyze_for_memories(self.messages[-2:])
                
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    cli = GroqCLI()
    cli.run()
