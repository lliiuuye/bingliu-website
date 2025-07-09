import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')  # 关键：无头模式
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)


# 启动 Chrome 浏览器（Headless）
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://tech.sina.com.cn/")


# 等待目标文章元素加载出来
wait = WebDriverWait(driver, 10)
time.sleep(10)  # 等页面完全渲染

wait.until(EC.presence_of_element_located((By.XPATH, '//a[@target="_blank" and string-length(text()) > 10]')))

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

# 输出调试信息
print(f"✅ 抓到 {len(titles)} 条标题")
for i, (title, _) in enumerate(titles, 1):
    print(f"{i}. {title}")

driver.quit()

# 构造插入 HTML 的 JavaScript 脚本内容11
news_items_html = ""
for title, href in titles:
    news_items_html += f"""<div class="news-item"><a href="{href}" target="_blank">{title}</a></div>\n"""

js_script = f"""
<script>
    document.addEventListener("DOMContentLoaded", function() {{
        const container = document.getElementById("news-container");
        if (container) {{
            container.innerHTML = `{news_items_html}`;
        }} else {{
            console.error("❌ 没找到 news-container 元素！");
        }}
    }});
</script>
"""

# 读取原始 HTML 文件
with open("public/index_temp.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 插入 JS 到 </body> 前
if "</body>" in html_content:
    html_content = html_content.replace("</body>", js_script + "\n</body>")
else:
    html_content += js_script  # 兜底：如果没 </body>，就直接加上去

# 写入新的 HTML 文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 已生成 index.html，打开即可看到技术动态区域更新！")
