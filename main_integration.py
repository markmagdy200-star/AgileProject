# main_integration.py
import os
from datetime import datetime, timedelta

# Import all necessary components from the three files
# The relative import structure is based on the assumption that these files
# are in the same directory and meant to be imported this way.

# --- Imports from Classroom_Manager.py ---
from Classroom_Manager import Scheduler, Classroom, Reservation 

# --- Imports from equipment_management.py ---
from equipment_management import (
    EquipmentManager, Equipment, 
    LicenseManager, SoftwareLicense, 
    PersonAllocationManager, LaboratoryEquipmentManager
)

# --- Imports from Student_Manager.py ---
from Student_Manager import StudentManager 


def setup_and_demo_system():
    """Initializes and demonstrates the integrated system."""
    
    # --- Initialization ---
    
    # Clean up the students folder from any previous runs
    # (The cleanup is handled by a line at the start of Student_Manager.py)
    
    print("--- 📚 System Initialization ---")
    
    # Managers
    scheduler = Scheduler()
    eq_manager = EquipmentManager()
    license_manager = LicenseManager()
    person_manager = PersonAllocationManager()
    lab_eq_manager = LaboratoryEquipmentManager()
    student_manager = StudentManager()

    # Add Classrooms
    scheduler.add_classroom(Classroom(id="R101", capacity=30, location="West Wing"))
    scheduler.add_classroom(Classroom(id="R102", capacity=50, location="West Wing"))
    print(f"Added Classrooms: {[r.id for r in scheduler.classrooms]}")

    # Add General Equipment
    eq_manager.add_equipment(Equipment("E001", "Projector", "AV"))
    eq_manager.add_equipment(Equipment("E002", "Whiteboard", "Stationery"))
    print(f"Added Equipment: {[e for e in eq_manager.equipment_list]}")

    # Add Lab Equipment (Uses the same Equipment class but tracked separately)
    lab_eq_manager.add_lab_equipment(Equipment("L001", "Microscope", "Biology"))
    print(f"Added Lab Equipment: {[e for e in lab_eq_manager.lab_equipment]}")

    # Add Licenses
    license_manager.add_license(SoftwareLicense("S001", "DesignSuite", 10))
    print(f"Added Licenses: {[l for l in license_manager.licenses]}")

    # Assign People
    person_manager.assign_professor("P001", "Computer Engineering")
    person_manager.assign_student("S001", "Computer Engineering")
    print("Assigned Professor P001 and Student S001.")

    # Add Student Record (to file system)
    student_manager.add_student({
        "student_id": "007", 
        "first_name": "James", 
        "last_name": "Bond", 
        "department": "Spy School", 
        "enrollment_year": 2021
    })
    print("Added Student 007 record to disk.")
    
    print("\n" + "="*50 + "\n")
    
    # --- Integration Demo ---

    print("--- 🗓️ Classroom Scheduling Demo ---")
    
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    later = now + timedelta(hours=1)
    
    # 1. Successful Reservation
    result = scheduler.reserve_classroom("R101", now, later, "Prof. P001")
    print(f"Reservation R101 (1 hour): {result}")
    
    # 2. Conflict Check
    conflict_start = now + timedelta(minutes=30)
    conflict_end = later + timedelta(minutes=30)
    result = scheduler.reserve_classroom("R101", conflict_start, conflict_end, "Student S001")
    print(f"Reservation R101 (Conflict): {result}")
    
    # 3. Maintenance Check
    scheduler.report_maintenance("R102", "Projector bulb replacement")
    result = scheduler.reserve_classroom("R102", now, later, "Another Prof")
    print(f"Reservation R102 (Maintenance): {result}")
    print(f"R102 Maintenance Notes: {scheduler.get_maintenance_reports('R102')}")

    print("\n" + "="*50 + "\n")
    
    print("--- 🛠️ Equipment and Licensing Demo ---")
    
    # 1. Allocate General Equipment
    eq_manager.allocate_equipment("E001", "R101") # Allocate Projector to classroom R101
    print(f"Equipment E001 (Projector) allocated to R101.")
    print(f"Tracking: {eq_manager.track_equipment()[0]}")
    
    # 2. Allocate Lab Equipment (Separately managed)
    lab_eq_manager.allocate_lab_equipment("L001", "S001") # Allocate Microscope to Student S001
    print(f"Lab Equipment L001 (Microscope) allocated to S001.")
    print(f"Tracking Lab: {lab_eq_manager.track_lab_equipment()[0]}")

    # 3. Allocate License Seat
    license_manager.allocate("S001")
    print(f"Allocated one seat for DesignSuite (S001).")
    print(f"License Tracking: {license_manager.track_licenses()}")

    print("\n" + "="*50 + "\n")

    print("--- 🧑‍🎓 Student and People Demo ---")
    
    # 1. Retrieve Student Record
    student_007 = student_manager.get_student("007")
    print("Retrieved Student 007:")
    student_manager.print_student(student_007)

    # 2. Update Student's Allocation in central People Manager
    person_manager.assign_student("007", "Field Operations")
    print(f"Student 007's department in People Manager updated to: {person_manager.student_allocations['007']}")
    
    # 3. List all professors/students in the Person Allocation Manager
    print("All people tracking:")
    for role, people in person_manager.track_people().items():
        print(f"  {role.capitalize()}: {people}")


if __name__ == "__main__":
    setup_and_demo_system()