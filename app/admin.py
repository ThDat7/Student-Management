from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from app import app, db, admin
from app.models import *
from flask_login import current_user


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN


class StatsView(AuthenticatedAdmin):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class SubjectView(AuthenticatedAdmin):

    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name']
    column_labels = {
        'id': 'STT',
        'name': 'Tên Môn Học',
    }


class UserView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'name', 'dob', 'address', 'sex', 'phone', 'email', 'username', 'password', 'avatar',
                   'user_role', 'role']
    column_labels = {
        'id': 'STT',
        'name': 'Họ Và Tên',
        'dob': 'Ngày Sinh',
        'address': 'Địa Chỉ',
        'sex': 'Giới Tính',
        'phone': 'Số Điện Thoại',
        'email': 'Email',
        'username': 'Tên Tài Khoản',
        'password': 'Mật Khẩu',
        'avatar': 'Ảnh Đại Diện',
        'user_role': 'Vai Trò',
        'role': 'Chức Vụ'
    }


admin.add_view(StatsView(name="Thống Kê Kết Quả Học Tập"))
admin.add_view(SubjectView(Subject, db.session, name='Quản Lý Môn Học'))
admin.add_view(UserView(User, db.session, name='Quản Lý Người Dùng'))
