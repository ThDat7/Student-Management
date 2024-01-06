from flask_admin import BaseView, expose
from app import admin
from flask_login import current_user, logout_user
from flask import redirect


class HomePageView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

admin.add_view(HomePageView(name='Home Page'))