from datetime import datetime
from typing import List, Dict, Optional


# ---------------------------------------------------------
# Equipment Management
# ---------------------------------------------------------

class Equipment:
    def __init__(self, equipment_id: str, name: str, category: str):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.is_allocated = False
        self.allocated_to = None
        self.allocation_date = None

    def allocate(self, allocated_to: str):
        if self.is_allocated:
            raise Exception(f"Equipment '{self.name}' is already allocated.")
        self.is_allocated = True
        self.allocated_to = allocated_to
        self.allocation_date = datetime.now()

    def release(self):
        self.is_allocated = False
        self.allocated_to = None
        self.allocation_date = None


class EquipmentManager:
    def __init__(self):
        self.equipment_list: Dict[str, Equipment] = {}

    def add_equipment(self, equipment: Equipment):
        self.equipment_list[equipment.equipment_id] = equipment

    def allocate_equipment(self, equipment_id: str, assigned_to: str):
        equipment = self.equipment_list.get(equipment_id)
        if not equipment:
            raise Exception("Equipment not found.")
        equipment.allocate(assigned_to)

    def release_equipment(self, equipment_id: str):
        equipment = self.equipment_list.get(equipment_id)
        if not equipment:
            raise Exception("Equipment not found.")
        equipment.release()

    def track_equipment(self):
        return [
            {
                "id": eq.equipment_id,
                "name": eq.name,
                "category": eq.category,
                "allocated": eq.is_allocated,
                "allocated_to": eq.allocated_to,
                "allocation_date": eq.allocation_date
            }
            for eq in self.equipment_list.values()
        ]


# ---------------------------------------------------------
# Software License Tracking
# ---------------------------------------------------------

class SoftwareLicense:
    def __init__(self, license_id: str, name: str, total_seats: int):
        self.license_id = license_id
        self.name = name
        self.total_seats = total_seats
        self.used_seats = 0

    def allocate_seat(self):
        if self.used_seats >= self.total_seats:
            raise Exception("No available license seats.")
        self.used_seats += 1

    def release_seat(self):
        if self.used_seats > 0:
            self.used_seats -= 1


class LicenseManager:
    def __init__(self):
        self.licenses: Dict[str, SoftwareLicense] = {}

    def add_license(self, license: SoftwareLicense):
        self.licenses[license.license_id] = license

    def allocate(self, license_id: str):
        license_obj = self.licenses.get(license_id)
        if not license_obj:
            raise Exception("License not found.")
        license_obj.allocate_seat()

    def release(self, license_id: str):
        license_obj = self.licenses.get(license_id)
        if not license_obj:
            raise Exception("License not found.")
        license_obj.release_seat()

    def track_licenses(self):
        return {
            lid: {
                "name": lic.name,
                "used_seats": lic.used_seats,
                "total_seats": lic.total_seats
            }
            for lid, lic in self.licenses.items()
        }


# ---------------------------------------------------------
# Professors and Student Allocation
# ---------------------------------------------------------

class PersonAllocationManager:
    def __init__(self):
        self.professor_departments: Dict[str, str] = {}
        self.student_allocations: Dict[str, str] = {}

    def assign_professor(self, professor_id: str, department: str):
        self.professor_departments[professor_id] = department

    def move_professor(self, professor_id: str, new_department: str):
        if professor_id not in self.professor_departments:
            raise Exception("Professor not found.")
        self.professor_departments[professor_id] = new_department

    def assign_student(self, student_id: str, department: str):
        self.student_allocations[student_id] = department

    def track_people(self):
        return {
            "professors": self.professor_departments,
            "students": self.student_allocations
        }


# ---------------------------------------------------------
# Laboratory Equipment Tracking & Allocation
# ---------------------------------------------------------

class LaboratoryEquipmentManager:
    def __init__(self):
        self.lab_equipment: Dict[str, Equipment] = {}

    def add_lab_equipment(self, equipment: Equipment):
        self.lab_equipment[equipment.equipment_id] = equipment

    def allocate_lab_equipment(self, equipment_id: str, allocated_to: str):
        if equipment_id not in self.lab_equipment:
            raise Exception("Lab equipment not found.")
        self.lab_equipment[equipment_id].allocate(allocated_to)

    def release_lab_equipment(self, equipment_id: str):
        if equipment_id not in self.lab_equipment:
            raise Exception("Lab equipment not found.")
        self.lab_equipment[equipment_id].release()

    def track_lab_equipment(self):
        return [
            {
                "id": eq.equipment_id,
                "name": eq.name,
                "category": eq.category,
                "allocated": eq.is_allocated,
                "allocated_to": eq.allocated_to
            }
            for eq in self.lab_equipment.values()
        ]
