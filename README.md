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