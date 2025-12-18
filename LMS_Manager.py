# LMS_Manager.py
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

class ContentType(Enum):
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    PRESENTATION = "presentation"
    AUDIO = "audio"

class AssignmentType(Enum):
    HOMEWORK = "homework"
    PROJECT = "project"
    LAB = "lab"
    ESSAY = "essay"

class LMSContent:
    def __init__(self, content_id: str, course_code: str, title: str, 
                 content_type: ContentType, url_or_path: str, description: str = ""):
        self.content_id = content_id
        self.course_code = course_code
        self.title = title
        self.content_type = content_type
        self.url_or_path = url_or_path
        self.description = description
        self.created_date = datetime.now().isoformat()
        self.views = 0
        self.views_by = []  # student_ids who viewed
    
    def to_dict(self):
        return {
            "content_id": self.content_id,
            "course_code": self.course_code,
            "title": self.title,
            "content_type": self.content_type.value,
            "url_or_path": self.url_or_path,
            "description": self.description,
            "created_date": self.created_date,
            "views": self.views,
            "views_by": self.views_by
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        content = cls(
            data["content_id"],
            data["course_code"],
            data["title"],
            ContentType(data["content_type"]),
            data["url_or_path"],
            data.get("description", "")
        )
        content.created_date = data.get("created_date", datetime.now().isoformat())
        content.views = data.get("views", 0)
        content.views_by = data.get("views_by", [])
        return content


class Assignment:
    def __init__(self, assignment_id: str, course_code: str, title: str, 
                 description: str, due_date: str, max_points: float,
                 assignment_type: AssignmentType = AssignmentType.HOMEWORK):
        self.assignment_id = assignment_id
        self.course_code = course_code
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_points = max_points
        self.assignment_type = assignment_type
        self.submissions = {}  # student_id -> {"submission": text, "submitted_date": date, "grade": None}
        self.created_date = datetime.now().isoformat()
    
    def submit_assignment(self, student_id: str, submission_text: str):
        """Student submits an assignment"""
        self.submissions[student_id] = {
            "submission": submission_text,
            "submitted_date": datetime.now().isoformat(),
            "grade": None,
            "feedback": ""
        }
    
    def grade_assignment(self, student_id: str, grade: float, feedback: str = ""):
        """Professor grades an assignment"""
        if student_id in self.submissions:
            self.submissions[student_id]["grade"] = grade
            self.submissions[student_id]["feedback"] = feedback
        else:
            raise ValueError(f"No submission found for student {student_id}")
    
    def to_dict(self):
        return {
            "assignment_id": self.assignment_id,
            "course_code": self.course_code,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "max_points": self.max_points,
            "assignment_type": self.assignment_type.value,
            "submissions": self.submissions,
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        assignment = cls(
            data["assignment_id"],
            data["course_code"],
            data["title"],
            data["description"],
            data["due_date"],
            data["max_points"],
            AssignmentType(data["assignment_type"])
        )
        assignment.submissions = data.get("submissions", {})
        assignment.created_date = data.get("created_date", datetime.now().isoformat())
        return assignment


class Quiz:
    def __init__(self, quiz_id: str, course_code: str, title: str, questions: List[Dict]):
        self.quiz_id = quiz_id
        self.course_code = course_code
        self.title = title
        self.questions = questions  # List of {question: str, options: [], correct_answer: int}
        self.time_limit = 30  # minutes
        self.attempts = {}  # student_id -> {score: float, answers: [], date: date}
        self.created_date = datetime.now().isoformat()
    
    def take_quiz(self, student_id: str, answers: List[int]) -> float:
        """Student takes quiz, returns score"""
        score = 0
        for i, (question, answer) in enumerate(zip(self.questions, answers)):
            if answer == question["correct_answer"]:
                score += 1
        
        percentage = (score / len(self.questions)) * 100
        
        self.attempts[student_id] = {
            "score": percentage,
            "answers": answers,
            "date": datetime.now().isoformat()
        }
        
        return percentage
    
    def get_quiz_results(self, student_id: str) -> Optional[Dict]:
        """Get quiz results for a student"""
        return self.attempts.get(student_id)
    
    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "course_code": self.course_code,
            "title": self.title,
            "questions": self.questions,
            "time_limit": self.time_limit,
            "attempts": self.attempts,
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        quiz = cls(
            data["quiz_id"],
            data["course_code"],
            data["title"],
            data["questions"]
        )
        quiz.time_limit = data.get("time_limit", 30)
        quiz.attempts = data.get("attempts", {})
        quiz.created_date = data.get("created_date", datetime.now().isoformat())
        return quiz


class Exam(Quiz):
    def __init__(self, exam_id: str, course_code: str, title: str, questions: List[Dict], duration: int = 120):
        super().__init__(exam_id, course_code, title, questions)
        self.time_limit = duration
        self.exam_date = ""
        self.location = ""
        self.proctored = False
    
    def schedule_exam(self, exam_date: str, location: str, proctored: bool = False):
        """Schedule an exam"""
        self.exam_date = exam_date
        self.location = location
        self.proctored = proctored


class Gradebook:
    def __init__(self, course_code: str):
        self.course_code = course_code
        self.grades = {}  # student_id -> {"assignments": {}, "quizzes": {}, "exams": {}, "final_grade": None}
        self.grading_scheme = {
            "assignments": 40,
            "quizzes": 20,
            "midterm": 20,
            "final_exam": 20
        }
    
    def add_grade(self, student_id: str, category: str, item_id: str, grade: float, max_grade: float = 100):
        """Add a grade for a student"""
        if student_id not in self.grades:
            self.grades[student_id] = {"assignments": {}, "quizzes": {}, "exams": {}, "final_grade": None}
        
        if category == "assignment":
            self.grades[student_id]["assignments"][item_id] = {"grade": grade, "max": max_grade}
        elif category == "quiz":
            self.grades[student_id]["quizzes"][item_id] = {"grade": grade, "max": max_grade}
        elif category == "exam":
            self.grades[student_id]["exams"][item_id] = {"grade": grade, "max": max_grade}
        
        # Recalculate final grade
        self.calculate_final_grade(student_id)
    
    def calculate_final_grade(self, student_id: str) -> float:
        """Calculate final grade based on grading scheme"""
        if student_id not in self.grades:
            return 0.0
        
        student_grades = self.grades[student_id]
        
        # Calculate assignment average
        assignment_total = sum(item["grade"] for item in student_grades["assignments"].values())
        assignment_count = len(student_grades["assignments"])
        assignment_avg = (assignment_total / assignment_count) if assignment_count > 0 else 0
        
        # Calculate quiz average
        quiz_total = sum(item["grade"] for item in student_grades["quizzes"].values())
        quiz_count = len(student_grades["quizzes"])
        quiz_avg = (quiz_total / quiz_count) if quiz_count > 0 else 0
        
        # Calculate exam average
        exam_total = sum(item["grade"] for item in student_grades["exams"].values())
        exam_count = len(student_grades["exams"])
        exam_avg = (exam_total / exam_count) if exam_count > 0 else 0
        
        # Weighted average
        final_grade = (
            assignment_avg * (self.grading_scheme["assignments"] / 100) +
            quiz_avg * (self.grading_scheme["quizzes"] / 100) +
            exam_avg * ((self.grading_scheme["midterm"] + self.grading_scheme["final_exam"]) / 100)
        )
        
        student_grades["final_grade"] = final_grade
        return final_grade
    
    def get_student_grades(self, student_id: str) -> Dict:
        """Get all grades for a student"""
        return self.grades.get(student_id, {})
    
    def to_dict(self):
        return {
            "course_code": self.course_code,
            "grades": self.grades,
            "grading_scheme": self.grading_scheme
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        gradebook = cls(data["course_code"])
        gradebook.grades = data.get("grades", {})
        gradebook.grading_scheme = data.get("grading_scheme", {
            "assignments": 40, "quizzes": 20, "midterm": 20, "final_exam": 20
        })
        return gradebook


class Feedback:
    def __init__(self, course_code: str):
        self.course_code = course_code
        self.feedbacks = []  # List of {"student_id": str, "feedback": str, "rating": int, "date": str}
    
    def add_feedback(self, student_id: str, feedback_text: str, rating: int = 5):
        """Student provides feedback for a course"""
        self.feedbacks.append({
            "student_id": student_id,
            "feedback": feedback_text,
            "rating": rating,
            "date": datetime.now().isoformat()
        })
    
    def get_average_rating(self) -> float:
        """Calculate average rating for the course"""
        if not self.feedbacks:
            return 0.0
        return sum(f["rating"] for f in self.feedbacks) / len(self.feedbacks)
    
    def get_feedbacks(self, min_rating: int = 0) -> List[Dict]:
        """Get all feedbacks, optionally filtered by minimum rating"""
        return [f for f in self.feedbacks if f["rating"] >= min_rating]


class LMSManager:
    def __init__(self, storage_folder="lms"):
        self.storage_folder = storage_folder
        if not os.path.exists(storage_folder):
            os.makedirs(storage_folder)
        
        # Subfolders for organization
        self.content_folder = os.path.join(storage_folder, "content")
        self.assignments_folder = os.path.join(storage_folder, "assignments")
        self.quizzes_folder = os.path.join(storage_folder, "quizzes")
        self.gradebooks_folder = os.path.join(storage_folder, "gradebooks")
        self.feedback_folder = os.path.join(storage_folder, "feedback")
        
        for folder in [self.content_folder, self.assignments_folder, 
                      self.quizzes_folder, self.gradebooks_folder, self.feedback_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    # Content Management
    def add_content(self, content: LMSContent):
        path = os.path.join(self.content_folder, f"{content.content_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content.to_dict(), f, indent=4)
    
    def get_content(self, content_id: str) -> Optional[LMSContent]:
        path = os.path.join(self.content_folder, f"{content_id}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return LMSContent.from_dict(data)
        return None
    
    def get_course_content(self, course_code: str) -> List[LMSContent]:
        """Get all content for a specific course"""
        contents = []
        for filename in os.listdir(self.content_folder):
            if filename.endswith(".json"):
                content = self.get_content(filename.replace(".json", ""))
                if content and content.course_code == course_code:
                    contents.append(content)
        return contents
    
    # Assignment Management
    def create_assignment(self, assignment: Assignment):
        path = os.path.join(self.assignments_folder, f"{assignment.assignment_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(assignment.to_dict(), f, indent=4)
    
    def get_assignment(self, assignment_id: str) -> Optional[Assignment]:
        path = os.path.join(self.assignments_folder, f"{assignment_id}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Assignment.from_dict(data)
        return None
    
    # Quiz Management
    def create_quiz(self, quiz: Quiz):
        path = os.path.join(self.quizzes_folder, f"{quiz.quiz_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(quiz.to_dict(), f, indent=4)
    
    def get_quiz(self, quiz_id: str) -> Optional[Quiz]:
        path = os.path.join(self.quizzes_folder, f"{quiz_id}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Quiz.from_dict(data)
        return None
    
    # Gradebook Management
    def get_gradebook(self, course_code: str) -> Gradebook:
        path = os.path.join(self.gradebooks_folder, f"{course_code}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Gradebook.from_dict(data)
        # Create new gradebook if doesn't exist
        return Gradebook(course_code)
    
    def save_gradebook(self, gradebook: Gradebook):
        path = os.path.join(self.gradebooks_folder, f"{gradebook.course_code}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(gradebook.to_dict(), f, indent=4)
    
    # Feedback Management
    def get_feedback(self, course_code: str) -> Feedback:
        path = os.path.join(self.feedback_folder, f"{course_code}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                feedback = Feedback(course_code)
                feedback.feedbacks = data.get("feedbacks", [])
                return feedback
        return Feedback(course_code)
    
    def save_feedback(self, feedback: Feedback):
        path = os.path.join(self.feedback_folder, f"{feedback.course_code}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({"feedbacks": feedback.feedbacks}, f, indent=4)