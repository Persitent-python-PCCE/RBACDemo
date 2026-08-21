from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from service.student_service import StudentService
from flask_jwt_extended import jwt_required, get_jwt
from dao.student_dao import StudentDAO
from utils.decorators import role_required


student_bp = Blueprint('student', __name__)
student_service = StudentService(StudentDAO())

def get_current_user_claims():
    try:
        return get_jwt()
    except Exception:
        return {}

@student_bp.route("/api/students", methods = ["GET"])
@role_required("ADMIN", "TEACHER", "STUDENT", "USER")
def get_students():
    studnets = student_service.get_all_students()
    return jsonify({
        "students":[s.to_dict() for s in studnets ]
    }), 200

@student_bp.route('/api/students', methods = ["POST"])
@role_required("ADMIN", "TEACHER")
def add_student():
    data = request.get_json()
    name = data.get('name')
    age = int(data.get('age'))
    email = data.get('email')
    course = data.get('course')

    student = student_service.add_student(name, email, age, course)
    return jsonify({
        "message": "Student created successfully",
        "student": student.to_dict()
    }), 201



@student_bp.route('/students', methods=['GET'])
@role_required("ADMIN", "TEACHER", "STUDENT", "USER")
def web_list_students():
    """
    Browser Template Route: List all students.
    Allowed Roles: ADMIN, TEACHER, STUDENT, USER
    Passes current_user claims to Jinja template for dynamic UI feature rendering.
    """
    students = student_service.get_all_students()
    claims = get_current_user_claims()
    return render_template('students/list.html', students=students, current_user=claims)


@student_bp.route('/students/add', methods=['GET', 'POST'])
@role_required("ADMIN", "TEACHER")
def web_add_student():
    """
    Browser Template Route: Add new student.
    Allowed Roles: ADMIN, TEACHER
    """
    claims = get_current_user_claims()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        try:
            age = int(request.form.get('age', 0))
            student_service.add_student(name, email, age, course)
            flash("Student added successfully!", "success")
            return redirect(url_for('student.web_list_students'))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('students/add.html', current_user=claims)

    return render_template('students/add.html', current_user=claims)


@student_bp.route('/students/edit/<int:s_id>', methods=['GET', 'POST'])
@role_required("ADMIN", "TEACHER")
def web_edit_student(s_id):
    """
    Browser Template Route: Edit student details.
    Allowed Roles: ADMIN, TEACHER
    """
    student = student_service.get_student_by_id(s_id)
    claims = get_current_user_claims()

    if not student:
        flash("Student not found", "danger")
        return redirect(url_for('student.web_list_students'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        try:
            age = int(request.form.get('age', 0))
            student_service.update_student(s_id, name=name, email=email, age=age, course=course)
            flash("Student updated successfully!", "success")
            return redirect(url_for('student.web_list_students'))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('students/edit.html', student=student, current_user=claims)

    return render_template('students/edit.html', student=student, current_user=claims)


@student_bp.route('/students/delete/<int:s_id>', methods=['POST'])
@role_required("ADMIN")
def web_delete_student(s_id):
    """
    Browser Template Route: Delete student.
    Allowed Roles: ADMIN
    """
    success = student_service.delete_student(s_id)
    if success:
        flash(f"Student #{s_id} deleted successfully!", "success")
    else:
        flash("Student not found or deletion failed", "danger")

    return redirect(url_for('student.web_list_students'))


