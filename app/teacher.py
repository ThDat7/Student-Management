from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.model.fields import InlineFieldList
from flask_login import current_user
from sqlalchemy import func
from wtforms import Form, FormField, FloatField, SelectField, IntegerField, Field, StringField
from flask import request, jsonify

from app import admin, dao
from app.models import *


class AuthenticatedTeacherModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.TEACHER


class AuthenticatedTeacherBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.TEACHER


class TeachView(AuthenticatedTeacherModelView):
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
    column_filters = ('classroom', 'classroom.year')

    edit_modal_template = 'admin/model/modals/teach_edit.html'

    def get_one(self, id):
        return dao.get_teach_data(id)

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        count_query = self.get_count_query() if not self.simple_list_pager else None
        count = count_query.scalar() if count_query else None

        query = db.session.query(Teach).join(Teacher).filter(Teacher.user_id == current_user.id).all()
        return count, query


class AverageScoreStatsView(AuthenticatedTeacherBaseView):

    def __init__(self, session, name):
        self.session = session
        super(AverageScoreStatsView, self).__init__(name)

    def get_list(self):
        list_data = {
            'labels': ['Năm học', 'Lớp', 'Môn học'],
            'cols': ['year', 'class', 'subject'],
            'data': []
        }
        teach = ((db.session.query(
            Teach.id,
            Classroom.year,
            func.concat(Classroom.grade, 'A', Classroom.order),
            Subject.name
        )
                  .select_from(Teach)
                  .join(Classroom, Teach.classroom_id.__eq__(Classroom.id))
                  .join(Subject, Teach.subject_id.__eq__(Subject.id))
                  .join(Teacher, Teach.teacher_id.__eq__(Teacher.id))
                  .filter(Teacher.user_id.__eq__(current_user.id))
                  .group_by(Classroom.year, Classroom.grade, Classroom.order, Subject.name))
                 .all())
        data = [{'id': id, 'year': year, 'class': class_name, 'subject': subject}
                for id, year, class_name, subject in teach]

        list_data['data'] = data
        return list_data

    @expose('/')
    def index(self):
        data = self.get_list()
        return self.render('admin/model/stats.html', data=data, url_detail='/admin/averagescorestatsview/stats_detail')

    def get_detail(self, id):
        teach = (self.session.query(Teach)
                 .filter(Teach.id.__eq__(id))).first()

        data = {
            'details': [
                {
                    'label': 'Năm học',
                    'value': teach.classroom.year
                },
                {
                    'label': 'Lớp',
                    'value': teach.classroom
                },
                {
                    'label': 'Môn',
                    'value': teach.subject.name
                },
            ],
            'stat_labels': ['Họ và tên đệm', 'Tên', 'Điểm TB HK1', 'Điểm TB HK2'],
            'stat_cols': ['last_name', 'first_name', 'avg_I', 'avg_II'],
            'stat_data': []
        }

        query = (self.session.query(Exam)
                 .join(Teach)
                 .join(Student)
                 .filter(Teach.teacher_id.__eq__(teach.teacher_id),
                         Teach.subject_id.__eq__(teach.subject_id),
                         Teach.classroom_id.__eq__(teach.classroom_id)))
        stat_data = []
        for student in teach.classroom.students:
            stat = {'last_name': student.last_name, 'first_name': student.first_name,
                    'avg_I': self.avg_score(query.filter(Teach.semester == SemesterEnum.I), student),
                    'avg_II': self.avg_score(query.filter(Teach.semester == SemesterEnum.II), student)}
            stat_data.append(stat)
        data['stat_data'] = stat_data
        return data

    def avg_score(self, query, student):
        exams = query.filter(Exam.student_id.__eq__(student.id)).all()
        # if len(exams) == 0:
        #     raise Exception("Điểm vẫn chưa nhập đủ")
        avg_score = 0.0
        for exam in exams:
            factor = 0
            for normal_exam in exam.normal_exams:
                if normal_exam.factor == FactorEnum.I:
                    avg_score += normal_exam.score
                    factor += 1
                else:
                    avg_score += normal_exam.score * 2
                    factor += 2
            avg_score += exam.final_exam.score * 3
            avg_score /= (factor + 3)
        return avg_score

    @expose('/stats_detail/<id>')
    def stats_detail(self, id):
        data = self.get_detail(id)
        return self.render('admin/model/modals/stats_details.html', data=data)


admin.add_view(TeachView(Teach, db.session, name='Quản Lý Điểm'))
admin.add_view(AverageScoreStatsView(db.session, name='Thống kê điểm trung bình'))
