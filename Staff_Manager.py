# Staff_Manager.py
import json
import os

class StaffManager:
    def __init__(self, file_path="staff.json"):
        self.file_path = file_path
        self.professors = {} # {prof_id: {details}}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    self.professors = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.professors = {} # Reset if file is corrupted or missing

    def save_data(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.professors, f, indent=4)
        except IOError as e:
            print(f"Error saving staff data: {e}")

    def add_professor(self, prof_id, name, department, email=""):
        if prof_id in self.professors:
            raise ValueError(f"Professor with ID {prof_id} already exists")
        self.professors[prof_id] = {
            "id": prof_id,
            "name": name,
            "department": department,
            "email": email,
            "courses_taught": [] # List of course codes
        }
        self.save_data()
        return f"Professor {name} (ID: {prof_id}) added."

    def get_professor(self, prof_id):
        return self.professors.get(prof_id)

    def get_all_professors(self):
        return list(self.professors.values()) # Return list of professor dicts

    def assign_course_to_prof(self, prof_id, course_code):
        prof = self.get_professor(prof_id)
        if not prof:
            raise ValueError(f"Professor with ID {prof_id} not found.")
        
        if course_code not in prof["courses_taught"]:
            prof["courses_taught"].append(course_code)
            self.save_data()
            return f"Course {course_code} assigned to Professor {prof['name']}."
        else:
            return f"Course {course_code} is already assigned to Professor {prof['name']}."

    def professor_exists(self, prof_id):
        return prof_id in self.professors

    # Placeholder methods from original StaffMember (kept for context if needed, but not managed by this class)
    # These are not implemented for StaffManager as it focuses on professors.
    # If you need TA/HR functionality, a separate manager would be required.
    # def assign_task(self, task): pass
    # def complete_task(self, task): pass
    # def fail_to_complete_task(self, task): pass
    # def view_performance(self): pass
    # def issue_reward(self, reward): pass
    # def view_payroll(self): raise NotImplementedError("Method not implemented")
    # def request_leave(self, start_date: str, end_date: str): raise NotImplementedError("Method not implemented")
    # def view_leave(self): raise NotImplementedError("Method not implemented")
    # def view_benefits(self): raise NotImplementedError("Method not implemented")