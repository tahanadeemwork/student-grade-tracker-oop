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

