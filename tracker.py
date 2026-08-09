from models import Student, HonorsStudent


class GradeTracker:
    def __init__(self):
        self.students = []
        self.subjects = set()

    def add_student(self, name, honors=False):
        if self.find_student(name) is not None:
            print(f"Student '{name}' already exists.")
            return False

        if honors:
            student = HonorsStudent(name)
        else:
            student = Student(name)

        self.students.append(student)
        return True

    def find_student(self, name):
        for s in self.students:
            if s.name.lower() == name.lower():
                return s
        return None

    def remove_student(self, name):
        student = self.find_student(name)
        if student is None:
            print(f"Student '{name}' not found.")
            return False
        self.students.remove(student)
        return True

    def add_grade(self, name, subject, grade, honors=False):
        student = self.find_student(name)
        if student is None:
            self.add_student(name, honors=honors)
            student = self.find_student(name)
            print(f"Student '{name}' didn't exist — created automatically.")

        student.add_grade(subject, grade)
        self.subjects.add(subject)
        return True

    