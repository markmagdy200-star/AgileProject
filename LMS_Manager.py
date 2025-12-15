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
