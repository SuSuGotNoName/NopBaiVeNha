from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service  # Thêm import này cho Firefox Service
import time
import getpass

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"C:/Users/Admin/Github/geckodriver.exe"

# Tạo đối tượng Service với geckodriver path
ser = Service(gecko_path)

# Tạo tùy chọn trình duyệt Firefox
options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False  # Để False nếu muốn hiện giao diện trình duyệt

# Khởi tạo driver với Service thay vì sử dụng `executable_path`
driver = webdriver.Firefox(service=ser, options=options)

# Truy cập vào trang đăng nhập Facebook
url = 'https://www.facebook.com/login/'
driver.get(url)

# Nhập tk và mật khẩu
tk = input('Nhập tài khoản vào đê: ')
password = getpass.getpass('Nhập pass dô đi nè: ')

# Tìm phần tử và nhập tk
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(tk)

# Tìm phần tử và nhập mật khẩu
driver.find_element(By.ID, "pass").send_keys(password)

# Nhấn nút đăng nhập
driver.find_element(By.NAME, "login").click()

# Chờ đợi đăng nhập thành công
time.sleep(5)

# Truy cập vào trang chính của người dùng (bảng tin)
driver.get('https://www.facebook.com/')

# Chờ cho đến khi hộp soạn thảo bài viết "Hoàng ơi, bạn đang nghĩ gì thế?" xuất hiện
post_box_trigger = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[text()='Hoàng ơi, bạn đang nghĩ gì thế?']"))
)
post_box_trigger.click()

# Chờ đến khi hộp nhập nội dung hiện ra
content_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
)
# Nhập nội dung bài viết
content_box.send_keys("Hello ,SuSuGotNoName here !!!")

# Nhấn nút "Đăng"
post_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[text()='Đăng']"))
)
post_button.click()

# Đợi một lúc để bài viết được đăng
time.sleep(30)

# Đóng trình duyệt
driver.quit()
