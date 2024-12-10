import os
from groq import Groq

# Initialize the Groq client
# Note: You need to set your GROQ_API_KEY environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "your-api-key-here")
)

def main():
    # Example prompt
    prompt = "Explain what makes quantum computing different from classical computing in 2 sentences."

    print("Sending request to Groq...")
    
    # Make the API call
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",  # Using Mixtral model
        temperature=0.7,
    )

    # Get the response
    response = chat_completion.choices[0].message.content
    
    print("\nResponse from Groq:")
    print(response)

if __name__ == "__main__":
    main()
