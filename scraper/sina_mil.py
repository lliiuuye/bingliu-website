
# sina_mil.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 打开新浪军事频道
driver.get("https://mil.news.sina.com.cn/")

# 等待页面加载
time.sleep(3)

# 获取文章标题
titles = driver.find_elements(By.XPATH, '//a[@target="_blank" and string-length(text()) > 10]')

print("获取到的文章标题如下：\n")
for i, title in enumerate(titles, 1):
    text = title.text.strip()
    if text:
        print(f"{i}. {text}")

driver.quit()
