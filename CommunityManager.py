# Community_Manager.py

from datetime import datetime
from typing import List, Dict, Optional
import uuid


# ---------------------------------------------------------
# Core Models
# ---------------------------------------------------------

class Message:
    def __init__(self, sender_id: str, receiver_id: str, content: str):
        self.message_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.is_deleted_by_sender = False
        self.is_deleted_by_receiver = False


class Announcement:
    def __init__(self, created_by: str, title: str, content: str, target: Dict):
        """
        target examples:
        {"type": "course", "course_code": "CS101"}
        {"type": "department", "department": "Computer Engineering"}
        """
        self.announcement_id = str(uuid.uuid4())
        self.created_by = created_by
        self.title = title
        self.content = content
        self.target = target
        self.timestamp = datetime.now().isoformat()


class MeetingRequest:
    def __init__(self, student_id: str, professor_id: str, proposed_time: str, note: str = ""):
        self.request_id = str(uuid.uuid4())
        self.student_id = student_id
        self.professor_id = professor_id
        self.proposed_time = proposed_time
        self.note = note
        self.status = "PENDING"  # PENDING | APPROVED | REJECTED
        self.created_at = datetime.now().isoformat()


# ---------------------------------------------------------
# Community Manager
# ---------------------------------------------------------

class CommunityManager:
    def __init__(self, curriculum_manager=None, lms_manager=None):
        # Messaging
        self.messages: List[Message] = []

        # Announcements
        self.announcements: List[Announcement] = []

        # Meetings
        self.meeting_requests: List[MeetingRequest] = []

        # Parent -> students mapping
        self.parent_students: Dict[str, List[str]] = {}

        # External modules (read-only usage)
        self.curriculum_manager = curriculum_manager
        self.lms_manager = lms_manager

    # -----------------------------------------------------
    # Parent Management
    # -----------------------------------------------------

    def register_parent(self, parent_id: str, student_ids: List[str]):
        """One parent -> many students"""
        self.parent_students[parent_id] = student_ids

    def get_parent_students(self, parent_id: str) -> List[str]:
        return self.parent_students.get(parent_id, [])

    # -----------------------------------------------------
    # Messaging
    # -----------------------------------------------------

    def send_message(self, sender_id: str, receiver_id: str, content: str):
        message = Message(sender_id, receiver_id, content)
        self.messages.append(message)
        return message.message_id

    def get_inbox(self, user_id: str) -> List[Message]:
        return [
            m for m in self.messages
            if m.receiver_id == user_id and not m.is_deleted_by_receiver
        ]

    def get_sent_messages(self, user_id: str) -> List[Message]:
        return [
            m for m in self.messages
            if m.sender_id == user_id and not m.is_deleted_by_sender
        ]

    def delete_message_for_user(self, message_id: str, user_id: str):
        for msg in self.messages:
            if msg.message_id == message_id:
                if msg.sender_id == user_id:
                    msg.is_deleted_by_sender = True
                elif msg.receiver_id == user_id:
                    msg.is_deleted_by_receiver = True
                return True
        return False

    # -----------------------------------------------------
    # Announcements
    # -----------------------------------------------------

    def create_announcement(self, created_by: str, title: str, content: str, target: Dict):
        announcement = Announcement(created_by, title, content, target)
        self.announcements.append(announcement)
        return announcement.announcement_id

    def get_announcements_for_student(self, student_id: str) -> List[Announcement]:
        visible = []

        student_courses = []
        student_department = None

        if self.curriculum_manager:
            student_courses = [
                c.course_code for c in self.curriculum_manager.get_student_courses(student_id)
            ]

            if student_courses:
                student_department = self.curriculum_manager.get_course(student_courses[0]).department

        for ann in self.announcements:
            if ann.target["type"] == "course" and ann.target.get("course_code") in student_courses:
                visible.append(ann)

            elif ann.target["type"] == "department" and ann.target.get("department") == student_department:
                visible.append(ann)

        return visible

    # -----------------------------------------------------
    # Meeting Requests
    # -----------------------------------------------------

    def request_meeting(self, student_id: str, professor_id: str, proposed_time: str, note: str = ""):
        request = MeetingRequest(student_id, professor_id, proposed_time, note)
        self.meeting_requests.append(request)
        return request.request_id

    def respond_to_meeting(self, request_id: str, approve: bool):
        for req in self.meeting_requests:
            if req.request_id == request_id:
                req.status = "APPROVED" if approve else "REJECTED"
                return True
        return False

    def get_meetings_for_professor(self, professor_id: str) -> List[MeetingRequest]:
        return [r for r in self.meeting_requests if r.professor_id == professor_id]

    def get_meetings_for_student(self, student_id: str) -> List[MeetingRequest]:
        return [r for r in self.meeting_requests if r.student_id == student_id]

    # -----------------------------------------------------
    # Parent: View Academic Progress (Read-Only)
    # -----------------------------------------------------

    def get_child_academic_progress(self, parent_id: str) -> Dict:
        """
        Returns grades for all children of a parent.
        Consumes LMS Gradebook (read-only).
        """
        result = {}

        if not self.lms_manager:
            return result

        for student_id in self.get_parent_students(parent_id):
            result[student_id] = {}

            # Iterate through all courses by scanning gradebooks folder
            # (Same philosophy as LMSManager)
            try:
                for course_code in self.lms_manager.get_gradebook(course_code=None).grades.keys():
                    gradebook = self.lms_manager.get_gradebook(course_code)
                    result[student_id][course_code] = gradebook.get_student_grades(student_id)
            except Exception:
                pass

        return result
