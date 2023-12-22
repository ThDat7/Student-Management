from flask import render_template, request, redirect, jsonify
from flask_login import login_user
from app import login, dao
from app.models import *
import admin, staff, teacher, utilview


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/login', methods=['post'])
def admin_login():
    request.form.get('username')
    request.form.get('password')


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=['get', 'post'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.authenicate_user(username, password)
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route("/api/count-student-in-class", methods=['get'])
def count_student_in_class():
    pass


@app.route("/update", methods=['POST'])
def update():
    data = request.json

    id = data.get('id')
    exams = data.get('exams')

    dao.update_exams(id, exams)

    return redirect("/admin")


@app.route('/normal_exam/update/<id>', methods=['POST'])
def update_exam(id):
    data = request.json
    exam_id = data.get('exam_id')
    score = data.get('score')

    normal_exam = dao.update_normal_exam(exam_id=exam_id, id=id, score=score)
    return jsonify(normal_exam)


if __name__ == '__main__':
    import sys

    app.run(debug=not (hasattr(sys, 'gettrace') and sys.gettrace() is not None))
