from html_generator_inference_scale import generate_html_with_iterations

# Test prompts
test_inputs = [
    "英会話教室です 住所は東京都渋谷区広尾1-10-2です 電話番号は 080-44643826 ですえっとね あと ね メールアドレス @ 塾講師. com です メールアドレス info @です はいで えっと 対象は 小学校高学年から中学生ぐらいまでですで 科目は 英会話から受験まで幅広く扱っています テキストはオリジナルのものと市販のものを併用する形で行っております 月謝は週2回のコースで10万8000円です よろしくお願いします",
    "make a simple portfolio page showcasing my photography work",
    "generate a landing page for my new bakery that specializes in French pastries"
]

# Generate HTML for each test input
for i, text in enumerate(test_inputs, 1):
    try:
        path = f"results/test_page_{i}.html"
        html = generate_html_with_iterations(text, n=3, path=path)
    except Exception as e:
        print(f"Error in test {i}: {str(e)}")

print("\nDone! Generated HTML files can be opened in a browser.")
