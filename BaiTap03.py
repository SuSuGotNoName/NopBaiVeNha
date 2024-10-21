from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#khoi tao webdriver
driver = webdriver.Chrome()

#mo trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)

#doi khoang 2 s
time.sleep(2)

#lay cac the ul
ul_tags = driver.find_elements(By.TAG_NAME, "ul" )

#chon the ul thu 2
ul_painters = ul_tags[20]

#lay tat ca the <li> thuoc cl_painters
li_tags = ul_painters.find_elements(By.TAG_NAME, "li")


#tao danh sach url
links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]

titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]


for link in links:
    print(link)

for title in titles:
    print(title)


driver.quit()