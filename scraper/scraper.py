import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_toutiao_news():
    url = "https://www.toutiao.com/ch/news_tech/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select("div.toutiao-card__title a")[:5]:  # 选取前5个新闻
        title = item.text.strip()
        link = "https://www.toutiao.com" + item["href"]
        articles.append({"title": title, "url": link})

    return articles

@app.route("/api/toutiao_news")
def get_news():
    return jsonify(fetch_toutiao_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
