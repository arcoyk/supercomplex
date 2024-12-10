import os
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "your-api-key-here")
)

def groq(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content

def generate_html(text):
    prompt = f"""Generate a complete, well-structured HTML webpage based on this request: "{text}"
Requirements:
- Include proper HTML5 structure with doctype
- Add meta viewport tag for responsiveness
- Include clean, modern CSS styling
- Structure content logically with semantic HTML
- Make it visually appealing and readable
- Keep the design minimal and professional
Generate only the HTML code without any explanations."""
    return groq(prompt)

if __name__ == "__main__":
    text = "create a webpage about my coffee shop in Tokyo"
    html = generate_html(text)
    with open('generated_page.html', 'w') as f:
        f.write(html)
    print("Generated HTML page saved as 'generated_page.html'")
