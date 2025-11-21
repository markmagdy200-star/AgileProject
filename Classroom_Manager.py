from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

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
    start: datetime
    end: datetime

class Scheduler:
    def __init__(self):
        self.classrooms: List[Classroom] = []
        self.reservations: List[Reservation] = []
        self._next_reservation_id = 1

    # -------------------------
    # CLASSROOM MANAGEMENT
    # -------------------------
    def add_classroom(self, room: Classroom):
        self.classrooms.append(room)

    def report_maintenance(self, classroom_id: str, description: str):
        room = self._find_room(classroom_id)
        room.is_under_maintenance = True
        room.maintenance_notes.append(description)
        return f"Maintenance reported for {classroom_id}: {description}"

    def resolve_maintenance(self, classroom_id: str):
        room = self._find_room(classroom_id)
        room.is_under_maintenance = False
        return f"Maintenance resolved for {classroom_id}"

    def get_maintenance_reports(self, classroom_id: Optional[str] = None):
        if classroom_id:
            room = self._find_room(classroom_id)
            return room.maintenance_notes
        # all rooms
        return {r.id: r.maintenance_notes for r in self.classrooms}

    # -------------------------
    # RESERVATION SYSTEM
    # -------------------------
    def reserve_classroom(self, classroom_id: str, start: datetime, end: datetime, reserved_by: str):
        room = self._find_room(classroom_id)

        if room.is_under_maintenance:
            return f"Classroom {classroom_id} is unavailable (maintenance)."

        # Check reservation conflicts
        for r in self.reservations:
            if r.classroom_id == classroom_id and not (end <= r.start or start >= r.end):
                return f"Classroom {classroom_id} is already reserved in this time slot."

        res = Reservation(
            id=self._next_reservation_id,
            classroom_id=classroom_id,
            reserved_by=reserved_by,
            start=start,
            end=end
        )

        self.reservations.append(res)
        self._next_reservation_id += 1

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