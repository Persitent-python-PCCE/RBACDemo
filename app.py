from flask import Flask, request, jsonify, flash, redirect
from config.database import init_db, db
from flask_jwt_extended import JWTManager
from controller.auth_controller import auth_bp
from controller.student_controller import student_bp

def create_app():
    app = Flask(__name__)
    init_db(app)
    app.config['SECRET_KEY'] = 'super-secret-flask-key-for-rbac-demo'

    app.config["JWT_SECRET_KEY"] = "super-secret-123-678"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def missing_token_callback(err_string):
        if request.is_json or request.path.startswith("/api"):
            return jsonify({
                "message": "Authorization token is missing",
                "error": "unauthorized"
            }), 401
        flash("Please login first to acces this page", "warning")
        return redirect("/")

    @jwt.invalid_token_loader
    def invalid_token_callback(err_string):
        if request.is_json or request.path.startswith("/api"):
                    return jsonify({
                        "message": "Authorization token is invalid",
                        "error": "invalid_token"
                    }), 401
        flash("session exipred or invalid token, login again", "warning")
        return redirect("/")




    with app.app_context():
        # db.drop_all()
        db.create_all()

    @app.route("/health")
    def health():
        return {"Status":"UP"}, 200

    @app.route("/")
    def home():
         return "FLASK ECOMM APP", 200
    return app




if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=3000, debug=True)
    
