from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://mil.news.sina.com.cn/")
time.sleep(3)

# 提取文章标题和链接
elements = driver.find_elements(By.XPATH, '//a[@target="_blank" and string-length(text()) > 10]')

# 筛选前 10 条标题
titles = []
for el in elements:
    title = el.text.strip()
    href = el.get_attribute("href")
    if title and href:
        titles.append((title, href))
    if len(titles) >= 10:
        break

driver.quit()

# 构造插入 HTML 的 JavaScript 脚本内容
news_items_html = ""
for title, href in titles:
    news_items_html += f"""<div class="news-item"><a href="{href}" target="_blank">{title}</a></div>\n"""

js_script = f"""
<script>
    document.getElementById("news-container").innerHTML = `{news_items_html}`;
</script>
"""

# 读取原始 HTML 文件，插入 JavaScript 到 </body> 前
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 插入 JS 到 </body> 前
html_content = html_content.replace("</body>", js_script + "\n</body>")

# 写入新的 HTML 文件
with open("index_with_news.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 已生成 index_with_news.html，打开即可看到技术动态区域更新啦！")
