from flask_login import current_user

from app.models import *
from app import app
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)


def authenticate_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password.strip())).first()


def create_exam(student_id, teach_id):
    exam = Exam(student_id=student_id, teach_id=teach_id)
    db.session.add(exam)
    db.session.commit()

    return exam


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


def create_normal_exam(exam_id, factor, score):
    normal_exam = NormalExam(exam_id=exam_id, factor=factor, score=score)
    db.session.add(normal_exam)
    db.session.commit()

    return normal_exam


def delete_normal_exam(id, exam_id):
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
        id = normal_exam.id
        db.session.delete(normal_exam)
        db.session.commit()
        return id

    return None


def update_final_exam(exam_id, score):
    exam = (db.session.query(Exam)
            .join(Teach)
            .join(Teacher)
            .join(User)
            .filter(User.id.__eq__(current_user.id),
                    Exam.id.__eq__(exam_id))
            .first())
    if exam:
        if exam.final_exam is None:
            exam.final_exam = FinalExam(exam_id=exam.id)

        exam.final_exam.score = score
        db.session.commit()
        return exam

    return None


def get_teach_data(teach_id):
    teach = ((db.session.query(Teach)
                  .filter(Teach.id.__eq__(teach_id)))
                 .first())

    classroom = teach.classroom

    students = classroom.students

    data = {
        'teach_id': teach_id,
        'year': classroom.year,
        'semester': teach.semester.value,
        'classroom': classroom.__str__(),
        'subject': teach.subject,
        'students': []
    }

    for student in students:
        student_data = {
            'id': student.id,
            'last_name': student.last_name,
            'first_name': student.first_name,
            'exam': None
        }

        exam = (db.session.query(Exam)
                .filter(Exam.student_id.__eq__(student.id),
                        Exam.teach_id.__eq__(teach_id))).first()

        exam_data = None
        if exam:
            exam_data = {
                'id': exam.id,
                'normal_exams': [],
                'final_exam': None
            }

            if exam.final_exam is not None:
                exam_data['final_exam'] = {
                    'score': exam.final_exam.score
                }

            for normal_exam in exam.normal_exams:
                normal_exam_data = {
                    'id': normal_exam.id,
                    'factor': normal_exam.factor,
                    'score': normal_exam.score
                }
                exam_data['normal_exams'].append(normal_exam_data)

        student_data['exam'] = exam_data
        data['students'].append(student_data)

    return data
