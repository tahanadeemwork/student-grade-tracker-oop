class Student:
    def __init__(self, name):
        self.name = name
        self._grades = {}

    def add_grade(self, subject, grade):
        if subject not in self._grades:
            self._grades[subject] = []
        self._grades[subject].append(grade)

    def get_grades(self):
        return self._grades

    def calculate_average(self):
        all_grades = []
        for subject_grades in self._grades.values():
            all_grades.extend(subject_grades)

        count = self._count_recursive(all_grades)
        if count == 0:
            return 0

        total = self._sum_recursive(all_grades)
        return total / count

    def _sum_recursive(self, grades_list):
        if not grades_list:
            return 0
        return grades_list[0] + self._sum_recursive(grades_list[1:])

    def _count_recursive(self, grades_list):
        if not grades_list:
            return 0
        return 1 + self._count_recursive(grades_list[1:])

    def student_report(self):
        lines = [f"--- Report for {self.name} ---"]
        if not self._grades:
            lines.append("No grades recorded yet.")
            return "\n".join(lines)

        for subject, grades in self._grades.items():
            lines.append(f"{subject}: {grades}")

        avg = self.calculate_average()
        lines.append(f"Overall average: {avg:.2f}")
        return "\n".join(lines)

    def to_dict(self):
        return {
            'type': 'Student',
            'name': self.name,
            'grades': self._grades
        }

    @staticmethod
    def from_dict(data):
        if data['type'] == 'HonorsStudent':
            student = HonorsStudent(data['name'])
        else:
            student = Student(data['name'])

        student._grades = data['grades']
        return student

class HonorsStudent(Student):
    def calculate_average(self):
        percentage = super().calculate_average()
        return self._to_gpa(percentage)

    def _to_gpa(self, percentage):
        if percentage >= 90:
            return 4.0
        elif percentage >= 80:
            return 3.0
        elif percentage >= 70:
            return 2.0
        elif percentage >= 60:
            return 1.0
        else:
            return 0.0

    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'HonorsStudent'
        return data