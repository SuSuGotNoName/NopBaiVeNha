from pymongo import MongoClient
from datetime import datetime

# Bước 1: Kết nối với MongoDB và tạo cơ sở dữ liệu
client = MongoClient('mongodb://localhost:27017/')
client.drop_database('driveManagement')
db = client['driveManagement']  # Tạo cơ sở dữ liệu driveManagement

# Bước 2: Tạo bộ sưu tập và thêm dữ liệu
files_collection = db['files']  # Tạo bộ sưu tập files

# Thêm dữ liệu vào bộ sưu tập 'files'
files_data = [
    { 'file_id': 1, 'name': "Report.pdf", 'size': 2048, 'owner': "Nguyen Van A", 'created_at': datetime(2024, 1, 10), 'shared': False },
    { 'file_id': 2, 'name': "Presentation.pptx", 'size': 5120, 'owner': "Tran Thi B", 'created_at': datetime(2024, 1, 15), 'shared': True },
    { 'file_id': 3, 'name': "Image.png", 'size': 1024, 'owner': "Le Van C", 'created_at': datetime(2024, 1, 20), 'shared': False },
    { 'file_id': 4, 'name': "Spreadsheet.xlsx", 'size': 3072, 'owner': "Pham Van D", 'created_at': datetime(2024, 1, 25), 'shared': True },
    { 'file_id': 5, 'name': "Notes.txt", 'size': 512, 'owner': "Nguyen Thi E", 'created_at': datetime(2024, 1, 30), 'shared': False }
]
files_collection.insert_many(files_data)  # Chèn dữ liệu vào collection

# Bước 3: Thực hiện các truy vấn để quản lý tệp

# 3.1: Xem tất cả tệp trong bộ sưu tập 'files'
print("Tất cả tệp:")
for file in files_collection.find():
    print(file)

# 3.2: Tìm tệp có kích thước lớn hơn 2000KB
print("\nTệp có kích thước lớn hơn 2000KB:")
for file in files_collection.find({ 'size': { '$gt': 2000 } }):
    print(file)

# 3.3: Đếm tổng số tệp
file_count = files_collection.count_documents({})
print(f"\nTổng số tệp: {file_count}")

# 3.4: Tìm tất cả tệp được chia sẻ
print("\nTệp được chia sẻ:")
for file in files_collection.find({ 'shared': True }):
    print(file)

# 3.5: Thống kê số lượng tệp theo chủ sở hữu
print("\nSố lượng tệp theo chủ sở hữu:")
owners_file_count = files_collection.aggregate([
    { '$group': { '_id': "$owner", 'count': { '$sum': 1 } } }
])
for owner in owners_file_count:
    print(owner)

# Bước 4: Cập nhật và xóa thông tin tệp

# 4.1: Cập nhật trạng thái chia sẻ của tệp với file_id = 1 thành true
files_collection.update_one({ 'file_id': 1 }, { '$set': { 'shared': True } })

# 4.2: Xóa tệp với file_id = 3
files_collection.delete_one({ 'file_id': 3 })

# Bước 5: Xem lại dữ liệu sau khi cập nhật và xóa
# Kiểm tra lại tất cả tệp trong bộ sưu tập
print("\nTất cả tệp sau khi cập nhật và xóa:")
for file in files_collection.find():
    print(file)
# // Câu hỏi 1: Tìm tất cả tệp của người dùng có tên là "Nguyen Van A".
# db.files.find({ owner: "Nguyen Van A" })
print('\n Tat ca tep cua nguoi dung NVA')
files_collection.find({"owner":"Nguyen Van A"})
for select in files_collection.find():
    print(select)
# // Câu hỏi 2: Tìm tệp lớn nhất trong bộ sưu tập.
# db.files.find().sort({ size: -1 }).limit(1)
#
# // Câu hỏi 3: Tìm số lượng tệp có kích thước nhỏ hơn 1000KB.
# db.files.countDocuments({ size: { $lt: 1000 } })
#
# // Câu hỏi 4: Tìm tất cả tệp được tạo trong tháng 1 năm 2024.
# db.files.find({
#     created_at: {
#         $gte: new Date("2024-01-01"),
#         $lt: new Date("2024-02-01")
#     }
# })
#
# // Câu hỏi 5: Cập nhật tên tệp với `file_id` là 4 thành "New Spreadsheet.xlsx".
# db.files.updateOne({ file_id: 4 }, { $set: { name: "New Spreadsheet.xlsx" } })
#
# // Câu hỏi 6: Xóa tất cả tệp có kích thước nhỏ hơn 1000KB.
# db.files.deleteMany({ size: { $lt: 1000 } })
# Đóng kết nối
client.close()
