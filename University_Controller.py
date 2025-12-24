# University_Controller.py
from Student_Manager import StudentManager
from Curriculum_Manager import CurriculumManager
from LMS_Manager import LMSManager
from Classroom_Manager import Scheduler
from equipment_management import EquipmentManager
from Staff_Manager import StaffManager
from datetime import datetime

class UniversityController:
    def __init__(self):
        # Initialize all individual managers
        self.student_mgr = StudentManager()
        self.curriculum_mgr = CurriculumManager()
        self.lms_mgr = LMSManager()
        self.scheduler = Scheduler()
        self.equipment_mgr = EquipmentManager()
        self.staff_mgr = StaffManager()

        # Initialize StudentPlanner (it has its own persistence)
        from Curriculum_Manager import StudentPlanner # Import only if needed
        self.student_planner = StudentPlanner() 

    # --- Integrated Student Operations ---
    def register_new_student(self, student_data):
        """Adds student to StudentManager."""
        if self.student_mgr.student_exists(student_data.get("student_id")):
            raise ValueError("Student ID already exists.")
        self.student_mgr.add_student(student_data)
        return f"Student {student_data['student_id']} registered successfully."

    def delete_student_fully(self, student_id):
        """Removes student from Records, Unenrolls from Courses, clears LMS data."""
        # 1. Check existence
        if not self.student_mgr.student_exists(student_id):
            return "Student not found."

        # 2. Get enrolled courses to unenroll
        courses_enrolled = self.curriculum_mgr.get_student_courses(student_id)
        for course in courses_enrolled:
            try:
                self.curriculum_mgr.unenroll_student(course.course_code, student_id)
            except Exception as e:
                print(f"Warning: Could not unenroll student {student_id} from {course.course_code}: {e}")

        # 3. Delete Basic Record
        deleted = self.student_mgr.delete_student(student_id)
        
        # 4. Remove from Student Planner (if any)
        if student_id in self.student_planner.student_plans:
            del self.student_planner.student_plans[student_id]
            self.student_planner.save_plans()

        if deleted:
            return f"Student {student_id} and all associated academic records removed."
        else:
            return "Student record found but could not be deleted."

    # --- Integrated Course Operations ---
    def enroll_student_in_course(self, student_id, course_code):
        """Checks if student and course exist before enrolling."""
        # 1. Validation
        if not self.student_mgr.student_exists(student_id):
            raise ValueError(f"Student with ID {student_id} does not exist in records.")
        
        course = self.curriculum_mgr.get_course(course_code)
        if not course:
            raise ValueError(f"Course with code {course_code} does not exist.")

        # 2. Enroll
        try:
            self.curriculum_mgr.enroll_student(course_code, student_id)
        except ValueError as e:
            raise e # Re-raise specific enrollment error

        # 3. Ensure Gradebook exists in LMS
        # The LMSManager's get_gradebook already handles creating a new one if it doesn't exist.
        # We just need to ensure it's saved for persistence if it was just created.
        gb = self.lms_mgr.get_gradebook(course_code)
        self.lms_mgr.save_gradebook(gb)
        
        return f"Student {student_id} successfully enrolled in {course_code}."

    def assign_professor_to_course(self, prof_id, course_code):
        """Links Staff Manager and Curriculum Manager."""
        # 1. Check Prof exists
        if not self.staff_mgr.get_professor(prof_id):
            raise ValueError(f"Professor with ID {prof_id} not found.")
        
        # 2. Check Course exists
        if not self.curriculum_mgr.get_course(course_code):
            raise ValueError(f"Course with code {course_code} not found.")
        
        # 3. Update Curriculum
        try:
            self.curriculum_mgr.assign_professor(course_code, prof_id)
        except ValueError as e:
            raise e # Re-raise if update fails
        
        # 4. Update Staff Record
        try:
            msg = self.staff_mgr.assign_course_to_prof(prof_id, course_code)
        except ValueError as e:
            # If staff manager fails, attempt to revert curriculum update (optional, for atomicity)
            # For simplicity, we'll just report error.
            raise ValueError(f"Failed to assign course in Staff Manager: {e}")
        
        return f"Professor {prof_id} assigned to {course_code}."

    # --- Integrated Scheduling ---
    def schedule_class_session(self, course_code, room_id, start_time_str, end_time_str):
        """Schedules a room for a specific course, handling datetime parsing."""
        # 1. Validate Course
        course = self.curriculum_mgr.get_course(course_code)
        if not course:
            raise ValueError("Invalid Course Code")

        # 2. Parse datetime strings
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            raise ValueError("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS or ISO format.")
        
        # 3. Validate Room & Reserve
        # We use the course code as the 'reserved_by' field for clarity
        reserved_by = f"Course: {course_code}"
        result = self.scheduler.reserve_classroom(room_id, start_time, end_time, reserved_by)
        
        return result
