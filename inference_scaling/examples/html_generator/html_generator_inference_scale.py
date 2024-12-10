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
2. Suggest specific enhancements for HTML structure, inline CSS styles, and JavaScript functionality
3. Focus on both technical and design aspects
4. Consider modern web development best practices
5. Ensure all CSS and JavaScript remain within the HTML file

Current HTML code for reference:
{html}

Return only the improvement prompt without any explanations or additional text.
Keep it in short.
"""

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

Requirements:
- Keep all CSS and JavaScript within the HTML file
- Use <style> tag in the head for CSS
- Use <script> tag at the end of body for JavaScript
- Ensure styles and scripts are properly organized and commented

Current HTML:
{current_html}

Return only the improved HTML code without any explanations."""
    else:
        full_prompt = f"""Generate a complete HTML webpage based on this request:

{prompt}

Requirements:
- Include proper HTML5 structure with doctype
- Add meta viewport tag for responsiveness
- Include all CSS within a <style> tag in the head section
- Include all JavaScript within a <script> tag at the end of body section
- Structure content logically with semantic HTML
- Make it visually appealing with modern CSS styling
- Add appropriate JavaScript for interactivity where relevant
- Keep the design minimal and professional
- Ensure all code is properly organized and commented
- DO NOT use external CSS or JavaScript files
- DO NOT use CDN links for styles or scripts

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

def save(path, html):
    with open(path, 'w') as f:
        f.write(html)
        print("saved ", path)

def generate_html_with_iterations(instruction, n=3, path="results/test_page.html"):
    """
    Generate HTML from text input and iteratively improve it.
    Example: generate_html_with_iterations("create a webpage about my coffee shop in Tokyo", 1)
    """
    # Initial generation
    print("GENERATING HTML --------------- ")
    html = generate_html(instruction)
    print(html[:100])
    save(path, html)

    # Iteratively improve
    for i in range(n):
        print(f"{i} GENERATING PROMPT -----------")
        improvement_prompt = generate_prompt(html)
        print(improvement_prompt[:300])
        print(f"{i} GENERATING HTML ------------")
        html = generate_html(improvement_prompt, html)
        print(html[:300])
        save(path, html)
    
    return html

# Example usage:
if __name__ == "__main__":
    # Example text input
    instruction = "create a webpage about my coffee shop in Tokyo"
    html = generate_html_with_iterations(instruction, 1)
