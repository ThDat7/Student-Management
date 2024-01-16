from flask_login import current_user
from sqlalchemy import func, case
import cloudinary.uploader
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
    validate_exams_number_rule(exam_id, factor)

    normal_exam = NormalExam(exam_id=exam_id, factor=factor, score=score)
    db.session.add(normal_exam)
    db.session.commit()

    return normal_exam


def validate_exams_number_rule(exam_id, factor):
    if exam_id is not None:
        exam = db.session.query(Exam).filter(Exam.id.__eq__(exam_id)).first()
        msg_error = None

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
    else:
        raise Exception("Cập nhật ảnh đại diện thất bại!!!Vui lòng cung cấp file ảnh")



def phone_student(kw):
    data = (db.session.query(Student, Classroom)
            .join(Student_ClassRoom, Student.id == Student_ClassRoom.student_id)
            .join(Classroom, Student_ClassRoom.classroom_id == Classroom.id)
            .filter(Student.phone_number.__eq__(kw))
            .first())

    if data is None:
        return data

    return {'id': data.Student.id,
            'fullname': f'{data.Student.last_name} {data.Student.first_name}',
            'dob': data.Student.dob,
            'sex': data.Student.sex,
            'classroom': data.Classroom.__str__()}


def score_student_one(kw):
    student = phone_student(kw)

    return (db.session.query(Exam.id.label('id_exam'), Subject.name.label('name_subject'),
                             func.group_concat(case((NormalExam.factor == FactorEnum.I, NormalExam.score), else_=None))
                             .label('s1'),
                             func.group_concat(case((NormalExam.factor == FactorEnum.II, NormalExam.score), else_=None))
                             .label('s2'),
                             FinalExam.score.label('final_score'))
            .join(Teach, Subject.id == Teach.subject_id, isouter=True)
            .join(Exam, Teach.id == Exam.teach_id, isouter=True)
            .join(FinalExam, Exam.id == FinalExam.exam_id, isouter=True)
            .join(NormalExam, Exam.id == NormalExam.exam_id, isouter=True)
            .filter(Exam.student_id == student['id'], Teach.semester == SemesterEnum.I)
            .group_by(Exam.id, Subject.name, FinalExam.score)
            .all())


def score_student_two(kw):
    student = phone_student(kw)

    return (db.session.query(Exam.id.label('id_exam'), Subject.name.label('name_subject'),
                             func.group_concat(case((NormalExam.factor == FactorEnum.I, NormalExam.score), else_=None))
                             .label('s1'),
                             func.group_concat(case((NormalExam.factor == FactorEnum.II, NormalExam.score), else_=None))
                             .label('s2'),
                             FinalExam.score.label('final_score'))
            .join(Teach, Subject.id == Teach.subject_id, isouter=True)
            .join(Exam, Teach.id == Exam.teach_id, isouter=True)
            .join(FinalExam, Exam.id == FinalExam.exam_id, isouter=True)
            .join(NormalExam, Exam.id == NormalExam.exam_id, isouter=True)
            .filter(Exam.student_id == student['id'], Teach.semester == SemesterEnum.II)
            .group_by(Exam.id, Subject.name, FinalExam.score)
            .all())
