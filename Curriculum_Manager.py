# Curriculum_Manager.py
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

class Course:
    def __init__(self, course_code: str, course_name: str, credits: int, 
                 department: str, description: str = "", prerequisites: List[str] = None):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.department = department
        self.description = description
        self.prerequisites = prerequisites or []
        self.is_core = False
        self.semesters_offered = []  # ["Fall", "Spring", "Summer"]
        self.professor_id = ""
        self.students_enrolled = []
        
    def to_dict(self):
        return {
            "course_code": self.course_code,
            "course_name": self.course_name,
            "credits": self.credits,
            "department": self.department,
            "description": self.description,
            "prerequisites": self.prerequisites,
            "is_core": self.is_core,
            "semesters_offered": self.semesters_offered,
            "professor_id": self.professor_id,
            "students_enrolled": self.students_enrolled
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        course = cls(
            data["course_code"],
            data["course_name"],
            data["credits"],
            data["department"],
            data.get("description", "")
        )
        course.prerequisites = data.get("prerequisites", [])
        course.is_core = data.get("is_core", False)
        course.semesters_offered = data.get("semesters_offered", [])
        course.professor_id = data.get("professor_id", "")
        course.students_enrolled = data.get("students_enrolled", [])
        return course


class CurriculumManager:
    def __init__(self, storage_folder="curriculum"):
        self.storage_folder = storage_folder
        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)
        
        self.core_courses = []
        self.elective_courses = []
        self.departments = ["Computer Engineering", "Mechanical Engineering", 
                           "Electrical Engineering", "Civil Engineering", "General"]
        self.load_course_lists() # Load existing core/elective lists

    def _get_course_path(self, course_code: str) -> str:
        return os.path.join(self.storage_folder, f"{course_code}.json")
    
    def load_course_lists(self):
        """Loads existing core and elective course codes on initialization."""
        self.core_courses = []
        self.elective_courses = []
        for filename in os.listdir(self.storage_folder):
            if filename.endswith(".json"):
                course_code = filename.replace(".json", "")
                course = self.get_course(course_code)
                if course:
                    if course.is_core:
                        self.core_courses.append(course_code)
                    else:
                        self.elective_courses.append(course_code)

    def add_course(self, course: Course):
        """Add a new course to the catalogue"""
        path = self._get_course_path(course.course_code)
        
        if os.path.exists(path):
            raise ValueError(f"Course {course.course_code} already exists.")
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(course.to_dict(), f, indent=4)
        
        # Update internal lists
        if course.is_core:
            self.core_courses.append(course.course_code)
        else:
            self.elective_courses.append(course.course_code)
    
    def get_course(self, course_code: str) -> Optional[Course]:
        """Retrieve a course by code"""
        path = self._get_course_path(course_code)
        
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return Course.from_dict(data)
            except (json.JSONDecodeError, FileNotFoundError):
                return None # Handle corrupted files
    
    def update_course(self, course_code: str, updates: dict):
        """Update course information"""
        course = self.get_course(course_code)
        if not course:
            raise ValueError(f"Course {course_code} not found.")
        
        # Track if core status changed to update lists
        old_is_core = course.is_core
        
        # Update fields
        for key, value in updates.items():
            if hasattr(course, key):
                setattr(course, key, value)
        
        # Save back
        with open(self._get_course_path(course_code), 'w', encoding='utf-8') as f:
            json.dump(course.to_dict(), f, indent=4)
        
        # Update core/elective lists if status changed
        new_is_core = course.is_core
        if old_is_core != new_is_core:
            if new_is_core:
                if course_code in self.elective_courses:
                    self.elective_courses.remove(course_code)
                if course_code not in self.core_courses:
                    self.core_courses.append(course_code)
            else: # Became elective
                if course_code in self.core_courses:
                    self.core_courses.remove(course_code)
                if course_code not in self.elective_courses:
                    self.elective_courses.append(course_code)
    
    def delete_course(self, course_code: str) -> bool:
        """Remove a course from catalogue"""
        path = self._get_course_path(course_code)
        
        if os.path.exists(path):
            os.remove(path)
            
            # Remove from lists
            if course_code in self.core_courses:
                self.core_courses.remove(course_code)
            if course_code in self.elective_courses:
                self.elective_courses.remove(course_code)
            return True
        return False
    
    def list_courses(self, department: str = None, core_only: bool = None) -> List[Course]:
        """List all courses, optionally filtered"""
        courses = []
        
        for filename in os.listdir(self.storage_folder):
            if filename.endswith(".json"):
                course_code = filename.replace(".json", "")
                course = self.get_course(course_code)
                
                if course:
                    if department and course.department != department:
                        continue
                    if core_only is not None and course.is_core != core_only:
                        continue
                    courses.append(course)
        
        return courses
    
    def assign_professor(self, course_code: str, professor_id: str):
        """Assign a professor to teach a course"""
        self.update_course(course_code, {"professor_id": professor_id})
    
    def enroll_student(self, course_code: str, student_id: str):
        """Enroll a student in a course"""
        course = self.get_course(course_code)
        if not course:
            raise ValueError(f"Course {course_code} not found.")
        
        if student_id not in course.students_enrolled:
            course.students_enrolled.append(student_id)
            self.update_course(course_code, {"students_enrolled": course.students_enrolled})
    
    def unenroll_student(self, course_code: str, student_id: str):
        """Remove a student from a course"""
        course = self.get_course(course_code)
        if not course:
            raise ValueError(f"Course {course_code} not found.")
        
        if student_id in course.students_enrolled:
            course.students_enrolled.remove(student_id)
            self.update_course(course_code, {"students_enrolled": course.students_enrolled})
    
    def get_student_courses(self, student_id: str) -> List[Course]:
        """Get all courses a student is enrolled in"""
        student_courses = []
        
        for filename in os.listdir(self.storage_folder):
            if filename.endswith(".json"):
                course_code = filename.replace(".json", "")
                course = self.get_course(course_code)
                
                if course and student_id in course.students_enrolled:
                    student_courses.append(course)
        
        return student_courses
    
    def get_professor_courses(self, professor_id: str) -> List[Course]:
        """Get all courses taught by a professor"""
        professor_courses = []
        
        for filename in os.listdir(self.storage_folder):
            if filename.endswith(".json"):
                course_code = filename.replace(".json", "")
                course = self.get_course(course_code)
                
                if course and course.professor_id == professor_id:
                    professor_courses.append(course)
        
        return professor_courses


