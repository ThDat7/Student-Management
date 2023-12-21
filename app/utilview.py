from flask_admin import BaseView, expose
from app import admin
from flask_login import current_user, logout_user
from flask import redirect


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(LogoutView(name="Đăng xuất"))
