import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_zhihu_news():
    url = "https://www.zhihu.com/hot"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    # 检查响应状态码
    if response.status_code != 200:
        return {"error": "Failed to retrieve the page"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    # 使用知乎热榜页面的 CSS 选择器提取问题标题
    for item in soup.find_all("div", class_="HotItem-content"):
        title = item.get_text().strip()
        link = "https://www.zhihu.com" + item.find("a")["href"]
        articles.append({"title": title, "url": link})
    
    return articles

@app.route("/api/zhihu_news")
def get_news():
    return jsonify(fetch_zhihu_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
