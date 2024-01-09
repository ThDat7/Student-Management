from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from app import app, db, admin
from app.models import *
from flask_login import current_user
from teacher import AverageScoreStatsView



class AuthenticatedAdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN


class AuthenticatedAdminBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN


class StudyStatsView(AuthenticatedAdminBaseView):
    def __init__(self, session, name):
        self.session = session
        super(StudyStatsView, self).__init__(name)

    def get_list(self):
        list_data = {
            'labels': ['Năm học', 'Học kỳ', 'Môn học'],
            'cols': ['year', 'semester', 'subject'],
            'data': []
        }
        teach = ((db.session.query(
            Teach.id,
            Classroom.year,
            Teach.semester,
            Subject.name
        )
                  .select_from(Teach)
                  .join(Classroom, Teach.classroom_id.__eq__(Classroom.id))
                  .join(Subject, Teach.subject_id.__eq__(Subject.id))
                  .group_by(Classroom.year, Subject.id, Teach.semester))
                 .all())
        data = [{'id': id, 'year': year, 'semester': teach_semester, 'subject': subject}
                for id, year, teach_semester, subject in teach]

        list_data['data'] = data
        return list_data

    @expose('/')
    def index(self):
        data = self.get_list()
        return self.render('admin/model/stats.html', data=data, url_detail='/admin/averagescorestatsview/stats_detail')

    def get_detail(self, id):
        teach = (db.session.query(Teach)
                 .filter(Teach.id.__eq__(id))).first()
        classrooms = (db.session.query(Classroom)
                      .join(Teach)
                      .join(Subject)
                      .filter(Classroom.year.__eq__(teach.classroom.year),
                              Subject.id.__eq__(teach.subject.id),
                              Teach.semester == teach.semester)
                      .group_by(Classroom.grade, Classroom.order)).all()

        data = {
            'details': [
                {
                    'label': 'Năm học',
                    'value': teach.classroom.year
                },
                {
                    'label': 'Học kỳ',
                    'value': teach.semester
                },
                {
                    'label': 'Môn',
                    'value': teach.subject.name
                },
            ],
            'stat_labels': ['Lớp', 'Sĩ số', 'Số lượng đạt', 'Tỉ lệ'],
            'stat_cols': ['classroom', 'student_count', 'pass_num', 'pass_rate'],
            'stat_data': []
        }
        query = (self.session.query(Exam)
                 .join(Teach)
                 .join(Classroom)
                 .join(Subject)
                 .filter(Classroom.year.__eq__(teach.classroom.year),
                         Subject.id.__eq__(teach.subject.id),
                         Teach.semester == teach.semester))
        for classroom in classrooms:
            stat = {
                'classroom': classroom.__str__(),
                'student_count': len(classroom.students),
                'pass_num': None,
                'pass_rate': None
            }
            pass_num = 0
            for student in classroom.students:
                avg_score = AverageScoreStatsView(db.session, name='').avg_score(query, student)
                if avg_score >= 5.0:
                    pass_num += 1

            pass_rate = pass_num / stat['student_count']
            stat['pass_num'] = pass_num
            stat['pass_rate'] = pass_rate
            data['stat_data'].append(stat)

        return data

    @expose('/stats_detail/<id>')
    def stats_detail(self, id):
        data = self.get_detail(id)
        return self.render('admin/model/modals/stats_details.html', data=data)


class SubjectView(AuthenticatedAdminModelView):
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


class UserView(AuthenticatedAdminModelView):
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


class ConfigView(AuthenticatedAdminModelView):
    column_display_pk = True
    edit_modal = True
    can_create = False
    can_delete = False

    column_list = ['key', 'value']
    column_labels = {
        'Key': 'Quy định',
        'value': 'Giá trị',
    }

    def get_pk_value(self, model):
        return model.key.name


admin.add_view(StudyStatsView(db.session, name='Thống kê kết quả học tập'))
admin.add_view(SubjectView(Subject, db.session, name='Quản Lý Môn Học'))
admin.add_view(UserView(User, db.session, name='Quản Lý Người Dùng'))
admin.add_view(ConfigView(Config, db.session, name='Quy định'))
