from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lí sinh viên")
root.geometry("600x800")

# #Kết nối tới db
# conn = sqlite3.connect('Sinh_vien.db')
# c = conn.cursor()
#
# # Tao bang de luu tru
# c.execute('''
#     CREATE TABLE Sinh_vien(
#         msv  INTEGER PRIMARY KEY,
#         first_name text,
#         last_name text,
#         Class text,
#         yearcommed interger,
#         avagre_point interger
#     )
# '''
# )

def them():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('Sinh_vien.db')
    c = conn.cursor()
    # Lấy dữ liệu đã nhập
    msv_value = msv.get()
    fristname_value = f_name.get()
    lastname_value = l_name.get()
    class_value = Class.get()
    yearcommed_value = yearcommed.get()
    avagrepoint_value = avagre_point.get()
    # Thực hiện câu lệnh để thêm
    c.execute('''
         INSERT INTO 
         Sinh_vien( msv, last_name, first_name, Class, yearcommed, avagre_point)
         VALUES 
         (:msv, :first_name, :lass_name,:Class, :yearcommed, :avagre_point)
     ''', {
        'msv': msv_value,
        'first_name': fristname_value,
        'lass_name': lastname_value,
        'Class': class_value,
        'yearcommed': yearcommed_value,
        'avagre_point': avagrepoint_value,
    }
              )
    conn.commit()
    conn.close()
    # Reset form
    msv.delete(0,END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    Class.delete(0, END)
    yearcommed.delete(0, END)
    avagre_point.delete(0, END)


def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('Sinh_vien.db')
    c = conn.cursor()
    # Lấy ID từ ô nhập liệu
    id_value = delete_box.get()
    # Kiểm tra xem ID có tồn tại hay không
    c.execute("SELECT * FROM Sinh_vien WHERE msv=:msv", {'msv': id_value})
    record = c.fetchone()

    if record is None:
        # Nếu không tìm thấy bản ghi nào với ID đó, hiện thông báo lỗi
        messagebox.showerror("Lỗi", " Mã sinh viên không tồn tại!")
    else:
        # Nếu tìm thấy bản ghi, tiến hành xóa
        c.execute('''DELETE FROM
                                Sinh_vien 
                              WHERE msv=:msv''',
                  {'msv': id_value})
        # Hiên thi thong bao
        messagebox.showinfo("Thông báo", "Đã xóa!")
    delete_box.delete(0, END)
    conn.commit()

    conn.close()

    # Hiển thị lại dữ liệu
    truy_van()
# hàm hiền thị trên treeview
def truy_van():
    # Xóa đi các dữ liệu trong TreeVIew
    for row in tree.get_children():
        tree.delete(row)
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('Sinh_vien.db')
    c = conn.cursor()
    c.execute("SELECT * FROM  Sinh_vien")
    records = c.fetchall()
    for r in records:
        tree.insert("",END, values=(r[0],r[1],r[2],r[3],r[4],r[5]))
    # ngắt kết nối
    conn.close()
# hàm chỉnh sửa
def chinh_sua():
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('Sinh_vien.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM Sinh_vien WHERE msv=:msv", {'msv': record_id})
    records = c.fetchall()

    global f_msv_editor, f_name_editor, l_name_editor, Class_editor, yearcommed_editor,avagre_point_editor

    f_msv_editor = Entry(editor, width=30)
    f_msv_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    Class_editor = Entry(editor, width=30)
    Class_editor.grid(row=3, column=1)
    yearcommed_editor = Entry(editor, width=30)
    yearcommed_editor.grid(row=4, column=1)
    avagre_point_editor = Entry(editor, width=30)
    avagre_point_editor.grid(row=5, column=1)


    f_msv_label = Label(editor, text="MSV")
    f_msv_label.grid(row=0, column=0, pady=(10, 0))
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=1, column=0)
    l_name_label = Label(editor, text="Tên")
    l_name_label.grid(row=2, column=0)
    Class_label = Label(editor, text=" Mã lớp")
    Class_label.grid(row=3, column=0)
    yearcommed_label = Label(editor, text="Năm nhập học")
    yearcommed_label.grid(row=4, column=0)
    avagre_point_label = Label(editor, text="Điểm trung bình")
    avagre_point_label.grid(row=5, column=0)
    for record in records:
        f_msv_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        Class_editor.insert(0, record[3])
        yearcommed_editor.insert(0, record[4])
        avagre_point_editor.insert(0, record[5])


    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)
# hàm cập nhật
def cap_nhat():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('Sinh_vien.db')
    c = conn.cursor()
    record_id = f_msv_editor.get()

    c.execute("""UPDATE Sinh_vien SET
           msv = :msv,
           first_name = :first_name, 
           last_name =  :last_name,
           Class = :Class,
           yearcommed =  :yearcommed,
           avagre_point = :avagre_point
           WHERE msv=:msv""",
              {
                  'first_name': f_name_editor.get(),
                  'last_name': l_name_editor.get(),
                  'Class': Class_editor.get(),
                  'yearcommed':yearcommed_editor.get(),
                  'avagre_point': avagre_point_editor.get(),
                  'msv': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()
def on_tree_select(event):
    # Lấy item được chọn trong Treeview
    selected_item = tree.selection()
    if selected_item:
        # Lấy giá trị của ID từ item được chọn
        item = tree.item(selected_item)
        id_value = item['values'][0]  # Giả sử cột đầu tiên chứa ID
        delete_box.delete(0, END)     # Xóa nội dung ô nhập liệu hiện tại
        delete_box.insert(0, id_value) # Chèn ID vào ô nhập liệu
# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho cửa sổ chính
msv = Entry(input_frame, width=30)
msv.grid(row=0, column=1, padx=20, pady=(10, 0))
f_name = Entry(input_frame, width=30)
f_name.grid(row=1, column=1)
l_name = Entry(input_frame, width=30)
l_name.grid(row=2, column=1)
Class = Entry(input_frame, width=30)
Class.grid(row=3, column=1)
yearcommed = Entry(input_frame, width=30)
yearcommed.grid(row=4, column=1)
avagre_point = Entry(input_frame, width=30)
avagre_point.grid(row=5, column=1)


# Các nhãn
msv_label = Label(input_frame, text="Mã Sinh Viên")
msv_label.grid(row=0, column=0, pady=(10, 0))
f_name_label = Label(input_frame, text="Họ")
f_name_label.grid(row=1, column=0)
l_name_label = Label(input_frame, text="Tên")
l_name_label.grid(row=2, column=0)
Class_label = Label(input_frame, text="Mã lớp")
Class_label.grid(row=3, column=0)
yearcommed_label = Label(input_frame, text="Năm nhập học")
yearcommed_label.grid(row=4, column=0)
avagre_point_label = Label(input_frame, text="Điểm Trung Bình")
avagre_point_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn ID để xóa")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("Mã sinh viên","Họ","Tên","Mã lớp","Năm nhập học","Điểm Trung Bình")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
# Thiết lập chiều rộng cho từng cột
tree.column("Mã sinh viên", width=100)
tree.column("Họ", width=85)
tree.column("Tên", width=85)
tree.column("Mã lớp", width=85)
tree.column("Năm nhập học", width=120)
tree.column("Điểm Trung Bình", width=120)
tree.pack()

# Định nghĩa tiêu đề cho các cột
for col in columns:
    tree.heading(col, text=col)
# Kết nối sự kiện nhấp chuột với hàm on_tree_select
tree.bind("<ButtonRelease-1>", on_tree_select)
# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()