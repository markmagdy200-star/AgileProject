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