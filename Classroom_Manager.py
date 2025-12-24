# Classroom_Manager.py
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import json
import os

@dataclass
class Classroom:
    id: str
    capacity: int
    location: Optional[str] = None
    is_under_maintenance: bool = False
    maintenance_notes: List[str] = field(default_factory=list)

@dataclass
class Reservation:
    id: int
    classroom_id: str
    reserved_by: str
    start_str: str # Store as string for JSON serialization
    end_str: str   # Store as string for JSON serialization

    # Helper to get datetime objects
    @property
    def start(self) -> datetime:
        return datetime.fromisoformat(self.start_str)

    @property
    def end(self) -> datetime:
        return datetime.fromisoformat(self.end_str)

class Scheduler:
    def __init__(self, storage_file="classrooms.json", res_file="reservations.json"):
        self.storage_file = storage_file
        self.res_file = res_file
        self.classrooms: List[Classroom] = []
        self.reservations: List[Reservation] = []
        self._next_reservation_id = 1
        self.load_data()

    def load_data(self):
        # Load Classrooms
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.classrooms = [Classroom(**room_data) for room_data in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.classrooms = [] # Reset if file is corrupted or missing

        # Load Reservations
        if os.path.exists(self.res_file):
            try:
                with open(self.res_file, 'r') as f:
                    data = json.load(f)
                    self.reservations = [Reservation(**res_data) for res_data in data]
                    # Ensure _next_reservation_id is correctly set
                    if self.reservations:
                        max_id = max(res.id for res in self.reservations)
                        self._next_reservation_id = max_id + 1
            except (json.JSONDecodeError, FileNotFoundError):
                self.reservations = [] # Reset if file is corrupted or missing
                self._next_reservation_id = 1

    def save_data(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump([asdict(r) for r in self.classrooms], f, indent=4)
            with open(self.res_file, 'w') as f:
                json.dump([asdict(r) for r in self.reservations], f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")


    def add_classroom(self, room: Classroom):
        if any(r.id == room.id for r in self.classrooms):
            raise ValueError(f"Classroom {room.id} already exists")
        self.classrooms.append(room)
        self.save_data()

    def report_maintenance(self, classroom_id: str, description: str):
        room = self._find_room(classroom_id)
        room.is_under_maintenance = True
        room.maintenance_notes.append(description)
        self.save_data()
        return f"Maintenance reported for {classroom_id}"

    def resolve_maintenance(self, classroom_id: str):
        room = self._find_room(classroom_id)
        room.is_under_maintenance = False
        self.save_data()
        return f"Maintenance resolved for {classroom_id}"

    def get_maintenance_reports(self, classroom_id: Optional[str] = None):
        if classroom_id:
            room = self._find_room(classroom_id)
            return room.maintenance_notes
        # all rooms
        return {r.id: r.maintenance_notes for r in self.classrooms}

    def reserve_classroom(self, classroom_id: str, start: datetime, end: datetime, reserved_by: str):
        room = self._find_room(classroom_id)
        if room.is_under_maintenance:
            return f"Classroom {classroom_id} is unavailable (maintenance)."

        # Check conflicts
        for r in self.reservations:
            # Use the @property to get datetime objects
            if r.classroom_id == classroom_id and not (end <= r.start or start >= r.end):
                return f"Classroom {classroom_id} is already reserved in this time slot."

        res = Reservation(
            id=self._next_reservation_id,
            classroom_id=classroom_id,
            reserved_by=reserved_by,
            start_str=start.isoformat(),
            end_str=end.isoformat()
        )
        self.reservations.append(res)
        self._next_reservation_id += 1
        self.save_data()
        return f"Reservation {res.id} created for classroom {classroom_id}"

    def check_availability(self, classroom_id: str, start: datetime, end: datetime) -> bool:
        room = self._find_room(classroom_id)
        if room.is_under_maintenance:
            return False

        for r in self.reservations:
            if r.classroom_id == classroom_id and not (end <= r.start or start >= r.end):
                return False
        return True

    # -------------------------
    # Helper
    # -------------------------
    def _find_room(self, classroom_id: str) -> Classroom:
        room = next((r for r in self.classrooms if r.id == classroom_id), None)
        if not room:
            raise ValueError(f"Classroom {classroom_id} not found")
        return room

