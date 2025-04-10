import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_bbc_news():
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("a", class_="gs-c-promo-heading"):
        title = item.get_text().strip()
        link = "https://www.bbc.com" + item.get("href")
        articles.append({"title": title, "url": link})

    return articles

@app.route("/api/bbc_news")
def get_news():
    return jsonify(fetch_bbc_news())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
