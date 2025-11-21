import shutil
shutil.rmtree("students", ignore_errors=True)

import os

class StudentManager:
    def __init__(self, folder="students"):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    def _path(self, student_id):
        return os.path.join(self.folder, f"{student_id}.txt")

    # Add Student
    def add_student(self, student):
        path = self._path(student["student_id"])

        if os.path.exists(path):
            raise ValueError("Student already exists.")

        with open(path, "w", encoding="utf-8") as f:
            for key, value in student.items():
                f.write(f"{key}: {value}\n")

    # Read Student File
    def get_student(self, student_id):
        path = self._path(student_id)
        if not os.path.exists(path):
            return None

        student = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    student[key.strip()] = value.strip()

        return student

    # Delete Student
    def delete_student(self, student_id):
        path = self._path(student_id)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    # Edit Student File
    def edit_student(self, student_id, updates):
        student = self.get_student(student_id)
        if student is None:
            return False

        # apply updates
        for key, value in updates.items():
            student[key] = value

        # rewrite file
        path = self._path(student_id)
        with open(path, "w", encoding="utf-8") as f:
            for k, v in student.items():
                f.write(f"{k}: {v}\n")

        return True

    # List All Students
    def list_students(self):
        data = []
        for filename in os.listdir(self.folder):
            if filename.endswith(".txt"):
                student_id = filename.replace(".txt", "")
                data.append(self.get_student(student_id))
        return data

    # Print Student 
    def print_student(self, student):
        if student is None:
            print("Student not found.")
            return
        
        print("\n---------------------------")
        for key, value in student.items():
            print(f"{key}: {value}")
        print("---------------------------\n")


# EXAMPLE USAGE (DEMO)
if __name__ == "__main__":
    manager = StudentManager()

    # Add Students
    print("Add students:\n")
    manager.add_student({
        "student_id": "001",
        "first_name": "Maria",
        "last_name": "Ibraheem",
        "dob": "2000-07-26",
        "department": "Computer Engineering",
        "email": "maria@example.edu",
        "enrollment_year": 2019,
        "gpa": 2.2,
        "status": "enrolled"
    })

    manager.add_student({
        "student_id": "002",
        "first_name": "Mark",
        "last_name": "Magdy",
        "dob": "2002-11-02",
        "department": "Mechanical Engineering",
        "email": "mark@example.edu",
        "enrollment_year": 2020,
        "gpa": 3.5,
        "status": "enrolled"
    })

    # List students 
    print("Listing all students:")
    for st in manager.list_students():
        manager.print_student(st)

    # Edit Maria
    print("Edit Maria's email:\n")
    manager.edit_student("001", {"email": "maria.newmail@uni.edu"})

    # Print edited Maria
    print("Updated Maria:")
    manager.print_student(manager.get_student("001"))

    # Delete Mark
    print("Deleting Mark:\n")
    manager.delete_student("002")

    # List remaining students
    print("Final Students List:")
    for st in manager.list_students():
        manager.print_student(st)
