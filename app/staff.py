import warnings

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from wtforms import ValidationError
from wtforms.fields.simple import HiddenField

from app import app, db, admin
from app.models import *
from flask_login import current_user, logout_user
from flask import redirect, request


class AuthenticatedStaff(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.STAFF


class ClassroomView(AuthenticatedStaff):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'grade', 'order', 'year', 'homeroom_teacher', 'student_count']
    column_labels = {
        'id': 'Mã số',
        'grade': 'Khối',
        'order': 'Thứ tự lớp',
        'year': 'Năm học',
        'homeroom_teacher': 'Chủ nhiệm',
        'student_count': 'Sỉ số'
    }
    details_modal_template = 'admin/model/modals/classroom_details.html'
    edit_modal_template = 'admin/model/modals/classroom_edit.html'

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        result = super(ClassroomView, self).get_list(page, sort_column, sort_desc, search, filters,
                                                     execute, page_size)
        from sqlalchemy import func
        n, cls = result
        for c in cls:
            number_student = (self.session.query(func.count(student_classroom.c.student_id))
                              .filter(student_classroom.c.classroom_id == c.id)).scalar()
            c.student_count = number_student
        return result


class StudentView(AuthenticatedStaff):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ['id', 'last_name', 'first_name', 'dob', 'sex', 'address', 'email', 'classroom']
    column_labels = {
        'id': 'STT',
        'last_name': 'Họ',
        'first_name': 'Tên',
        'dob': 'Ngày sinh',
        'sex': 'Giới tính',
        'address': 'Địa chỉ',
        'classroom': 'Lớp học'
    }

    form_excluded_columns = ('classroom')

    def on_model_change(self, form, model, is_created):
        msg = None

        age = datetime.now().year - form.data['dob'].year

        from sqlalchemy import or_
        config_age = self.session.query(Config).filter(or_(Config.key==ConfigKeyEnum.MAX_AGE, Config.key==ConfigKeyEnum.MIN_AGE)).all()
        for int_config in config_age:
            if int_config.key == ConfigKeyEnum.MIN_AGE and age < int_config.value:
                msg = 'Tuổi nhỏ hơn quy định'
            elif int_config.key == ConfigKeyEnum.MAX_AGE and age > int_config.value:
                msg = 'Tuổi lớn hơn quy định'
        if msg is not None:
            raise ValidationError(msg)


admin.add_view(ClassroomView(Classroom, db.session, name='Quản Lý Lớp Học'))
admin.add_view(StudentView(Student, db.session, name='Quản Lý Học Sinh'))
