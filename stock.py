from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sqlite3
import time

# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('stock.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE stock (
            id integer primary key autoincrement,
            _date text,
            open_price integer,
            highest_price integer,
            lowest_price integer,
            closing_price integer,
            changed_price integer,
            price_change_percentage real,
            changed_volume integer
        )
    ''')
except Exception as e:
    print(e)

# Hàm chèn dữ liệu
def insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO stock(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)
        VALUES (:_date, :open_price, :highest_price, :lowest_price, :closing_price, :changed_price, :price_change_percentage, :changed_volume)
    ''', {
        '_date': _date,
        'open_price': open_price,
        'highest_price': highest_price,
        'lowest_price': lowest_price,
        'closing_price': closing_price,
        'changed_price': changed_price,
        'price_change_percentage': price_change_percentage,
        'changed_volume': changed_volume
    })
    conn.commit()
    conn.close()

# 1. Thu thập dữ liệu từ website
# Đường dẫn đến file thực thi geckodriver
gecko_path = r"C:/Users/Admin/Github/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường dẫn geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options();
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox hiển thị giao diện (False: hiện giao diện)
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)
# Truy cập trang web cần lấy dữ liệu
driver.get("https://simplize.vn/co-phieu/SAB/lich-su-gia")
time.sleep(5)

# Lấy toàn bộ hàng trong bảng
rows = driver.find_elements(By.CSS_SELECTOR, ".simplize-table-row.simplize-table-row-level-0")
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    _date = columns[0].text
    open_price = int(columns[1].text.replace(",", ""))
    highest_price = int(columns[2].text.replace(",", ""))
    lowest_price = int(columns[3].text.replace(",", ""))
    closing_price = int(columns[4].text.replace(",", ""))
    changed_price = int(columns[5].text.replace(",", "") if columns[5].text != '-' else 0)
    price_change_percentage = float(columns[6].text.replace(",", "").replace("%", "") if columns[6].text != '-' else 0)
    changed_volume = int(columns[7].text.replace(",", ""))

    insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)

driver.quit()

# 2. Thực hiện các truy vấn

# Kết nối cơ sở dữ liệu
conn = sqlite3.connect('stock.db')
c = conn.cursor()

# Câu 1: Ngày và giá cổ phiếu đóng cửa cao nhất
c.execute('''
    SELECT _date, closing_price
    FROM stock
    WHERE closing_price = (SELECT MAX(closing_price) FROM stock)
''')
result_max = c.fetchone()
if result_max:
    print(f"Ngày có giá cổ phiếu đóng cửa cao nhất: {result_max[0]} với giá: {result_max[1]}")

# Câu 2: Giá cổ phiếu đóng cửa thấp nhất
c.execute('SELECT MIN(closing_price) FROM stock')
result_min = c.fetchone()
print(f"Giá cổ phiếu đóng cửa thấp nhất: {result_min[0]}")

# Câu 3: Trung bình giá cổ phiếu đóng cửa trong 30 ngày gần nhất
c.execute('SELECT AVG(closing_price) FROM (SELECT closing_price FROM stock ORDER BY _date DESC LIMIT 30)')
result_avg = c.fetchone()
print(f"Trung bình giá cổ phiếu đóng cửa trong 30 ngày gần nhất: {result_avg[0]}")

# Đóng kết nối
conn.close()
