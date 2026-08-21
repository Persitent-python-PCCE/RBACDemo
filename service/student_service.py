from models.student import Student

class StudentService():
    def __init__(self, dao):#dao = mock
        self.student_dao = dao
    #tightly coupled -> StudentDao()

    def add_student(self, name, email, age, course):
        existing_student = self.student_dao.get_student_by_email(email)
        if existing_student:
            raise ValueError("Email already exitst")
        student = Student(name = name, age = age, email = email, course = course)
        return self.student_dao.add_student(student)

    def get_all_students(self):
        return self.student_dao.get_all_students()

    def update_student(self, s_id, name = None, email = None, age = None, course = None):
        student = self.student_dao.get_student_by_id(s_id)
        if name:
            student.name = name
        if email:
            student.email = email
        if age:
            student.age = age
        if course:
            student.course = course

        return self.student_dao.update_student(student)

    def delete_student(self, s_id):
        student = self.student_dao.get_student_by_id(s_id)
        if not student:
            return False

        return self.student_dao.delete_student(student)