from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re

# Cấu hình WebDriver để chạy ẩn (không mở cửa sổ trình duyệt)
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ở chế độ headless
chrome_options.add_argument("--disable-gpu")  # Tắt GPU tăng tốc
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Tạo nơi chứa links và dataframe rỗng
all_links = []
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

# Lấy tất cả đường dẫn đến painters từ Wikipedia
for i in range(65, 91):  # Chỉ chạy với trang chữ "F" (ASCII = 70)
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{chr(i)}%22"
    try:
        driver.get(url)
        time.sleep(3)  # Đợi trang tải

        # Lấy tất cả thẻ ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")

        # Lấy thẻ ul chứa thông tin painters (thường nằm ở vị trí thứ 21)
        if len(ul_tags) > 20:
            ul_painters = ul_tags[20]
        else:
            print(f"Không tìm thấy thông tin painters trên trang {url}")
            driver.quit()
            continue

        # Lấy tất cả thẻ <li> thuộc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tạo danh sách các url
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        all_links.extend(links)
    except Exception as e:
        print(f"Error: {e}")
    driver.quit()

# Lấy thông tin của từng họa sĩ
count = 0
for link in all_links:
    if count > 2:  # Chỉ lấy thông tin 100 họa sĩ đầu tiên để tránh mất thời gian
        break
    count += 1
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)
        time.sleep(2)

        # Lấy thông tin chi tiết
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = re.findall(r'[0-9]{1,2} +\s+[A-Za-z]+\s+[0-9]{4}', birth_element.text)[0]
        except:
            birth = ""

        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = re.findall(r'[0-9]{1,2} +\s+[A-Za-z]+\s+[0-9]{4}', death_element.text)[0]
        except:
            death = ""

        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        # Tạo dictionary thông tin họa sĩ
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}

        # Chuyển đổi dictionary thành DataFrame
        painter_df = pd.DataFrame([painter])

        # Thêm thông tin vào DF chính
        d = pd.concat([d, painter_df], ignore_index=True)

        driver.quit()
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()

# Lưu DataFrame vào file Excel
file_name = 'Painters.xlsx'
d.to_excel(file_name, index=False)
print(f'DataFrame đã được lưu thành công vào file: {file_name}')
