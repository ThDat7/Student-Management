from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.model.fields import InlineFieldList
from flask_login import current_user
from wtforms import Form, FormField, FloatField, SelectField, IntegerField, Field, StringField
from flask import request

from app import admin, dao
from app.models import *


class AuthenticatedTeacher(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.TEACHER


class TeachView(AuthenticatedTeacher):
    column_list = ['classroom.year', 'semester', 'classroom', 'subject.name']
    column_labels = {
        'classroom.year': 'Năm học',
        'semester': 'Học kỳ',
        'classroom': 'Lớp học',
        'subject.name': 'Môn học'
    }

    edit_modal = True
    can_delete = False
    can_create = False

    edit_modal_template = 'admin/model/modals/teach_edit.html'

    def get_one(self, id):
        return dao.get_teach_data(id)


admin.add_view(TeachView(Teach, db.session, name='Quản Lý Điểm'))
