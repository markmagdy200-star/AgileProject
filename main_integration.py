# main_integration.py
import os
from datetime import datetime, timedelta

# Import all necessary components from the three files
from Classroom_Manager import Scheduler, Classroom, Reservation
from equipment_management import (
    EquipmentManager, Equipment, 
    LicenseManager, SoftwareLicense, 
    PersonAllocationManager, LaboratoryEquipmentManager
)
from Student_Manager import StudentManager

def setup_and_demo_system():
    """Initializes and demonstrates the integrated system."""
    
    # --- Initialization ---
    
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
    scheduler.add_classroom(Classroom(id="R201", capacity=25, location="North Wing"))
    print(f"Added Classrooms: {[r.id for r in scheduler.classrooms]}")

    # Add General Equipment
    eq_manager.add_equipment(Equipment("E001", "Projector", "AV"))
    eq_manager.add_equipment(Equipment("E002", "Whiteboard", "Stationery"))
    eq_manager.add_equipment(Equipment("E003", "Sound System", "AV"))
    print(f"Added Equipment: {[e for e in eq_manager.equipment_list]}")

    # Add Lab Equipment
    lab_eq_manager.add_lab_equipment(Equipment("L001", "Microscope", "Biology"))
    lab_eq_manager.add_lab_equipment(Equipment("L002", "Centrifuge", "Chemistry"))
    print(f"Added Lab Equipment: {[e for e in lab_eq_manager.lab_equipment]}")

    # Add Licenses
    license_manager.add_license(SoftwareLicense("S001", "DesignSuite", 10))
    license_manager.add_license(SoftwareLicense("S002", "ProgrammingIDE", 5))
    print(f"Added Licenses: {[l for l in license_manager.licenses]}")

    # Assign People
    person_manager.assign_professor("P001", "Computer Engineering")
    person_manager.assign_professor("P002", "Mechanical Engineering")
    person_manager.assign_student("S001", "Computer Engineering")
    print("Assigned Professor P001, P002 and Student S001.")

    # Add Student Records
    student_manager.add_student({
        "student_id": "001",
        "first_name": "Maria",
        "last_name": "Ibraheem", 
        "department": "Computer Engineering",
        "email": "maria@example.edu",
        "enrollment_year": 2019,
        "gpa": 2.2,
        "status": "enrolled"
    })
    
    student_manager.add_student({
        "student_id": "002", 
        "first_name": "Mark",
        "last_name": "Magdy", 
        "department": "Mechanical Engineering",
        "email": "mark@example.edu",
        "enrollment_year": 2020,
        "gpa": 3.5,
        "status": "enrolled"
    })
    
    student_manager.add_student({
        "student_id": "007", 
        "first_name": "James", 
        "last_name": "Bond", 
        "department": "Spy School", 
        "enrollment_year": 2021
    })
    print("Added student records to disk.")
    
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
    eq_manager.allocate_equipment("E001", "R101")
    print(f"Equipment E001 (Projector) allocated to R101.")
    print(f"Tracking: {eq_manager.track_equipment()[0]}")
    
    # 2. Allocate Lab Equipment
    lab_eq_manager.allocate_lab_equipment("L001", "S001")
    print(f"Lab Equipment L001 (Microscope) allocated to S001.")
    print(f"Tracking Lab: {lab_eq_manager.track_lab_equipment()[0]}")

    # 3. Allocate License Seat
    license_manager.allocate("S001")
    license_manager.allocate("S001")  # Allocate two seats
    print(f"Allocated two seats for DesignSuite (S001).")
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
    
    # 4. Edit student record
    student_manager.edit_student("001", {"email": "maria.newmail@uni.edu", "gpa": 2.5})
    print("Updated Maria's email and GPA")
    
    updated_maria = student_manager.get_student("001")
    print("Updated Maria:")
    student_manager.print_student(updated_maria)


def launch_comprehensive_gui():
    """Launch the comprehensive GUI application"""
    try:
        import tkinter as tk
        from GUI import UniversityManagementGUI
        
        print("🚀 Launching Comprehensive University Management System GUI...")
        print("Please wait while the GUI initializes...")
        
        root = tk.Tk()
        app = UniversityManagementGUI(root)
        print("✅ GUI initialized successfully!")
        print("📋 Available Features:")
        print("   • Classroom Management & Reservations")
        print("   • Equipment & Lab Equipment Tracking")
        print("   • Software License Management")
        print("   • Student Records System")
        print("   • People Allocation Management")
        print("   • Real-time Dashboard")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error: Could not import GUI module. Make sure GUI.py is in the same directory.")
        print(f"Detailed error: {e}")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("Make sure all required modules are available:")
        print("  - Classroom_Manager.py")
        print("  - equipment_management.py") 
        print("  - Student_Manager.py")
        print("  - GUI.py")


def system_status_check():
    """Check if all required components are available"""
    print("\n🔍 Performing System Status Check...")
    
    required_files = [
        "Classroom_Manager.py",
        "equipment_management.py", 
        "Student_Manager.py",
        "GUI.py"
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_ok = False
    
    if all_ok:
        print("✅ All system components are ready!")
    else:
        print("❌ Some components are missing. Please check the files above.")
    
    return all_ok


if __name__ == "__main__":
    # Display welcome message
    print("=" * 70)
    print("           COMPREHENSIVE UNIVERSITY MANAGEMENT SYSTEM")
    print("=" * 70)
    print("\nThis system integrates:")
    print("  • Student Information Management")
    print("  • Classroom Scheduling & Reservations") 
    print("  • Equipment & Laboratory Management")
    print("  • Software License Tracking")
    print("  • People Allocation System")
    
    # Check system status
    system_ready = system_status_check()
    
    if not system_ready:
        print("\n⚠️  Please ensure all required files are in the same directory.")
        exit(1)
    
    # Main menu
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Run Comprehensive Console Demo")
        print("2. Launch Full-Featured GUI Application")
        print("3. System Information")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            print("STARTING COMPREHENSIVE CONSOLE DEMO...")
            print("="*50)
            setup_and_demo_system()
            print("\n" + "="*50)
            print("CONSOLE DEMO COMPLETED")
            print("="*50)
            
        elif choice == "2":
            print("\n" + "="*50)
            print("LAUNCHING COMPREHENSIVE GUI...")
            print("="*50)
            launch_comprehensive_gui()
            print("\nGUI session ended. Returning to main menu...")
            
        elif choice == "3":
            print("\n" + "="*50)
            print("SYSTEM INFORMATION")
            print("="*50)
            print("Version: Comprehensive University Management System v2.0")
            print("Features:")
            print("  • 7-Tab GUI Interface with Real-time Updates")
            print("  • Student Records with File-based Storage")
            print("  • Classroom Reservation System with Conflict Detection")
            print("  • Equipment & Lab Equipment Allocation Tracking")
            print("  • Software License Seat Management")
            print("  • Professor & Student Department Allocation")
            print("  • Maintenance Reporting System")
            print("  • Interactive Dashboard with System Statistics")
            
        elif choice == "4":
            print("\nThank you for using the University Management System!")
            print("Goodbye! 👋")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")