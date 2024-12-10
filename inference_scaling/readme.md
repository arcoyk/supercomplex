# Groq API Example

This is a simple example demonstrating how to use the Groq API with Python. Groq is a high-performance AI inference platform that provides access to various language models.

## Setup

1. Install the required package:
```bash
pip install groq
```

2. Get your Groq API key:
   - Sign up at [Groq Console](https://console.groq.com)
   - Create a new API key in your account settings

3. Set your API key as an environment variable:
```bash
export GROQ_API_KEY='your-api-key-here'
```

## Running the Example

Simply run the Python script:
```bash
python groq_example.py
```

The example will:
1. Initialize a Groq client
2. Send a sample prompt about quantum computing
3. Display the response from the model

## Code Explanation

The example demonstrates:
- Setting up the Groq client
- Creating a chat completion request
- Using the Mixtral-8x7b model
- Handling the response

You can modify the prompt in the script to experiment with different queries.

## Notes

- The example uses the Mixtral-8x7b-32768 model, which is a powerful language model available through Groq
- The temperature parameter (0.7) controls response creativity - higher values make output more creative, lower values make it more focused
- Make sure to keep your API key secure and never commit it to version control
