# 抓取動態網頁，使用 selenuium，需要下載 pip install selenium


# 安裝 webDriver，https://sites.google.com/chromium.org/driver/downloads?authuser=0 找對應的版本即可
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# # 測試用
# import time
# 方法 1 手動下載 ChromeDriver
# driver = webdriver.Chrome("./chromedriver")
# time.sleep(10)
# driver.quit()




# 方法 2 自動下載 ChromeDriver
# 安裝 webdriver-manager 套件，需要下載 pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://zh-tw.facebook.com/"
email = "vin318@yahoo.com.tw"
password = "avincent1255"

# 避免跳出通知
chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

# 使用 ChromeDriverManager 自動下載 chromedriver
driver = webdriver.Chrome( ChromeDriverManager().install(), chrome_options = chrome_options )

# 最大化視窗
driver.maximize_window()

# 進入 fb 登入畫面
driver.get(url)

# 填入帳號密碼，送出
driver.find_element_by_id("email").send_keys(email)
driver.find_element_by_id("pass").send_keys(password)
driver.find_element_by_name("login").click()

# 等 5 秒，讓 fb 有時間處理資料
time.sleep(5)

# 關閉瀏覽器
# driver.quit()

# 進入 博客來 的粉專
driver.get("https://www.facebook.com/bookstw/")
time.sleep(5)

# 因為 fb 動態頁面需要滾動至對應位置才會有資料出來
# 模擬向下滾動的行為，滑動 3 次
for x in range(3):
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
  print("scroll")
  time.sleep(5)

# 取得網頁資料，在取得文章
root = BeautifulSoup(driver.page_source, "html.parser")
titles = root.find_all("div", class_="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a")

for title in titles:
  posts = title.find_all("div", dir="auto")
  if len(posts):
    for post in posts:
      print(post.text)
  
  print("-" * 30)

  # 取得照片，照片或相簿的位置一起抓
  images = root.find_all(
    "img", class_ = ["i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6", "i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm"])

  if len(images) != 0:
      for index, image in enumerate(images):
        img = requests.get(image['src'])
        with open(f"images/img{ index + 1 }.jpg", "wb") as file:
          file.write(img.content)
        print(f"第 { index + 1 } 張圖片下載完成 !")
