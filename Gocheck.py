from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains,ScrollOrigin
from time import sleep
import re
import sqlite3
import pandas as pd


gch = sqlite3.connect('sqlite_gocheck.db')
c = gch.cursor()
try:
    c.execute('''
        CREATE TABLE sanpham (
            stt integer primary key autoincrement,
            ten_san_pham text, 
            gia_ban text, 
            hinh_anh text
        )   
    ''')
except Exception as e:
    print(e)

def insert_data( ten_san_pham, gia_ban, hinh_anh):
    gch = sqlite3.connect('sqlite_gocheck.db')
    c = gch.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO sanpham (ten_san_pham, gia_ban, hinh_anh)
        VALUES ( :ten_san_pham, :gia_ban, :hinh_anh)
    ''',
      {
          'ten_san_pham': ten_san_pham,
          'gia_ban': gia_ban,
          'hinh_anh': hinh_anh,
          
      })
    gch.commit()
    gch.close()
driver= webdriver.Chrome()

# Tạo url
url = 'https://gochek.vn/collections/all'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
sleep(1)

# Tìm phần tử body của trang để gửi phím mũi tên xuống
body = driver.find_element(By.TAG_NAME, "body")
sleep(3)

# Nhấn phím mũi tên xuống nhiều lần để cuộn xuống từ từ
for i in range(50):  # Lặp 30 lần, mỗi lần cuộn xuống một ít
    body.send_keys(Keys.ARROW_DOWN)
    sleep(0.01)  # Tạm dừng 0.2 giây giữa mỗi lần cuộn để trang tải nội dung

# Tạm dừng thêm vài giây để trang tải hết nội dung ở cuối trang
sleep(1)



# # Tìm tất cả các sp 
spgo = driver.find_elements(By.XPATH, "//div[contains(@class,'product-block')]")

# print(len(spgo))

# # lay tung san pham
for i, goc in enumerate(spgo, 1):

    parent_div = goc
    sp =parent_div
    
    # Lat ten sp
    try:
        ten_san_pham = sp.find_element(By.TAG_NAME, 'h3').text
    except:
        ten_san_pham=''
    
    # Lat gia sp
    try:
        gia_ban = sp.find_element(By.CLASS_NAME, "pro-price.highlight").text
        gia_ban1 = [el.text for el in gia_ban.find_elements(By.XPATH, ".//*[not(contains(@class, 'pro-price-del'))]")]
        gia_ban = " ".join(gia_ban1)
    except:
        gia_ban = sp.find_element(By.CLASS_NAME, "box-pro-prices").text

    
    # Lat hinh anh
    try:
        hinh_anh = sp.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        hinh_anh=''

    insert_data(ten_san_pham, gia_ban, hinh_anh)
driver.quit()

