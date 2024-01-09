from flask_login import current_user
from sqlalchemy import func
import cloudinary.uploader
from wtforms import ValidationError

from app.models import *
from app import app
import hashlib


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


def authenticate_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return db.session.query(User).filter(User.username.__eq__(username.strip()),
                                         User.password.__eq__(password.strip())).first()


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
    validate_exams_number_rule(exam_id, factor, score)

    normal_exam = NormalExam(exam_id=exam_id, factor=factor, score=score)
    db.session.add(normal_exam)
    db.session.commit()

    return normal_exam


def validate_exams_number_rule(exam_id, factor):
    msg_error = None
    if exam_id is not None:
        exam = db.session.query(Exam).filter(Exam.id.__eq__(exam_id)).first()
        len15p, len45p = 0, 0
        if exam.normal_exams is not None:
            for normal_exam in exam.normal_exams:
                if normal_exam.factor == FactorEnum.I:
                    len15p += 1
                else:
                    len45p += 1

            if factor == 'I' and len15p >= 5:
                msg_error = 'Số cột điểm 15p đang lớn hơn quy định!!!'
            elif factor == 'II' and len45p >= 3:
                msg_error = 'Số cột điểm 45p đang lớn hơn quy định!!!'

            if msg_error is not None:
                raise Exception(msg_error)


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


def get_score_average_stats(teach_id):
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


def search_students_by_name(student_name, exclude_ids):
    students = (db.session.query(func.concat(Student.last_name, ' ', Student.first_name), Student.id)
                .filter(
        func.concat(Student.last_name, ' ', Student.first_name).ilike(f"%{student_name}%"),
        ~Student.id.in_(exclude_ids))
                .order_by(Student.first_name)).all()

    return [{'full_name': full_name, 'id': id} for (full_name, id) in students]


def get_student(id):
    student = (db.session.query(Student)
               .filter(Student.id == id)).first()

    return {'last_name': student.last_name,
            'first_name': student.first_name,
            'sex': student.sex,
            'dob': student.dob,
            'address': student.address
            }


def upload_image(avatar, id):
    user = db.session.query(User).filter(User.id.__eq__(id)).first()
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        user.avatar = res['secure_url']

    db.session.add(user)
    db.session.commit()


def stats():
    from sqlalchemy import func

    result = (db.session.query(
        Subject.name,
        Teach.semester,
        Classroom.year,
        Teach.classroom,
        func.count(Classroom.students)
        (func.sum(NormalExam.score) / func.count(NormalExam.id)).label('avg_normal_score'),
        (func.sum(FinalExam.score) / func.count(FinalExam.exam_id)).label('avg_final_score'))
              .join(Teach, Subject.id == Teach.subject_id)
              .join(Classroom, Teach.classroom_id == Classroom.id)
              .join(Exam, Teach.id == Exam.id)
              .join(FinalExam, Exam.id == FinalExam.exam_id)
              .join(NormalExam, Exam.id == NormalExam.exam_id)
              .group_by(Subject.name, Teach.semester, Classroom.year, Teach.classroom)
              .having(func.avg(NormalExam.score) >= 5.0, func.avg(FinalExam.score) >= 5.0)
              .all())
    return result
