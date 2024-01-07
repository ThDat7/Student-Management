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
    address = Column(String(255), default="text")
    phone = Column(String(11), default="text")
    email = Column(String(100), default="text")
    avatar = Column(String(255),
                    default='https://res.cloudinary.com/dh5jcbzly/image/upload/v1703666812/hme7xdtwowv4rloj1dzq.jpg')
    joined_date = Column(DateTime, default=datetime.now())

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

    student_classroom = db.Table('student_classroom',
                             Column("student_id", Integer, ForeignKey("student.id"), primary_key=True),
                             Column("classroom_id", Integer, ForeignKey("classroom.id"), primary_key=True))

    def __str__(self):
        return str(self.grade.value) + 'A' + str(self.order)


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
