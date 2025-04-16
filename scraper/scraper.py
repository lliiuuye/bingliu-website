import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_sohu_news():
    url = "https://www.sohu.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    # 检查响应状态码
    if response.status_code != 200:
        return {"error": "Failed to retrieve the page"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    # 查找搜狐首页的新闻标题
    for item in soup.find_all("h3", class_="news-title"):
        title = item.get_text().strip()
        link = item.find("a")["href"]
        articles.append({"title": title, "url": link})
    
    return articles

@app.route("/api/sohu_news")
def get_news():
    return jsonify(fetch_sohu_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
