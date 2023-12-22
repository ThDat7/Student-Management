from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.model.fields import InlineFieldList
from flask_login import current_user
from wtforms import Form, FormField, FloatField, SelectField, IntegerField, Field, StringField
from flask import request

from app import admin
from app.models import *


class NormalExamForm(Form):
    id = IntegerField('id')
    exam = QuerySelectField()
    factor = SelectField(choices=[(FactorEnum.I, '15p'), (FactorEnum.II, '45p')])
    score = FloatField('score')


class FinalExamForm(Form):
    id = IntegerField('id')
    exam = QuerySelectField()
    score = FloatField('score')


class ExamForm(Form):
    id = IntegerField('id')
    normal_exams = QuerySelectMultipleField()
    final_exam = QuerySelectField()


class TeachForm(Form):
    exams = InlineFieldList(FormField(ExamForm))


class AuthenticatedTeacher(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.TEACHER


class TeachView(AuthenticatedTeacher):
    column_list = ['id', 'exams']

    edit_modal = True
    can_view_details = True
    details_modal = True

    details_modal_template = 'admin/model/modals/teach_details.html'
    edit_modal_template = 'admin/model/modals/teach_edit.html'

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):
        (form) = super(TeachView, self).edit_view()
        return super(TeachView, self).edit_view()


admin.add_view(TeachView(Teach, db.session, name='Quản Lý Điểm'))
