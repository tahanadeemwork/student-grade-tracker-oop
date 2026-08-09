from tracker import GradeTracker


def print_menu():
    print("\n--- Student Grade Tracker (OOP) ---")
    print("1. Add student")
    print("2. Add grade")
    print("3. View student report")
    print("4. View all students (sorted by average)")
    print("5. View unique subjects")
    print("6. Delete student")
    print("7. Exit")


def ask_honors():
    choice = input("Honors student? (y/n): ").strip().lower()
    return choice == "y"


def main():
    tracker = GradeTracker()
    tracker.load()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter student name: ").strip()
            honors = ask_honors()
            if tracker.add_student(name, honors=honors):
                tracker.save()
                print(f"Student '{name}' added.")

        elif choice == "2":
            name = input("Enter student name: ").strip()
            subject = input("Enter subject: ").strip()
            grade_input = input("Enter grade: ").strip()
            try:
                grade = float(grade_input)
            except ValueError:
                print("Invalid grade — must be a number.")
                continue
            honors = False
            if tracker.find_student(name) is None:
                honors = ask_honors()
            tracker.add_grade(name, subject, grade, honors=honors)
            tracker.save()
            print(f"Grade added for {name} in {subject}.")

        elif choice == "3":
            name = input("Enter student name: ").strip()
            student = tracker.find_student(name)
            if student is None:
                print(f"Student '{name}' not found.")
            else:
                print(student.student_report())

        elif choice == "4":
            tracker.view_all_students()

        elif choice == "5":
            tracker.view_unique_subjects()

        elif choice == "6":
            name = input("Enter student name to delete: ").strip()
            if tracker.remove_student(name):
                tracker.save()
                print(f"Student '{name}' deleted.")

        elif choice == "7":
            tracker.save()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()