from html_generator import generate_html

# Test prompts
test_inputs = [
    "英会話教室です 住所は東京都渋谷区広尾1-10-2です 電話番号は 080-44643826 ですえっとね あと ね メールアドレス @ 塾講師. com です メールアドレス info @です はいで えっと 対象は 小学校高学年から中学生ぐらいまでですで 科目は 英会話から受験まで幅広く扱っています テキストはオリジナルのものと市販のものを併用する形で行っております 月謝は週2回のコースで10万8000円です よろしくお願いします",
    "make a simple portfolio page showcasing my photography work",
    "generate a landing page for my new bakery that specializes in French pastries"
]

def save(path, html):
    # Save to a test file
    with open(path, 'w') as f:
        f.write(html)
    print(f"Generated {path} successfully!")

# Generate HTML for each test input
for i, text in enumerate(test_inputs, 1):
    try:
        print(f"\nGenerating HTML for test {i}: {text[:50]}...")
        html = generate_html(text)
        path = f'results/test_page_{i}.html'
        save(path, html)
        
    except Exception as e:
        print(f"Error generating HTML for test {i}: {str(e)}")

print("\nDone! You can open the generated HTML files in a browser to view them.")
