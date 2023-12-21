from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum
import hashlib


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TEACHER = "teacher"


class GradeEnum(enum.Enum):
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12

    def __str__(self):
        return self.value


class FactorEnum(enum.Enum):
    I = 1
    II = 2

    def __str__(self):
        return self.name


class SemesterEnum(enum.Enum):
    I = 1
    II = 2


class ConfigKeyEnum(enum.Enum):
    MAX_AGE = "max_age"
    MIN_AGE = "min_age"
    MAX_NUM = "max_num"


class Role(db.Model):
    __tablename__ = 'role'
    name = Column(Enum(RoleEnum), primary_key=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    last_name = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    dob = Column(DateTime, nullable=False)
    sex = Column(Boolean, nullable=False)
    address = Column(String(255))
    phone = Column(String(11))
    email = Column(String(100))

    role = Column(Enum(RoleEnum), ForeignKey('role.name'), nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    user = relationship('User')

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name


class Teach(db.Model):
    __tablename__ = 'teach'
    id = Column(Integer, primary_key=True, autoincrement=True)
    semester = Column(Enum(SemesterEnum), nullable=False)

    teacher_id = Column("teacher_id", Integer, ForeignKey("teacher.id"))
    subject_id = Column("subject_id", Integer, ForeignKey("subject.id"))
    classroom_id = Column("classroom_id", Integer, ForeignKey("classroom.id"))

    teacher = relationship('Teacher')
    subject = relationship('Subject')
    classroom = relationship('Classroom')


class Student(db.Model):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    dob = Column(DateTime, nullable=False)
    sex = Column(Boolean, nullable=False)
    address = Column(String(255))
    email = Column(String(255))

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Enum(GradeEnum), nullable=False)
    order = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    homeroom_teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable=False)
    homeroom_teacher = relationship('Teacher')

    students = relationship('Student', secondary="student_classroom", backref=db.backref('classroom'))
    student_count = None

    def __str__(self):
        return str(self.grade.value) + 'A' + str(self.order)


student_classroom = db.Table('student_classroom',
                             Column("student_id", Integer, ForeignKey("student.id"), primary_key=True),
                             Column("classroom_id", Integer, ForeignKey("classroom.id"), primary_key=True))


class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    grade = Column(Enum(GradeEnum), nullable=False)

    def __str__(self):
        return self.name


class Exam(db.Model):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    teach_id = Column(Integer, ForeignKey('teach.id'), nullable=False)

    student = relationship('Student')
    teach = relationship('Teach', backref='exams')

    final_exam = relationship('FinalExam', back_populates='exam', uselist=False)


