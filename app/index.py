from flask import render_template, request, redirect, jsonify, Response
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
    return dao.get_user_by_id(user_id)


@app.route("/login-admin", methods=['get', 'post'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.authenticate_user(username, password)
        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route('/api/exam', methods=['POST'])
def create_exam():
    data = request.json
    student_id = data.get('student_id')
    teach_id = data.get('teach_id')

    exam = dao.create_exam(student_id, teach_id)

    return jsonify({
        'id': exam.id,
        'student_id': exam.student_id
    })


@app.route('/api/normal_exam/<id>', methods=['PUT'])
def update_normal_exam(id):
    data = request.json
    exam_id = data.get('exam_id')
    score = data.get('score')

    normal_exam = dao.update_normal_exam(exam_id, id, score)
    return jsonify({
        'id': normal_exam.id,
        'score': normal_exam.score,
        'exam_id': normal_exam.exam_id,
    })


@app.route('/api/normal_exam', methods=['POST'])
def create_normal_exam():
    data = request.json
    exam_id = data.get('exam_id')
    factor = data.get('factor')
    score = data.get('score')

    try:
        normal_exam = dao.create_normal_exam(exam_id, factor, score)
        return jsonify({
            'id': normal_exam.id,
            'score': normal_exam.score,
            'exam_id': normal_exam.exam_id,
        })
    except Exception as e:
        return Response("{'msg': e}", status=400)


@app.route('/api/normal_exam/<id>', methods=['DELETE'])
def delete_normal_exam(id):
    data = request.json
    exam_id = data.get('exam_id')

    id = dao.delete_normal_exam(id, exam_id)
    return jsonify({'id': id})


@app.route('/api/final_exam/<id>', methods=['POST'])
def update_final_exam(id):
    data = request.json
    score = data.get('score')

    exam = dao.update_final_exam(exam_id=id, score=score)
    return jsonify({
        'score': exam.final_exam.score,
        'exam_id': exam.id,
    })


@app.route('/api/search_student', methods=['GET'])
def search_student():
    student_name = request.args.get('student_name').strip()
    exclude_ids = request.args.getlist('exclude_ids[]')

    students = dao.search_students_by_name(student_name, exclude_ids)
    return jsonify({
        'students': students
    })


@app.route('/api/student/<id>', methods=['GET'])
def get_student(id):
    student = dao.get_student(id)
    return jsonify({
        'student': student
    })


def init_config_defaults():
    default_configs = [
        (ConfigKeyEnum.MIN_AGE, 17),
        (ConfigKeyEnum.MAX_AGE, 20),
        (ConfigKeyEnum.MAX_NUM, 40),
    ]

    for key, value in default_configs:
        config_entry = db.session.query(Config).filter_by(key=key).first()
        if config_entry is None:
            config_entry = Config(key=key, value=value)
            db.session.add(config_entry)
            db.session.commit()


if __name__ == '__main__':
    import sys

    with app.app_context():
        init_config_defaults()

    app.run(debug=not (hasattr(sys, 'gettrace') and sys.gettrace() is not None))
    # app.run()
