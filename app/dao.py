from flask_login import current_user

from app.models import *
from app import app
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)


def authenicate_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password.strip())).first()


def count_student_in_class():
    from sqlalchemy import func
    from sqlalchemy.orm import aliased

    student_alias = aliased(Student)

    query = (db.session.query(Classroom, func.count(student_alias.id).label('student_count'))
             .outerjoin(student_classroom, student_classroom.c.classroom_id == Classroom.id)
             .group_by(Classroom.id)
             )

    result = query.all()
    rs = []
    for cls, count in result:
        # Create a new Classroom instance
        classroom_instance = Classroom()

        # Update the attributes of the instance with the values from the dictionary
        classroom_instance.__dict__.update(cls.__dict__)

        # Add the student_count attribute
        setattr(classroom_instance, 'student_count', count)

        rs.append(classroom_instance)
    print(rs[0].__dict__)


def update_exams(id, exams):
    is_teach_belong_teacher = (db.session.query(Teach)
                               .join(Teacher)
                               .join(User)
                               .filter(Teacher.user_id.__eq__(current_user.id),
                                       Teach.id.__eq__(id))
                               .first()) is not None

    if not is_teach_belong_teacher:
        return

    for e_form in exams:
        e_db = (db.session.query(Exam)
                .filter(Exam.id.__eq__(e_form.id))
                .first())

        # for n_e_form in e_form.normal_exams:
        #     new_n_e = NormalExam(id=n_e_form.id, score=n_e_form.score)
        #     if new_n_e.id is None:
        #         e_db.normal_exams.append(new_n_e)
    db.session.commit()


def update_normal_exam(exam_id, id, score):
    normal_exam = (db.session.query(NormalExam)
                   .join(Exam)
                   .join(Teach)
                   .join(Teacher)
                   .join(User)
                   .filter(User.id.__eq__(current_user.id),
                           Exam.id.__eq__(exam_id),
                           NormalExam.id.__eq__(id))
                   .first())
    if normal_exam:
        normal_exam.score = score
        db.session.commit()
        return normal_exam

    return None
