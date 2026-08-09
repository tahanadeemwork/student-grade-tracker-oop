from models import Student, HonorsStudent
import json

DATA_FILE = "students.json"

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

    def view_all_students(self):
        if not self.students:
            print("No students recorded yet.")
            return

        summaries = []
        for s in self.students:
            avg = s.calculate_average()
            summaries.append((s.name, avg))

        summaries.sort(key=lambda pair: pair[1], reverse=True)

        print("\n--- All Students (sorted by average) ---")
        for name, avg in summaries:
            print(f"{name}: {avg:.2f}")

    def view_unique_subjects(self):
        if not self.subjects:
            print("No subjects recorded yet.")
            return
        print("\n--- Unique Subjects ---")
        for subject in sorted(self.subjects):
            print(f"- {subject}")

    def save(self):
        data = [student.to_dict() for student in self.students]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = []
            self.subjects = set()
            return

        self.students = [Student.from_dict(d) for d in data]
        self.subjects = set()
        for student in self.students:
            for subject in student.get_grades().keys():
                self.subjects.add(subject)