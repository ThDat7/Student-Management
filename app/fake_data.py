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
        admin1 = User(username="admin1", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                      last_name="Trịnh Thanh",
                      first_name="Hải", dob='2003-05-05 00:00:00', sex=SexEnum.Nam.name, email="hai@example.com",
                      role=admin_role.name)
        admin2 = User(username="admin2", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                      last_name="Nguyễn Thành",
                      first_name="Đạt", dob='2003-05-06 00:00:00', sex=SexEnum.Nam.name, email="dat@example.com",
                      role=admin_role.name)
        db.session.add_all([admin1, admin2])
        db.session.commit()

        #################### giao vien va nhan vien
        # Tạo user giáo viên va staff
        # Giáo viên 1 dạy toán khối 11 và 12
        giao_vien_1 = User(username="gv1", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                           last_name="Nguyễn",
                           first_name="B", dob='1995-12-02 00:00:00', sex=SexEnum.Nữ.name,
                           email="giaovien1@example.com", role=teacher_role.name)
        # Giáo viên 2 dạy lịch sử khối 10 và 11
        giao_vien_2 = User(username="gv2", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                           last_name="Đào",
                           first_name="Q", dob='1990-11-30 00:00:00', sex=SexEnum.Nam.name,
                           email="giaovien2@example.com", role=teacher_role.name)
        # Giáo viên 3 dạy tiếng anh khối 12
        giao_vien_3 = User(username="gv3", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                           last_name="Lê",
                           first_name="H", dob='1997-10-03 00:00:00', sex=SexEnum.Nữ.name,
                           email="giaovien3@example.com", role=teacher_role.name)
        # Giáo viên 4 dạy toán khối 10
        giao_vien_4 = User(username="gv4", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                           last_name="Phan",
                           first_name="M", dob='1997-11-03 00:00:00', sex=SexEnum.Nam.name,
                           email="giaovien4@example.com", role=teacher_role.name)

        nhan_vien1 = User(username="nv1", password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                          last_name="Lê Trương Minh",
                          first_name="Hoàng", dob='2003-11-01 00:00:00', sex=SexEnum.Nam.name,
                          email="nhanvien@example.com", role=staff_role.name)
        db.session.add_all([giao_vien_1, giao_vien_2, giao_vien_3, giao_vien_4, nhan_vien1])
        db.session.commit()

        # Tạo giáo viên
        teacher_1 = Teacher(user=giao_vien_1)
        teacher_2 = Teacher(user=giao_vien_2)
        teacher_3 = Teacher(user=giao_vien_3)
        teacher_4 = Teacher(user=giao_vien_4)
        db.session.add_all([teacher_1, teacher_2, teacher_3, teacher_4])
        db.session.commit()

        #################### hoc sinh
        # Mỗi lớp 5 học sinh, mỗi khối 3 lớp, có 3 khối
        # Tạo học sinh

        # Khối 10
        # Học sinh lớp 10A1
        student_1_10a1 = Student(last_name="Nguyễn Văn", first_name="A", dob='2003-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0121')
        student_2_10a1 = Student(last_name="Nguyễn Văn", first_name="B", dob='2003-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0122')
        student_3_10a1 = Student(last_name="Trần Thị", first_name="C", dob='2003-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0123')
        student_4_10a1 = Student(last_name="Lê Thị", first_name="D", dob='2003-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0124')
        student_5_10a1 = Student(last_name="Lê Trí", first_name="E", dob='2003-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0125')
        # Học sinh lớp 10A2
        student_1_10a2 = Student(last_name="Huỳnh Tấn", first_name="P", dob='2003-06-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0126')
        student_2_10a2 = Student(last_name="Trần Minh", first_name="L", dob='2003-07-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0127')
        student_3_10a2 = Student(last_name="Trần", first_name="M", dob='2003-08-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0128')
        student_4_10a2 = Student(last_name="Lê Thị", first_name="N", dob='2003-09-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0129')
        student_5_10a2 = Student(last_name="Lê Trí", first_name="O", dob='2003-10-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0120')
        # Học sinh lớp 10A3
        student_1_10a3 = Student(last_name="Huỳnh Tấn", first_name="Q", dob='2003-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0111')
        student_2_10a3 = Student(last_name="Trần Minh", first_name="S", dob='2003-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0222')
        student_3_10a3 = Student(last_name="Trần", first_name="T", dob='2003-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0333')
        student_4_10a3 = Student(last_name="Lê Thị", first_name="Y", dob='2003-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='0444')
        student_5_10a3 = Student(last_name="Lê Trí", first_name="A", dob='2003-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='0555')

        # Khối 11
        # Học sinh lớp 11A1
        student_1_11a1 = Student(last_name="Nguyễn Văn", first_name="A", dob='2002-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='5555')
        student_2_11a1 = Student(last_name="Nguyễn Văn", first_name="B", dob='2002-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='6666')
        student_3_11a1 = Student(last_name="Trần Thị", first_name="C", dob='2002-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='7777')
        student_4_11a1 = Student(last_name="Lê Thị", first_name="D", dob='2002-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='8888')
        student_5_11a1 = Student(last_name="Lê Trí", first_name="E", dob='2002-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9999')
        # Học sinh lớp 11A2
        student_1_11a2 = Student(last_name="Huỳnh Tấn", first_name="P", dob='2002-06-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1000')
        student_2_11a2 = Student(last_name="Trần Minh", first_name="L", dob='2002-07-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1001')
        student_3_11a2 = Student(last_name="Trần", first_name="M", dob='2002-08-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='1002')
        student_4_11a2 = Student(last_name="Lê Thị", first_name="N", dob='2002-09-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='1003')
        student_5_11a2 = Student(last_name="Lê Trí", first_name="O", dob='2002-10-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1004')
        # Học sinh lớp 11A3
        student_1_11a3 = Student(last_name="Huỳnh Tấn", first_name="Q", dob='2002-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1005')
        student_2_11a3 = Student(last_name="Trần Minh", first_name="S", dob='2002-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1006')
        student_3_11a3 = Student(last_name="Trần", first_name="T", dob='2002-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='1007')
        student_4_11a3 = Student(last_name="Lê Thị", first_name="Y", dob='2002-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='1008')
        student_5_11a3 = Student(last_name="Lê Trí", first_name="A", dob='2002-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='1009')

        # Khối 12
        # Học sinh lớp 12A1
        student_1_12a1 = Student(last_name="Nguyễn Văn", first_name="A", dob='2001-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9000')
        student_2_12a1 = Student(last_name="Nguyễn Văn", first_name="B", dob='2001-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9001')
        student_3_12a1 = Student(last_name="Trần Thị", first_name="C", dob='2001-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9002')
        student_4_12a1 = Student(last_name="Lê Thị", first_name="D", dob='2001-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9003')
        student_5_12a1 = Student(last_name="Lê Trí", first_name="E", dob='2001-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9004')
        # Học sinh lớp 12A2
        student_1_12a2 = Student(last_name="Huỳnh Tấn", first_name="P", dob='2001-06-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9005')
        student_2_12a2 = Student(last_name="Trần Minh", first_name="L", dob='2001-07-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9006')
        student_3_12a2 = Student(last_name="Trần", first_name="M", dob='2001-08-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9007')
        student_4_12a2 = Student(last_name="Lê Thị", first_name="N", dob='2001-09-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9008')
        student_5_12a2 = Student(last_name="Lê Trí", first_name="O", dob='2001-10-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9009')
        # Học sinh lớp 12A3
        student_1_12a3 = Student(last_name="Huỳnh Tấn", first_name="Q", dob='2001-01-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9010')
        student_2_12a3 = Student(last_name="Trần Minh", first_name="S", dob='2001-02-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9011')
        student_3_12a3 = Student(last_name="Trần", first_name="T", dob='2001-03-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9012')
        student_4_12a3 = Student(last_name="Lê Thị", first_name="Y", dob='2001-04-01 00:00:00', sex=SexEnum.Nữ.name,
                                 address="Text",
                                 phone_number='9013')
        student_5_12a3 = Student(last_name="Lê Trí", first_name="A", dob='2001-05-01 00:00:00', sex=SexEnum.Nam.name,
                                 address="Text",
                                 phone_number='9014')

        db.session.add_all([student_1_10a1, student_2_10a1, student_3_10a1, student_4_10a1, student_5_10a1,
                            student_1_10a2, student_2_10a2, student_3_10a2, student_4_10a2, student_5_10a2,
                            student_1_10a3, student_2_10a3, student_3_10a3, student_4_10a3, student_5_10a3,
                            student_1_11a1, student_2_11a1, student_3_11a1, student_4_11a1, student_5_11a1,
                            student_1_11a2, student_2_11a2, student_3_11a2, student_4_11a2, student_5_11a2,
                            student_1_11a3, student_2_11a3, student_3_11a3, student_4_11a3, student_5_11a3,
                            student_1_12a1, student_2_12a1, student_3_12a1, student_4_12a1, student_5_12a1,
                            student_1_12a2, student_2_12a2, student_3_12a2, student_4_12a2, student_5_12a2,
                            student_1_12a3, student_2_12a3, student_3_12a3, student_4_12a3, student_5_12a3])
        db.session.commit()

        #################### Tạo lớp học
        # Khối 10
        # Lớp 10a1
        classroom_10a1 = Classroom(grade=GradeEnum.TENTH, order=1, year=2023, homeroom_teacher=teacher_1)
        db.session.add(classroom_10a1)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_10a1.students.append(student_1_10a1)
        classroom_10a1.students.append(student_2_10a1)
        classroom_10a1.students.append(student_3_10a1)
        classroom_10a1.students.append(student_4_10a1)
        classroom_10a1.students.append(student_5_10a1)
        db.session.commit()

        # Lớp 10a2
        classroom_10a2 = Classroom(grade=GradeEnum.TENTH, order=2, year=2023, homeroom_teacher=teacher_1)
        db.session.add(classroom_10a2)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_10a2.students.append(student_1_10a2)
        classroom_10a2.students.append(student_2_10a2)
        classroom_10a2.students.append(student_3_10a2)
        classroom_10a2.students.append(student_4_10a2)
        classroom_10a2.students.append(student_5_10a2)
        db.session.commit()

        # Lớp 10a3
        classroom_10a3 = Classroom(grade=GradeEnum.TENTH, order=3, year=2023, homeroom_teacher=teacher_2)
        db.session.add(classroom_10a3)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_10a3.students.append(student_1_10a3)
        classroom_10a3.students.append(student_2_10a3)
        classroom_10a3.students.append(student_3_10a3)
        classroom_10a3.students.append(student_4_10a3)
        classroom_10a3.students.append(student_5_10a3)
        db.session.commit()

        # Khối 11
        # Lớp 11a1
        classroom_11a1 = Classroom(grade=GradeEnum.ELEVENTH, order=1, year=2023, homeroom_teacher=teacher_2)
        db.session.add(classroom_11a1)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_11a1.students.append(student_1_11a1)
        classroom_11a1.students.append(student_2_11a1)
        classroom_11a1.students.append(student_3_11a1)
        classroom_11a1.students.append(student_4_11a1)
        classroom_11a1.students.append(student_5_11a1)
        db.session.commit()

        # Lớp 11a2
        classroom_11a2 = Classroom(grade=GradeEnum.ELEVENTH, order=2, year=2023, homeroom_teacher=teacher_3)
        db.session.add(classroom_11a2)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_11a2.students.append(student_1_11a2)
        classroom_11a2.students.append(student_2_11a2)
        classroom_11a2.students.append(student_3_11a2)
        classroom_11a2.students.append(student_4_11a2)
        classroom_11a2.students.append(student_5_11a2)
        db.session.commit()

        # Lớp 11a3
        classroom_11a3 = Classroom(grade=GradeEnum.ELEVENTH, order=3, year=2023, homeroom_teacher=teacher_3)
        db.session.add(classroom_11a3)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_11a3.students.append(student_1_11a3)
        classroom_11a3.students.append(student_2_11a3)
        classroom_11a3.students.append(student_3_11a3)
        classroom_11a3.students.append(student_4_11a3)
        classroom_11a3.students.append(student_5_11a3)
        db.session.commit()

        # Khối 12
        # Lớp 12a1
        classroom_12a1 = Classroom(grade=GradeEnum.TWELVETH, order=1, year=2023, homeroom_teacher=teacher_4)
        db.session.add(classroom_12a1)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_12a1.students.append(student_1_12a1)
        classroom_12a1.students.append(student_2_12a1)
        classroom_12a1.students.append(student_3_12a1)
        classroom_12a1.students.append(student_4_12a1)
        classroom_12a1.students.append(student_5_12a1)
        db.session.commit()

        # Lớp 12a2
        classroom_12a2 = Classroom(grade=GradeEnum.TWELVETH, order=2, year=2023, homeroom_teacher=teacher_4)
        db.session.add(classroom_12a2)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_12a2.students.append(student_1_12a2)
        classroom_12a2.students.append(student_2_12a2)
        classroom_12a2.students.append(student_3_12a2)
        classroom_12a2.students.append(student_4_12a2)
        classroom_12a2.students.append(student_5_12a2)
        db.session.commit()

        # Lớp 12a3
        classroom_12a3 = Classroom(grade=GradeEnum.TWELVETH, order=3, year=2023, homeroom_teacher=teacher_1)
        db.session.add(classroom_12a3)
        db.session.commit()
        # Thêm học sinh vào lớp học
        classroom_12a3.students.append(student_1_12a3)
        classroom_12a3.students.append(student_2_12a3)
        classroom_12a3.students.append(student_3_12a3)
        classroom_12a3.students.append(student_4_12a3)
        classroom_12a3.students.append(student_5_12a3)
        db.session.commit()

        # Tạo môn học
        # Khối 10
        subject_10_1 = Subject(name="Math", grade=GradeEnum.TENTH)
        subject_10_2 = Subject(name="History", grade=GradeEnum.TENTH)

        # Khối 11
        subject_11_1 = Subject(name="Math", grade=GradeEnum.ELEVENTH)
        subject_11_2 = Subject(name="History", grade=GradeEnum.ELEVENTH)

        # Khối 12
        subject_12_1 = Subject(name="Math", grade=GradeEnum.TWELVETH)
        subject_12_2 = Subject(name="English", grade=GradeEnum.TWELVETH)
        db.session.add_all([subject_10_1, subject_10_2, subject_11_1, subject_11_2, subject_12_1, subject_12_2])
        db.session.commit()

        # Tạo giảng dạy
        # Toán khổi 10 do gv4 giảng dạy
        teach_t_10a1_1 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a1,
                               semester=SemesterEnum.I)
        teach_t_10a1_2 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a1,
                               semester=SemesterEnum.II)
        teach_t_10a2_1 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a2,
                               semester=SemesterEnum.I)
        teach_t_10a2_2 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a2,
                               semester=SemesterEnum.II)
        teach_t_10a3_1 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a3,
                               semester=SemesterEnum.I)
        teach_t_10a3_2 = Teach(teacher=teacher_4, subject=subject_10_1, classroom=classroom_10a3,
                               semester=SemesterEnum.II)

        #Toán khối 11 và 12 do gv1 giảng dạy
        # Khối 11
        teach_t_11a1_1 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a1,
                               semester=SemesterEnum.I)
        teach_t_11a1_2 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a1,
                               semester=SemesterEnum.II)
        teach_t_11a2_1 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a2,
                               semester=SemesterEnum.I)
        teach_t_11a2_2 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a2,
                               semester=SemesterEnum.II)
        teach_t_11a3_1 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a3,
                               semester=SemesterEnum.I)
        teach_t_11a3_2 = Teach(teacher=teacher_1, subject=subject_11_1, classroom=classroom_11a3,
                               semester=SemesterEnum.II)
        # Khối 12
        teach_t_12a1_1 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a1,
                               semester=SemesterEnum.I)
        teach_t_12a1_2 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a1,
                               semester=SemesterEnum.II)
        teach_t_12a2_1 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a2,
                               semester=SemesterEnum.I)
        teach_t_12a2_2 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a2,
                               semester=SemesterEnum.II)
        teach_t_12a3_1 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a3,
                               semester=SemesterEnum.I)
        teach_t_12a3_2 = Teach(teacher=teacher_1, subject=subject_12_1, classroom=classroom_12a3,
                               semester=SemesterEnum.II)

        # Lịch sử khối 10 và 11 do gv2 giảng dạy
        # Khối 10
        teach_ls_10a1_1 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a1,
                               semester=SemesterEnum.I)
        teach_ls_10a1_2 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a1,
                               semester=SemesterEnum.II)
        teach_ls_10a2_1 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a2,
                               semester=SemesterEnum.I)
        teach_ls_10a2_2 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a2,
                               semester=SemesterEnum.II)
        teach_ls_10a3_1 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a3,
                               semester=SemesterEnum.I)
        teach_ls_10a3_2 = Teach(teacher=teacher_2, subject=subject_10_2, classroom=classroom_10a3,
                               semester=SemesterEnum.II)
        # Khối 11
        teach_ls_11a1_1 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a1,
                                semester=SemesterEnum.I)
        teach_ls_11a1_2 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a1,
                                semester=SemesterEnum.II)
        teach_ls_11a2_1 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a2,
                                semester=SemesterEnum.I)
        teach_ls_11a2_2 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a2,
                                semester=SemesterEnum.II)
        teach_ls_11a3_1 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a3,
                                semester=SemesterEnum.I)
        teach_ls_11a3_2 = Teach(teacher=teacher_2, subject=subject_11_2, classroom=classroom_11a3,
                                semester=SemesterEnum.II)

        # Tiếng anh khổi 12 do gv3 giảng dạy
        teach_ta_12a1_1 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a1,
                               semester=SemesterEnum.I)
        teach_ta_12a1_2 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a1,
                               semester=SemesterEnum.II)
        teach_ta_12a2_1 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a2,
                               semester=SemesterEnum.I)
        teach_ta_12a2_2 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a2,
                               semester=SemesterEnum.II)
        teach_ta_12a3_1 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a3,
                               semester=SemesterEnum.I)
        teach_ta_12a3_2 = Teach(teacher=teacher_3, subject=subject_12_2, classroom=classroom_12a3,
                               semester=SemesterEnum.II)

        db.session.add_all([
            teach_t_10a1_1, teach_t_10a1_2, teach_t_10a2_1, teach_t_10a2_2, teach_t_10a3_1, teach_t_10a3_2,
            teach_ls_10a1_1, teach_ls_10a1_2, teach_ls_10a2_1, teach_ls_10a2_2, teach_ls_10a3_1, teach_ls_10a3_2,
            teach_t_11a1_1, teach_t_11a1_2, teach_t_11a2_1, teach_t_11a2_2, teach_t_11a3_1, teach_t_11a3_2,
            teach_ls_11a1_1, teach_ls_11a1_2, teach_ls_11a2_1, teach_ls_11a2_2, teach_ls_11a3_1, teach_ls_11a3_2,
            teach_t_12a1_1, teach_t_12a1_2, teach_t_12a2_1, teach_t_12a2_2, teach_t_12a3_1, teach_t_12a3_2,
            teach_ta_12a1_1, teach_ta_12a1_2, teach_ta_12a2_1, teach_ta_12a2_2, teach_ta_12a3_1, teach_ta_12a3_2
        ])
        db.session.commit()

        # # Tạo kiem tra
        # exam1 = Exam(student=student1, teach=teach1)
        # exam2 = Exam(student=student2, teach=teach1)
        # db.session.add_all([exam1, exam2])
        # db.session.commit()
        #
        # # Tạo exam detail
        # e1 = NormalExam(exam=exam1, factor=FactorEnum.I, score=7.1)
        # e2 = NormalExam(exam=exam1, factor=FactorEnum.I, score=8)
        # e3 = NormalExam(exam=exam1, factor=FactorEnum.I, score=7)
        # e4 = NormalExam(exam=exam1, factor=FactorEnum.I, score=6)
        # e5 = NormalExam(exam=exam1, factor=FactorEnum.II, score=5)
        # fe = FinalExam(exam=exam1, score=8)
        #
        # e21 = NormalExam(exam=exam2, factor=FactorEnum.I, score=1)
        # e22 = NormalExam(exam=exam2, factor=FactorEnum.I, score=2)
        # e23 = NormalExam(exam=exam2, factor=FactorEnum.I, score=3)
        # e24 = NormalExam(exam=exam2, factor=FactorEnum.I, score=4)
        # e25 = NormalExam(exam=exam2, factor=FactorEnum.I, score=7)
        # fe2 = FinalExam(exam=exam2, score=2)
        # db.session.add_all([e1, e2, e3, e4, e5, fe])
        # db.session.add_all([e21, e22, e23, e24, e25, fe2])
        # db.session.commit()
