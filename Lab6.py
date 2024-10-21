from pymongo import MongoClient
from datetime import datetime

#conecct to mongodb
client = MongoClient('mongodb://Localhost:27017/')
client.drop_database('facebookData')
db =client['facebookData'] #chosse csdl tiktok
#creat collection
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]

#add data user
user_data = [
    {'user_id': 1, 'name': "Nguyen Van A", 'email': "a@gmail.com",'age': 25},
    {'user_id': 2, 'name': "Tran Thi B", 'email': "b@gmail.com", 'age': 30},
    {'user_id': 3, 'name': "Le Van C", 'email': "c@gmail.com", 'age': 22}
]
users_collection.insert_many(user_data)
#add data post
post_data = [
    { 'post_id': 1, 'user_id': 1, 'content': "Hôm nay thật đẹp trời!", 'created_at': datetime(2024,10, 1) },
    { 'post_id': 2, 'user_id': 2, 'content': "Mình vừa xem một bộ phim hay!", 'created_at': datetime(2024,10,2 ) },
    { 'post_id': 3, 'user_id': 1, 'content': "Chúc mọi người một ngày tốt lành!", 'created_at': datetime(2024,10,3) }
]
posts_collection.insert_many(post_data)
#add data comments
comment_data = [
    { 'comment_id': 1, 'post_id': 1, 'user_id': 2, 'content': "Thật tuyệt vời!", 'created_at': datetime(2024,10,1) },
    { 'comment_id': 2, 'post_id': 2, 'user_id': 3, 'content': "Mình cũng muốn xem bộ phim này!", 'created_at': datetime(2024,10,2) },
    { 'comment_id': 3, 'post_id': 3, 'user_id': 1, 'content': "Cảm ơn bạn!", 'created_at': datetime(2024,10,3) }
]
comments_collection.insert_many(comment_data)

#Truy Van
#nguoi dung
print("Tat ca nguoi dung:")
for user in  user_data:
    print(user)
#bai dang user_id = 1
print("\nTất cả bai dang của người dùng 'user1':")
user_post = posts_collection.find({'user_id': 1})
for posts in user_post:
    print(posts)

#do tuoi tren 25
print("\n Tat ca nguoi dung tren 25 tuoi")
user_over25 = users_collection.find({'age' :{"$gte" : 25}})
for peopleo25 in user_over25:
    print(peopleo25)
#all post in T10
#db.posts.find({ created_at: { $gte: new Date("2024-10-01"), $lt: new Date("2024-11-01") } })
print("\n Tat ca nguoi dung dang bai trong thang 10")
user_postt10 = posts_collection.find({ 'created_at': {'$gte': datetime(2024,10, 1), '$lt': datetime(2024,11, 1) }})
for user_postbai in user_postt10:
    print(user_postbai)
# // Bước 6: Cập Nhật và Xóa Dữ Liệu
# // Cập nhật nội dung bài đăng của người dùng với post_id = 1
# db.posts.updateOne({ post_id: 1 }, { $set: { content: "Hôm nay thời tiết thật đẹp!" } })
print("\n Cap nhat sau khi xoa bai dang ")
posts_collection.update_one({ 'post_id':1},{'$set': { 'content':"Hôm nay thời tiết thật đẹp!"} })
for post in posts_collection.find():
    print(post)


# // Xóa bình luận với comment_id = 2
# db.comments.deleteOne({ comment_id: 2 })
print('xoa binh luan ne')
comments_collection.delete_one({'comment_id':2})
for comment in comments_collection.find():
    print(comment)

# Đóng kết nối
client.close()