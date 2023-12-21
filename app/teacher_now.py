# from flask_admin.contrib.sqla import ModelView
# from flask_admin import BaseView, expose
# from flask_admin.model import InlineFormAdmin
#
# from app import app, db, admin
# from app.models import *
# from flask_login import current_user, logout_user
# from flask import redirect
#
#
# class AuthenticatedTeacher(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.role == RoleEnum.TEACHER
#
#
# class TeachView(AuthenticatedTeacher):
#     column_display_pk = True
#     can_view_details = True
#     can_export = True
#     can_create = False
#     edit_modal = True
#     details_modal = True
#     create_modal = True
#
#     column_list = ['classroom.year', 'classroom', 'subject', 'semester']
#     column_details_list = ['classroom', 'subject', 'semester', 'classroom.year']
#
#     # form_widget_args = {
#     #     'teacher': {
#     #         'disabled': True,
#     #         'hidden': True
#     #     },
#     #     'classroom': {
#     #         'disabled': True
#     #     },
#     #     'subject': {
#     #         'disabled': True
#     #     },
#     #     'semester': {
#     #         'disabled': True
#     #     }
#     # }
#
#     column_labels = {
#         'teach.classroom': 'Năm học',
#         'classroom': 'Lớp học',
#         'subject': 'Môn',
#         'semester': 'Học kỳ'
#     }
#
#     list_template = 'admin/model/teach_list.html'
#     details_modal_template = 'admin/model/modals/teach_details.html'
#     # edit_modal_template = 'admin/model/modals/teach_edit.html'
#
#     # def edit_view(self):
#
#
#     def get_list(self, page, sort_column, sort_desc, search, filters,
#                  execute=True, page_size=None):
#         result = super(TeachView, self).get_list(page, sort_column, sort_desc, search, filters,
#                                                 execute, page_size)
#         n, cls = result
#         cls = (self.session.query(Teach)
#                .join(Teacher)
#                .filter(Teacher.user_id.__eq__(current_user.id))
#                .group_by(Teach.id)).all()
#         return n, cls
#
#     def get_one(self, id):
#         teach = (self.session.query(Teach)
#          .join(Teacher)
#          .filter(Teacher.user_id.__eq__(current_user.id),
#                  Teach.id.__eq__(id))).first()
#         return teach
#
#     # @expose('/edit/', methods=['POST'])
#     # def edit_exams(self):
#     #     print(self.model)
#
#     def update_model(self, form, model):
#         pass
#
#
# admin.add_view(TeachView(Teach, db.session, name='Quản Lý Điểm'))
