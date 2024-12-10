import os
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "your-api-key-here")
)

def generate_prompt(html):
    """Use Groq to generate a dynamic improvement prompt"""
    prompt = f"""You are an expert web developer. Generate a prompt that will guide improvements to this HTML code. The prompt should:
1. Identify areas that need improvement
2. Suggest specific enhancements
3. Focus on both technical and design aspects
4. Consider modern web development best practices

Current HTML code for reference:
{html}

Return only the improvement prompt without any explanations or additional text."""

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

def generate_html(prompt, current_html=None):
    """
    Generate HTML based on a prompt and optionally existing HTML.
    If current_html is provided, it will be used as context for improvements.
    """
    if current_html:
        full_prompt = f"""Improve this HTML code based on the following requirements:

{prompt}

Current HTML:
{current_html}

Return only the improved HTML code without any explanations."""
    else:
        full_prompt = f"""Generate a complete HTML webpage based on this request:

{prompt}

Requirements:
- Include proper HTML5 structure with doctype
- Add meta viewport tag for responsiveness
- Include clean, modern CSS styling
- Structure content logically with semantic HTML
- Make it visually appealing and readable
- Keep the design minimal and professional

Return only the HTML code without any explanations."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.7,
    )
    
    return chat_completion.choices[0].message.content

def generate_html_with_iterations(instruction, n=3):
    """
    Generate HTML from text input and iteratively improve it.
    Example: generate_html_with_iterations("create a webpage about my coffee shop in Tokyo")
    """
    # Initial generation
    print("GENERATING HTML --------------- ")
    html = generate_html(instruction)
    print(html[:100])

    # Iteratively improve
    for i in range(n):
        print(f"{i} GENERATING PROMPT -----------")
        improvement_prompt = generate_prompt(html)
        print(improvement_prompt[:300])
        print(f"{i} GENERATING HTML ------------")
        html = generate_html(improvement_prompt, html)
        print(html[:300])
    
    return html

# Example usage:
if __name__ == "__main__":
    # Example text input
    instruction = "create a webpage about my coffee shop in Tokyo"
    html = generate_html_with_iterations(instruction)
    # Save the result
    with open('generated_page.html', 'w') as f:
        f.write(html)
