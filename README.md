# Student_Web
-Chỉnh sửa lại chọn ngày sinh ở quản lý học sinh


#Chỉnh lỗi group_by trong MySQL
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));


#CSS bg-images (tạm thời chưa bỏ vào admin/base.html)
body {
     background-image: url("{{ url_for('static', filename='assets/images/choosing-bg.jpg') }}")
}

table {
     color: #66ccff !important;
}


Mô hình dữ liệu lớp học như sau
- Trường học có 3 khối: 10, 11, 12

- Mỗi khối có 3 lớp, gồm:
    + Khối 10: 10a1, 10a2, 10a3
    + Khối 11: 11a1, 11a2, 11a3
    + Khối 12: 12a1, 12a2, 12a3

- Mỗi khối có 2 môn học, gồm:
    + Khối 10: Toán, Lịch sử
    + Khối 11: Toán, Lịch sử
    + Khối 12: Toán, Tiếng anh

- Gồm có 2 admin, 4 giáo viên, 1 nhân viên

- Mỗi lớp gồm 5 học sinh (tổng cộng 45 học sinh) và giáo viên chủ nhiệm mỗi lớp như sau:
    + Lớp 10a1, 10a2, 12a3: Giáo viên 1
    + Lớp 10a3, 11a1: Giáo viên 2
    + Lớp 11a2, 11a3: Giáo viên 3
    + Lớp 12a1, 12a2: Giáo viên 4

- Lịch giảng dạy của giáo viên như sau:
    + Giáo viên 1: dạy Toán Khối 11 và 12
    + Giáo viên 2: dạy Lịch sử Khối 10 và 11
    + Giáo viên 3: dạy Tiếng anh Khối 12
    + Giáo viên 4: dạy Toán khối 10