# Student Grade Tracker — OOP Rewrite

A full rebuild of my original dictionary-based Student Grade Tracker, this time using a `Student` class and a `GradeTracker` manager class instead of loose functions operating on a list of dictionaries. This project was planned from the start of the fundamentals version specifically so the improvement from OOP would be something felt directly, not just read about.

## Features

- `Student` class: stores a name and a protected grades record, with `add_grade()`, `calculate_average()`, and `student_report()`
- `HonorsStudent(Student)`: overrides `calculate_average()` to convert the percentage average into a 4.0 GPA scale — the polymorphism checkpoint of this project
- `GradeTracker` class: manages the full roster — `add_student()`, `find_student()`, `remove_student()`, `add_grade()` (with auto-create for new students, carried over from the original version)
- `view_all_students()`: lists every student sorted by average, calling each object's own `calculate_average()` regardless of whether it's a `Student` or `HonorsStudent` — no type-checking involved
- Unique subjects tracked as a set at the `GradeTracker` level, maintained incrementally as grades are added
- Full save/reload via `to_dict()`/`from_dict()`, correctly reconstructing each student's actual subclass (an `HonorsStudent` reloads as an `HonorsStudent`, not a plain `Student`)
- `remove_student()` to delete a student and all their data

## How to run

Requires Python 3.x (standard library only).

```bash
python main.py
```

Follow the menu prompts. When adding a student (or a grade for a student who doesn't exist yet), you'll be asked whether they're an honors student — this determines whether a `Student` or `HonorsStudent` object gets created.

## Project structure

- `models.py` — `Student` and `HonorsStudent` class definitions, including `to_dict()`/`from_dict()`
- `tracker.py` — `GradeTracker` class: add/remove/find/report/save/load logic
- `main.py` — menu loop tying everything together
- `students.json` — generated automatically; stores the persisted roster
- `README.md` — this file

## Design notes

- **Encapsulation:** grade data (`_grades`) is only ever modified through `Student`'s own `add_grade()` method — never reached into directly from outside the class.
- **Polymorphism:** `HonorsStudent` overrides `calculate_average()` to return a GPA-scale number instead of a raw percentage. `student_report()` isn't overridden at all — it's inherited from `Student` — but because it internally calls `self.calculate_average()`, it automatically produces the correct output for either class, decided at runtime by the object's actual type.
- **Serialization:** each class has its own `to_dict()`, and a static factory method `Student.from_dict()` reads a `'type'` field to decide which class to reconstruct on load — the one place in the codebase where an explicit type check is needed at all.

## Before vs. after: fundamentals version vs. this OOP rewrite

The original version modeled each student as a dictionary inside a shared list, with every operation implemented as a free function that took the entire list (and often the student's name) as parameters. This rewrite surfaced several concrete improvements:

1. **Nothing protected the data before.** In the dictionary version, any code anywhere could do `student['grades']['Math'].append(-9999)` directly, bypassing all validation. Now, grade data can only be changed through `Student.add_grade()` — the object owns and protects its own state.

2. **Adding honors students would have meant scattering `if` checks everywhere.** To support a "different kind of student" in the dictionary version, I would have needed conditional logic (`if student['type'] == 'honors': ...`) inside every function that touched a student — report generation, averaging, sorting, all of it. With inheritance and polymorphism, `GradeTracker.view_all_students()` calls `student.calculate_average()` on a mixed list of `Student` and `HonorsStudent` objects with zero type-checking anywhere in that method — Python resolves which version to run automatically, based on the object's actual class.

3. **Functions no longer need external data handed to them.** `add_grade(subject, grade)` on `Student` doesn't need the whole student list or a name passed in anymore, because `self` already knows who it is and where its own data lives — the old version's `add_grade(students, name, subject, grade)` needed all of that passed in externally every single call.

## What I learned

The hardest part of this rewrite was serialization — specifically, making sure that saving and reloading didn't just restore raw data, but restored the *correct type* of object. It's easy to save a dictionary and load it back; it's a different problem entirely to save an object, lose it back to plain JSON, and then reconstruct it as the right class. Writing `from_dict()` as a static factory that reads a `'type'` field and decides between `Student` and `HonorsStudent` was the piece that took the most thought, and testing it — checking `type()` on a reloaded object and seeing `HonorsStudent` instead of `Student` — was the clearest proof that it actually worked.

The moment OOP's benefit really clicked, rather than just making sense in theory, was testing `view_all_students()` on a mixed list of regular and honors students. Calling `student.calculate_average()` in a single loop, with no `if` checks anywhere, and watching it correctly print a percentage for one student and a GPA for another — that's the point where polymorphism stopped being a term I could define and started being something I'd actually used to solve a real problem. In the dictionary version, doing the same thing would have meant a type-check buried in every function that touched student data.

If I were starting this rewrite over, I'd think more carefully upfront about which responsibilities belong on `Student` versus `GradeTracker` — for example, deciding that unique-subject tracking has to live at the tracker level (since a single student has no way to know about the whole roster) was something I worked out along the way rather than planning from the start.