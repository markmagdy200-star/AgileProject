# Student_Manager.py
import os
import shutil

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
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        key, value = line.strip().split(":", 1)
                        student[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error reading student file {path}: {e}")
            return None # Return None if file is unreadable

        return student
    
    def student_exists(self, student_id):
        """Checks if a student record exists."""
        return os.path.exists(self._path(student_id))

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
        try:
            with open(path, "w", encoding="utf-8") as f:
                for k, v in student.items():
                    f.write(f"{k}: {v}\n")
        except IOError as e:
            print(f"Error writing to student file {path}: {e}")
            return False
        return True

    # List All Students
    def list_students(self):
        data = []
        if not os.path.exists(self.folder):
            return data 
            
        for filename in os.listdir(self.folder):
            if filename.endswith(".txt"):
                student_id = filename.replace(".txt", "")
                student_data = self.get_student(student_id)
                if student_data: # Ensure data was read successfully
                    data.append(student_data)
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