class NormalExam(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    exam_id = Column(Integer, ForeignKey('exam.id'), nullable=False)
    exam = relationship('Exam', backref='normal_exams')

    factor = Column(Enum(FactorEnum), nullable=False)
    score = Column(Float, nullable=False)


class FinalExam(db.Model):
    exam_id = Column(Integer, ForeignKey('exam.id'), primary_key=True)
    exam = relationship('Exam', back_populates='final_exam')

    score = Column(Float, nullable=False)


class Config(db.Model):
    __tablename__ = 'config'
    key = Column(Enum(ConfigKeyEnum), primary_key=True)
    value = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # Xóa các bảng đã có sẵn
        db.drop_all()

        # Tạo các bảng
        db.create_all()

        # Tạo vai trò
        admin_role = Role(name=RoleEnum.ADMIN)
        staff_role = Role(name=RoleEnum.STAFF)
        teacher_role = Role(name=RoleEnum.TEACHER)
        db.session.add_all([admin_role, staff_role, teacher_role])
        db.session.commit()

        #################### admin
        # Tạo người dùng
        user1 = User(username="admin", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Doe",
                     first_name="John", dob=datetime.now(), sex=True, address="", phone="", email="john@example.com",
                     role=admin_role.name)
        user2 = User(username="ad", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Smith",
                     first_name="Alice", dob=datetime.now(), sex=False, address="", phone="", email="alice@example.com",
                     role=admin_role.name)
        db.session.add_all([user1, user2])
        db.session.commit()
        #################### giao vien va nhan vien
        # Tạo giao vien va staff
        user3 = User(username="gv", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Giao",
                     first_name="Vien", dob=datetime.now(), sex=True, address="", phone="",
                     email="giaovien@example.com", role=teacher_role.name)
        user4 = User(username="nv", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Nhan",
                     first_name="Vien", dob=datetime.now(), sex=False, address="", phone="",
                     email="nhanvien@example.com", role=staff_role.name)
        db.session.add_all([user3, user4])
        db.session.commit()

        # Tạo giáo viên và nhân viên
        teacher1 = Teacher(user=user3)
        db.session.add_all([teacher1])
        db.session.commit()

        #################### hoc sinh
        # Tạo học sinh
        student1 = Student(last_name="Hoc", first_name="Sinh", dob=datetime.now(), sex=True, address="")
        student2 = Student(last_name="Sinh", first_name="Vien", dob=datetime.now(), sex=False, address="")
        db.session.add_all([student1, student2])
        db.session.commit()

        #################### Tạo lớp học
        classroom1 = Classroom(grade=GradeEnum.TENTH, order=1, year=2023, homeroom_teacher=teacher1)
        db.session.add(classroom1)
        db.session.commit()

        # Thêm học sinh vào lớp học
        classroom1.students.append(student1)
        classroom1.students.append(student2)
        db.session.commit()

        classroom2 = Classroom(grade=GradeEnum.ELEVENTH, order=1, year=2023, homeroom_teacher=teacher1)
        db.session.add(classroom2)
        db.session.commit()

        # Thêm học sinh vào lớp học
        classroom2.students.append(student2)
        db.session.commit()

        # Tạo môn học
        subject1 = Subject(name="Math", grade=GradeEnum.TENTH)
        subject2 = Subject(name="History", grade=GradeEnum.ELEVENTH)
        db.session.add_all([subject1, subject2])
        db.session.commit()

        # Tạo giảng dạy
        teach1 = Teach(teacher=teacher1, subject=subject1, classroom=classroom1, semester=SemesterEnum.I)
        teach2 = Teach(teacher=teacher1, subject=subject2, classroom=classroom2, semester=SemesterEnum.I)
        db.session.add_all([teach1, teach2])
        db.session.commit()

        # Tạo kiem tra
        exam1 = Exam(student=student1, teach=teach1)
        exam2 = Exam(student=student2, teach=teach1)
        db.session.add_all([exam1, exam2])
        db.session.commit()

        # Tạo exam detail
        e1 = NormalExam(exam=exam1, factor=FactorEnum.I, score=7.1)
        e2 = NormalExam(exam=exam1, factor=FactorEnum.I, score=8)
        e3 = NormalExam(exam=exam1, factor=FactorEnum.I, score=7)
        e4 = NormalExam(exam=exam1, factor=FactorEnum.I, score=6)
        e5 = NormalExam(exam=exam1, factor=FactorEnum.II, score=5)
        fe = FinalExam(exam=exam1, score=8)

        e21 = NormalExam(exam=exam2, factor=FactorEnum.I, score=1)
        e22 = NormalExam(exam=exam2, factor=FactorEnum.I, score=2)
        e23 = NormalExam(exam=exam2, factor=FactorEnum.I, score=3)
        e24 = NormalExam(exam=exam2, factor=FactorEnum.I, score=4)
        e25 = NormalExam(exam=exam2, factor=FactorEnum.I, score=7)
        fe2 = FinalExam(exam=exam2, score=2)
        db.session.add_all([e1, e2, e3, e4, e5, fe])
        db.session.add_all([e21, e22, e23, e24, e25, fe2])
        db.session.commit()
