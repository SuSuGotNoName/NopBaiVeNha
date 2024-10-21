from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

# Tạo DataFrame để lưu thông tin họa sĩ
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

# Khởi tạo webdriver
driver = webdriver.Chrome()

# Duyệt qua từng chữ cái từ A đến Z
for i in range(65, 91):
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{chr(i)}%22"
    try:
        # Mở trang danh sách họa sĩ
        driver.get(url)

        # Đợi cho các thẻ ul xuất hiện
        wait = WebDriverWait(driver, 10)
        ul_tags = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "ul")))

        # Kiểm tra chỉ số và chọn thẻ ul phù hợp
        if len(ul_tags) > 20:
            ul_painters = ul_tags[20]

            # Lấy tất cả thẻ <li> thuộc ul_painters
            li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

            # Lấy danh sách link và tên họa sĩ
            links = [li.find_element(By.TAG_NAME, "a").get_attribute("href") for li in li_tags]

            # Truy cập từng trang họa sĩ để lấy thông tin chi tiết
            for link in links:
                try:
                    driver.get(link)

                    # Đợi tải trang
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

                    # Lấy tên họa sĩ
                    try:
                        name = driver.find_element(By.TAG_NAME, "h1").text
                    except Exception as e:
                        name = ""
                        print(f"Lỗi khi lấy tên: {e}")

                    # Lấy ngày sinh
                    try:
                        birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
                        birth = re.findall(r'[0-9]+\s[A-Za-z]+\s+[0-9]{4}', birth_element.text)[0]
                    except Exception as e:
                        birth = ""
                        print(f"Lỗi khi lấy ngày sinh: {e}")

                    # Lấy ngày mất
                    try:
                        death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
                        death = re.findall(r'[0-9]+\s[A-Za-z]+\s+[0-9]{4}', death_element.text)[0]
                    except Exception as e:
                        death = ""
                        print(f"Lỗi khi lấy ngày mất: {e}")

                    # Lấy quốc tịch
                    try:
                        nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
                        nationality = nationality_element.text
                    except Exception as e:
                        nationality = ""
                        print(f"Lỗi khi lấy quốc tịch: {e}")

                    # Tạo dictionary lưu thông tin họa sĩ
                    painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}

                    # Thêm vào DataFrame
                    d = pd.concat([d, pd.DataFrame([painter])], ignore_index=True)

                except Exception as e:
                    print(f"Lỗi khi truy cập trang {link}: {e}")

        else:
            print(f"Không tìm thấy thẻ ul phù hợp cho ký tự {chr(i)}")

    except Exception as e:
        print(f"Lỗi xảy ra với ký tự {chr(i)}: {e}")

# Lưu DataFrame vào file Excel
output_file = 'painters_info.xlsx'
d.to_excel(output_file, index=False)
print(f"Dữ liệu đã được lưu vào {output_file}")

# Đóng trình duyệt
driver.quit()
