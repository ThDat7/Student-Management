from app import app, db
from models import *

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
                     first_name="John", dob=datetime.now(), sex=True, email="john@example.com",
                     role=admin_role.name)
        user2 = User(username="ad", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Smith",
                     first_name="Alice", dob=datetime.now(), sex=False, email="alice@example.com",
                     role=admin_role.name)
        db.session.add_all([user1, user2])
        db.session.commit()
        #################### giao vien va nhan vien
        # Tạo giao vien va staff
        user3 = User(username="gv", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Giao",
                     first_name="Vien", dob=datetime.now(), sex=True,
                     email="giaovien@example.com", role=teacher_role.name)
        user4 = User(username="nv", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), last_name="Nhan",
                     first_name="Vien", dob=datetime.now(), sex=False,
                     email="nhanvien@example.com", role=staff_role.name)
        db.session.add_all([user3, user4])
        db.session.commit()

        # Tạo giáo viên và nhân viên
        teacher1 = Teacher(user=user3)
        db.session.add_all([teacher1])
        db.session.commit()

        #################### hoc sinh
        # Tạo học sinh
        student1 = Student(last_name="Hoc", first_name="Sinh", dob=datetime.now(), sex=True, address="", phone_number='0123')
        student2 = Student(last_name="Sinh", first_name="Vien", dob=datetime.now(), sex=False, address="", phone_number='0124')
        student3 = Student(last_name="Thanh", first_name="Dat", dob=datetime.now(), sex=True, address="", phone_number='0125')
        student4 = Student(last_name="Thanh", first_name="Hai", dob=datetime.now(), sex=True, address="", phone_number='0126')
        student5 = Student(last_name="Minh", first_name="Hoang", dob=datetime.now(), sex=True, address="", phone_number='0127')
        student6 = Student(last_name="ABC", first_name="XYZ", dob=datetime.now(), sex=True, address="", phone_number='0128')
        db.session.add_all([student1, student2, student3, student4, student5, student6])
        db.session.commit()

        #################### Tạo lớp học
        classroom1 = Classroom(grade=GradeEnum.TENTH, order=1, year=2023, homeroom_teacher=teacher1)
        db.session.add(classroom1)
        db.session.commit()

        # Thêm học sinh vào lớp học
        classroom1.students.append(student1)
        classroom1.students.append(student2)
        classroom1.students.append(student3)
        classroom1.students.append(student4)
        classroom1.students.append(student5)
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
        teach3 = Teach(teacher=teacher1, subject=subject1, classroom=classroom1, semester=SemesterEnum.II)
        teach2 = Teach(teacher=teacher1, subject=subject2, classroom=classroom2, semester=SemesterEnum.I)
        teach4 = Teach(teacher=teacher1, subject=subject2, classroom=classroom2, semester=SemesterEnum.II)
        teach5 = Teach(teacher=teacher1, subject=subject1, classroom=classroom2, semester=SemesterEnum.I)
        db.session.add_all([teach1, teach2, teach3, teach4, teach5])
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
