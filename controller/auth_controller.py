from flask import Blueprint, request, jsonify, flash, redirect, render_template, url_for, make_response
from dao.user_dao import UserDAO
from flask_jwt_extended import create_access_token, unset_jwt_cookies, set_access_cookies
from models.user import User

auth_bp = Blueprint('auth', __name__)
user_dao = UserDAO()

ALLOWED_ROLES = ["ADMIN", "TEACHER", "STUDENT", "USER"]

@auth_bp.route('/api/register', methods = ['POST'])
def api_register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role").upper()

    user = User(username = username, role = role)
    user.set_password(password)
    user_dao.add_user(user)

    return jsonify({
        "message" : "User registered successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/api/login", methods = ["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = user_dao.get_by_username(username)

    if not user or not user.check_password(password):
        return jsonify({"message" : "Invalid username or password"}), 401

    #jwt -> 
    additional_claims = {
        "role" : user.role,
        "username" : user.username
    }

    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({
        "message": "Login successful",
        "access_token" : access_token,
        "user": user.to_dict()
    }), 200


@auth_bp.route('/register', methods=['GET', 'POST'])
def web_register():
    """Renders user registration HTML template for browser users."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'USER').upper()

        if not username or not password:
            flash("Username and password are required", "danger")
            return render_template('register.html', allowed_roles=ALLOWED_ROLES)

        if role not in ALLOWED_ROLES:
            flash(f"Invalid role selected", "danger")
            return render_template('register.html', allowed_roles=ALLOWED_ROLES)

        if user_dao.get_by_username(username):
            flash(f"Username '{username}' is already taken", "warning")
            return render_template('register.html', allowed_roles=ALLOWED_ROLES)

        user = User(username=username, role=role)
        user.set_password(password)
        user_dao.add_user(user)

        flash(f"Registration successful! Account created with role '{role}'. Please log in.", "success")
        return redirect(url_for('auth.web_login'))

    return render_template('register.html', allowed_roles=ALLOWED_ROLES)


@auth_bp.route('/login', methods=['GET', 'POST'])
def web_login():
    """Renders user login HTML template and sets JWT in browser cookie."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = user_dao.get_by_username(username)

        if not user or not user.check_password(password):
            flash("Invalid username or password", "danger")
            return render_template('login.html')

        additional_claims = {
            "role": user.role,
            "username": user.username
        }
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

        response = make_response(redirect(url_for('student.web_list_students')))
        set_access_cookies(response, access_token)
        flash(f"Welcome back, {user.username}! Logged in as {user.role}.", "success")
        return response

    return render_template('login.html')


@auth_bp.route('/logout')
def web_logout():
    """Logs out user by clearing JWT cookies."""
    response = make_response(redirect(url_for('auth.web_login')))
    unset_jwt_cookies(response)
    flash("Logged out successfully", "info")
    return response
