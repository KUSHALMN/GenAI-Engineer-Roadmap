students = {}

def add_student(name, grade):
    students[name] = grade
    print(f"Added: {name}")

def view_students():
    if not students:
        print("No students found.")
    for name, grade in students.items():
        print(f"{name}: {grade}")

def delete_student(name):
    if name in students:
        del students[name]
        print(f"Deleted: {name}")
    else:
        print("Student not found.")

add_student("Alice", "A")
add_student("Bob", "B")
view_students()
delete_student("Alice")
view_students()
