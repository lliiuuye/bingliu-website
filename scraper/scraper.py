import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_techcrunch_news():
    url = "https://techcrunch.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    print(soup.prettify())  # 输出格式化的 HTML 内容以查看结构

    articles = []
    for item in soup.select("a[data-qa='story-card-title']"):
        print(item)  # 输出每个匹配的新闻链接，调试用
        title = item.text.strip()
        link = item["href"]
        articles.append({"title": title, "url": link})

    return articles

@app.route("/api/techcrunch_news")
def get_news():
    return jsonify(fetch_techcrunch_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