class StudentPlanner:
    def __init__(self, storage_file="student_plans.json"):
        self.storage_file = storage_file
        self.student_plans = {}  # student_id -> {semester: [course_codes]}
        self.load_plans()

    def load_plans(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.student_plans = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.student_plans = {}

    def save_plans(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.student_plans, f, indent=4)
        except IOError as e:
            print(f"Error saving student plans: {e}")
    
    def create_study_plan(self, student_id: str, semester: str, course_codes: List[str]):
        """Create or update a student's semester study plan"""
        if student_id not in self.student_plans:
            self.student_plans[student_id] = {}
        
        self.student_plans[student_id][semester] = course_codes
        self.save_plans()
    
    def get_study_plan(self, student_id: str, semester: str = None) -> Dict:
        """Get student's study plan for a specific or all semesters"""
        if student_id not in self.student_plans:
            return {}
        
        if semester:
            return {semester: self.student_plans[student_id].get(semester, [])}
        
        return self.student_plans[student_id]
    
    def add_course_to_plan(self, student_id: str, semester: str, course_code: str):
        """Add a course to student's semester plan"""
        if student_id not in self.student_plans:
            self.student_plans[student_id] = {}
        
        if semester not in self.student_plans[student_id]:
            self.student_plans[student_id][semester] = []
        
        if course_code not in self.student_plans[student_id][semester]:
            self.student_plans[student_id][semester].append(course_code)
            self.save_plans()
    
    def remove_course_from_plan(self, student_id: str, semester: str, course_code: str):
        """Remove a course from student's semester plan"""
        if (student_id in self.student_plans and 
            semester in self.student_plans[student_id] and 
            course_code in self.student_plans[student_id][semester]):
            
            self.student_plans[student_id][semester].remove(course_code)
            self.save_plans()
