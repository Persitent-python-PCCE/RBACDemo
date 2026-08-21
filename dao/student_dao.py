from config.database import db
from models.student import Student

class StudentDAO:

    def add_student(self, student):
        db.session.add(student)
        db.session.commit()
        return student

    def get_all_students(self):
        return Student.query.all()

    def get_student_by_id(self, s_id):
        return Student.query.get(s_id)

    def get_student_by_email(self, email):
        return Student.query.filter_by(email = email).first()

    def update_student(self, student):
        db.session.commit()
        return student

    def delete_student(self, student):
        db.session.delete(student)
        db.session.commit
        return True