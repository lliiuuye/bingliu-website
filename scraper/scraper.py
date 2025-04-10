import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# 更新为爬取 TechCrunch 的科技新闻
def fetch_techcrunch_news():
    url = "https://techcrunch.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    # TechCrunch 网站的新闻结构是通过 <a> 标签在 <h2> 标签下
    for item in soup.select("h2 a")[:15]:  # 只获取前5条新闻
        title = item.get_text(strip=True)
        link = item["href"]
        if not link.startswith("http"):
            link = "https://techcrunch.com" + link  # 补全相对链接
        articles.append({"title": title, "url": link})

    return articles

@app.route("/api/techcrunch_news")
def get_news():
    return jsonify(fetch_techcrunch_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
