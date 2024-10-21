from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome();

#mo 1 trang web
driver.get("https://gomotungkinh.com/")
time.sleep(5)
#tim phan tu img
bonk_img = driver.find_element(By.ID, "bonk")


while True:
    bonk_img.click()
    print("daasdsad")
    time.sleep(0.5)