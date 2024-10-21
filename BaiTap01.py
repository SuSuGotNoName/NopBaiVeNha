from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#khoi tao webdriver
driver = webdriver.Chrome()

#mo trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name"
driver.get(url)

#doi khoang 2 s
time.sleep(2)

#Lay tat ca cac the <a>
tags = driver.find_elements(By.TAG_NAME, "a")

#tao ra danh sach lien ket
links = [tag.get_attribute("href") for tag in tags]

#xuat thong tin ra
for link in links:
    print(link)

#dong webdriver
driver.quit()