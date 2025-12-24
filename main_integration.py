# main_integration.py
import os
from datetime import datetime, timedelta

# Import all necessary components from all files
from Classroom_Manager import Scheduler, Classroom, Reservation
from equipment_management import (
    EquipmentManager, Equipment, 
    LicenseManager, SoftwareLicense, 
    PersonAllocationManager, LaboratoryEquipmentManager
)
from Student_Manager import StudentManager
from Curriculum_Manager import CurriculumManager, Course, StudentPlanner
from LMS_Manager import LMSManager, LMSContent, Assignment, Quiz, ContentType, AssignmentType
from Staff_Manager import StaffManager # Import StaffManager
from University_Controller import UniversityController # Import the new Controller

# --- Console Demo Function ---
def setup_and_demo_system():
    """Initializes and demonstrates the integrated system via console output."""
    
    print("--- 📚 System Initialization (Console Demo) ---")
    
    # Initialize the Controller, which initializes all managers with persistence
    controller = UniversityController()

    # Seed sample data if files are missing (same logic as GUI initialization)
    initialize_system_with_sample_data(controller)
    
    # --- Integration Demo ---
    print("\n--- 🗓️ Classroom Scheduling Demo ---")
    try:
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        later = now + timedelta(hours=1)
        
        # 1. Successful Reservation
        result = controller.scheduler.reserve_classroom("R101", now, later, "Prof. P001")
        print(f"Reservation R101 (1 hour): {result}")
        
        # 2. Conflict Check
        conflict_start = now + timedelta(minutes=30)
        conflict_end = later + timedelta(minutes=30)
        result = controller.scheduler.reserve_classroom("R101", conflict_start, conflict_end, "Student S001")
        print(f"Reservation R101 (Conflict): {result}")
        
        # 3. Maintenance Check
        controller.scheduler.report_maintenance("R102", "Projector bulb replacement")
        result = controller.scheduler.reserve_classroom("R102", now, later, "Another Prof")
        print(f"Reservation R102 (Maintenance): {result}")
        print(f"R102 Maintenance Notes: {controller.scheduler.get_maintenance_reports('R102')}")
    except Exception as e:
        print(f"Error during Classroom Demo: {e}")

    print("\n--- 🛠️ Equipment and Licensing Demo ---")
    try:
        # 1. Allocate General Equipment
        controller.equipment_mgr.allocate_equipment("E001", "R101")
        print(f"Equipment E001 (Projector) allocated to R101.")
        print(f"Tracking: {controller.equipment_mgr.track_equipment()[0]}")
        
        # 2. Allocate Lab Equipment
        controller.lab_eq_manager.allocate_lab_equipment("L001", "S001")
        print(f"Lab Equipment L001 (Microscope) allocated to S001.")
        print(f"Tracking Lab: {controller.lab_eq_manager.track_lab_equipment()[0]}")

        # 3. Allocate License Seat
        controller.license_manager.allocate("S001")
        controller.license_manager.allocate("S001")  # Allocate two seats
        print(f"Allocated two seats for DesignSuite (S001).")
        print(f"License Tracking: {controller.license_manager.track_licenses()}")
    except Exception as e:
        print(f"Error during Equipment/License Demo: {e}")


    print("\n--- 🧑‍🎓 Student, Staff & People Demo ---")
    try:
        # 1. Retrieve Student Record
        student_007 = controller.student_manager.get_student("007")
        print("Retrieved Student 007:")
        controller.student_manager.print_student(student_007)

        # 2. Update Student's Allocation in central People Manager (using controller for check)
        print("Assigning student 007 to 'Field Operations' department via Controller...")
        controller.person_manager.assign_student("007", "Field Operations")
        print(f"Student 007's department in People Manager: {controller.person_manager.student_allocations.get('007')}")
        
        # 3. Add a Professor and assign them
        prof_id = "P003"
        prof_name = "Dr. Alex Lee"
        prof_dept = "Electrical Engineering"
        controller.staff_manager.add_professor(prof_id, prof_name, prof_dept, "alex.lee@uni.edu")
        print(f"Added Professor {prof_name} (ID: {prof_id}).")

        # Assign Professor to Course (using Controller)
        course_to_assign = "EE201"
        try:
            msg = controller.assign_professor_to_course(prof_id, course_to_assign)
            print(f"Assignment result: {msg}")
            print(f"Professor {prof_id} courses: {controller.staff_manager.get_professor(prof_id)['courses_taught']}")
            print(f"Course {course_to_assign} professor: {controller.curriculum_manager.get_course(course_to_assign).professor_id}")
        except ValueError as e:
            print(f"Error assigning professor to course: {e}")


        # 4. List all professors/students in the Person Allocation Manager
        print("All people tracking:")
        for role, people in controller.person_manager.track_people().items():
            print(f"  {role.capitalize()}: {people}")
        
        # 5. Edit student record
        print("Editing Maria's (001) record...")
        controller.student_manager.edit_student("001", {"email": "maria.newmail@uni.edu", "gpa": 2.5})
        updated_maria = controller.student_manager.get_student("001")
        print("Updated Maria:")
        controller.student_manager.print_student(updated_maria)
        
        # 6. Delete a student using the Controller for full cleanup
        print("Deleting student 002 (Mark Magdy) using the Controller...")
        delete_message = controller.delete_student_fully("002")
        print(f"Deletion result: {delete_message}")
        print("Listing remaining students:")
        remaining_students = controller.student_manager.list_students()
        if remaining_students:
            for st in remaining_students:
                controller.student_manager.print_student(st)
        else:
            print("No students remaining.")
            
    except Exception as e:
        print(f"Error during Student/Staff/People Demo: {e}")


    print("\n--- 📚 Curriculum & LMS Demo ---")
    try:
        # 1. List all courses
        courses = controller.curriculum_manager.list_courses()
        print(f"Total courses in catalogue: {len(courses)}")
        print("Sample courses:")
        for course in courses[:3]:
            print(f"  • {course.course_code}: {course.course_name} ({course.credits} credits), Prof: {course.professor_id if course.professor_id else 'Unassigned'}")
        
        # 2. Show student study plans
        print("\nStudent study plans:")
        maria_plan = controller.student_planner.get_study_plan("001")
        print("Maria's Fall 2024 plan:")
        for semester, course_list in maria_plan.items():
            print(f"  {semester}: {', '.join(course_list)}")
        
        # 3. Show LMS content for CS101
        print("\nLMS Content for CS101:")
        cs101_content = controller.lms_manager.get_course_content("CS101")
        for content in cs101_content:
            print(f"  • {content.title} ({content.content_type.value})")
        
        # 4. Show assignment submissions
        print("\nAssignment submissions for CS101:")
        cs101_assignment = controller.lms_manager.get_assignment("ASSIGN_001")
        if cs101_assignment:
            print(f"  Assignment: {cs101_assignment.title}")
            for student_id, submission in cs101_assignment.submissions.items():
                print(f"    Student {student_id}: {submission.get('grade', 'Not graded')}/100")
        else:
            print("  No assignment found for ASSIGN_001.")
        
        # 5. Show quiz results
        print("\nQuiz results for CS101:")
        cs101_quiz = controller.lms_manager.get_quiz("QUIZ_001")
        if cs101_quiz and "001" in cs101_quiz.attempts:
            attempt = cs101_quiz.attempts["001"]
            print(f"  Student 001: {attempt['score']:.1f}%")
        else:
            print("  No quiz attempts found for QUIZ_001.")
            
        # 6. Enroll student in a new course via Controller
        print("\nEnrolling student 001 in ME101 via Controller...")
        try:
            msg = controller.enroll_student_in_course("001", "ME101")
            print(f"Enrollment result: {msg}")
            me101_course = controller.curriculum_manager.get_course("ME101")
            print(f"ME101 students: {me101_course.students_enrolled}")
        except ValueError as e:
            print(f"Enrollment failed: {e}")

    except Exception as e:
        print(f"Error during Curriculum/LMS Demo: {e}")

    print("\n" + "="*50)
    print("✅ COMPREHENSIVE CONSOLE DEMO COMPLETED SUCCESSFULLY!")
    print("="*50)


# --- GUI Launcher Function ---
def launch_comprehensive_gui():
    """Launch the comprehensive GUI application"""
    try:
        import tkinter as tk
        from GUI import UniversityManagementGUI
        
        print("🚀 Launching Comprehensive University Management System GUI...")
        print("Please wait while the GUI initializes...")
        
        root = tk.Tk()
        app = UniversityManagementGUI(root) # GUI now uses the Controller internally
        print("✅ GUI initialized successfully!")
        print("📋 Available Features:")
        print("   • Classroom Management & Reservations")
        print("   • Equipment & Lab Equipment Tracking")
        print("   • Software License Management")
        print("   • Student Records System")
        print("   • Staff & Faculty Management")
        print("   • People Allocation Management")
        print("   • 📚 Curriculum & Course Catalogue Management")
        print("   • 🎓 Learning Management System (LMS)")
        print("   • 📝 Student Study Planning")
        print("   • 📊 Gradebook & Feedback System")
        print("   • Real-time Dashboard")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error: Could not import GUI module. Make sure GUI.py and all related files are in the same directory.")
        print(f"Detailed error: {e}")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("Ensure all required modules and their dependencies are correctly set up.")

# --- System Status Check ---
def system_status_check():
    """Check if all required components are available."""
    print("\n🔍 Performing System Status Check...")
    
    required_files = [
        "Classroom_Manager.py",
        "equipment_management.py", 
        "Student_Manager.py",
        "Curriculum_Manager.py",   
        "LMS_Manager.py",         
        "Staff_Manager.py",       # Added Staff Manager
        "University_Controller.py", # Added Controller
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

# --- Sample Data Seeding Function (Used by both Console Demo and GUI) ---
def initialize_system_with_sample_data(controller: UniversityController):
    """
    Seeds the system with sample data if data files are missing or empty.
    """
    print("Seeding system with sample data if files are missing or empty...")

    # Sample Classrooms
    if not controller.scheduler.classrooms:
        print("  - Adding sample classrooms...")
        try:
            controller.scheduler.add_classroom(Classroom(id="R101", capacity=30, location="West Wing"))
            controller.scheduler.add_classroom(Classroom(id="R102", capacity=50, location="East Wing"))
            controller.scheduler.add_classroom(Classroom(id="R201", capacity=25, location="North Wing"))
            print("    Sample classrooms added.")
        except Exception as e:
            print(f"    Error adding sample classrooms: {e}")

    # Sample Equipment
    if not controller.equipment_mgr.equipment_list:
        print("  - Adding sample equipment...")
        try:
            controller.equipment_mgr.add_equipment(Equipment("E001", "Projector", "AV"))
            controller.equipment_mgr.add_equipment(Equipment("E002", "Whiteboard", "Stationery"))
            controller.equipment_mgr.add_equipment(Equipment("E003", "Sound System", "AV"))
            print("    Sample equipment added.")
        except Exception as e:
            print(f"    Error adding sample equipment: {e}")

    # Sample Lab Equipment
    if not controller.lab_eq_manager.lab_equipment:
        print("  - Adding sample lab equipment...")
        try:
            controller.lab_eq_manager.add_lab_equipment(Equipment("L001", "Microscope", "Biology"))
            controller.lab_eq_manager.add_lab_equipment(Equipment("L002", "Centrifuge", "Chemistry"))
            print("    Sample lab equipment added.")
        except Exception as e:
            print(f"    Error adding sample lab equipment: {e}")

    # Sample Licenses
    if not controller.license_manager.licenses:
        print("  - Adding sample licenses...")
        try:
            controller.license_manager.add_license(SoftwareLicense("S001", "DesignSuite", 10))
            controller.license_manager.add_license(SoftwareLicense("S002", "ProgrammingIDE", 5))
            print("    Sample licenses added.")
        except Exception as e:
            print(f"    Error adding sample licenses: {e}")
            
    # Sample Staff (Professors)
    if not controller.staff_manager.professors:
        print("  - Adding sample professors...")
        try:
            controller.staff_manager.add_professor("P001", "Dr. Emily Carter", "Computer Engineering", "emily.carter@uni.edu")
            controller.staff_manager.add_professor("P002", "Prof. John Smith", "Mechanical Engineering", "john.smith@uni.edu")
            print("    Sample professors added.")
        except Exception as e:
            print(f"    Error adding sample professors: {e}")

    # Sample Student (if student records are empty)
    if not controller.student_manager.list_students():
        print("  - Adding sample students...")
        try:
            controller.student_manager.add_student({
                "student_id": "001", "first_name": "Maria", "last_name": "Ibraheem", 
                "department": "Computer Engineering", "enrollment_year": 2019, "email": "maria@example.edu",
                "gpa": 2.2, "status": "enrolled"
            })
            controller.student_manager.add_student({
                "student_id": "002", "first_name": "Mark", "last_name": "Magdy", 
                "department": "Mechanical Engineering", "enrollment_year": 2020, "email": "mark@example.edu",
                "gpa": 3.5, "status": "enrolled"
            })
            controller.student_manager.add_student({
                "student_id": "007", "first_name": "James", "last_name": "Bond", 
                "department": "Spy School", "enrollment_year": 2021
            })
            print("    Sample students added.")
        except Exception as e:
            print(f"    Error adding sample students: {e}")

    # Sample Curriculum Data
    if not controller.curriculum_manager.list_courses():
        print("  - Adding sample courses...")
        try:
            courses_to_add = [
                Course("CS101", "Introduction to Programming", 3, "Computer Engineering", "Basic programming concepts.", []),
                Course("CS201", "Data Structures", 4, "Computer Engineering", "Advanced data structures.", ["CS101"]),
                Course("ME101", "Engineering Mechanics", 3, "Mechanical Engineering", "Basic mechanics principles.", []),
                Course("EE201", "Circuit Analysis", 4, "Electrical Engineering", "Analysis of electrical circuits.", []),
            ]
            for course in courses_to_add:
                course.is_core = True # Mark as core for demo
                controller.curriculum_manager.add_course(course)
            print("    Sample courses added.")
        except Exception as e:
            print(f"    Error adding sample courses: {e}")

    # Sample Student Enrollments & Plan
    try:
        # Enroll students if not already enrolled
        if not controller.curriculum_manager.get_course("CS101").students_enrolled or "001" not in controller.curriculum_manager.get_course("CS101").students_enrolled:
            controller.enroll_student_in_course("001", "CS101")
        if not controller.curriculum_manager.get_course("CS101").students_enrolled or "002" not in controller.curriculum_manager.get_course("CS101").students_enrolled:
            controller.enroll_student_in_course("002", "CS101")
        if not controller.curriculum_manager.get_course("CS201").students_enrolled or "001" not in controller.curriculum_manager.get_course("CS201").students_enrolled:
            controller.enroll_student_in_course("001", "CS201")
        if not controller.curriculum_manager.get_course("ME101").students_enrolled or "002" not in controller.curriculum_manager.get_course("ME101").students_enrolled:
            controller.enroll_student_in_course("002", "ME101")
        
        # Create sample study plans if they don't exist
        if not controller.student_planner.get_study_plan("001") or "Fall 2024" not in controller.student_planner.get_study_plan("001"):
            controller.student_planner.create_study_plan("001", "Fall 2024", ["CS101", "CS201"])
        if not controller.student_planner.get_study_plan("002") or "Fall 2024" not in controller.student_planner.get_study_plan("002"):
            controller.student_planner.create_study_plan("002", "Fall 2024", ["CS101", "ME101"])
        print("  - Sample enrollments and study plans setup.")
    except Exception as e:
        print(f"    Error setting up enrollments/plans: {e}")

    # Sample LMS Data
    if not controller.lms_manager.get_course_content("CS101"):
        print("  - Adding sample LMS content...")
        try:
            content = LMSContent("CONT_001", "CS101", "Introduction to Python Video", ContentType.VIDEO, "https://example.com/python-intro.mp4", "A basic Python tutorial.")
            controller.lms_manager.add_content(content)
            
            assignment = Assignment("ASSIGN_001", "CS101", "Python Basics HW", "Complete exercises.", "2024-12-15", 100)
            controller.lms_manager.create_assignment(assignment)
            
            quiz = Quiz("QUIZ_001", "CS101", "Python Fundamentals Quiz", [{"question": "What is Python?", "options": ["Snake", "Language", "Food"], "correct_answer": 1}])
            controller.lms_manager.create_quiz(quiz)
            print("    Sample LMS content added.")
        except Exception as e:
            print(f"    Error adding sample LMS content: {e}")
            
    # Sample Gradebook entries
    try:
        # Ensure gradebooks are created/loaded
        gb_cs101 = controller.lms_manager.get_gradebook("CS101")
        # Add some grades if none exist for student 001
        if "001" not in gb_cs101.grades or not gb_cs101.grades["001"].get("assignments"):
            gb_cs101.add_grade("001", "assignment", "ASSIGN_001", 85)
            gb_cs101.add_grade("001", "quiz", "QUIZ_001", 75)
            controller.lms_manager.save_gradebook(gb_cs101)
            print("  - Sample grades added for CS101.")
    except Exception as e:
        print(f"    Error adding sample grades: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Display welcome message
    print("=" * 80)
    print("              COMPREHENSIVE UNIVERSITY MANAGEMENT SYSTEM v4.0")
    print("=" * 80)
    print("\nThis system integrates:")
    print("  • Student Information Management")
    print("  • Classroom Scheduling & Reservations") 
    print("  • Equipment & Laboratory Management")
    print("  • Software License Tracking")
    print("  • Staff & Faculty Management")
    print("  • People Allocation System")
    print("  • 📚 Curriculum & Course Catalogue")
    print("  • 🎓 Learning Management System (LMS)")
    print("  • 📝 Student Study Planning & Progress Tracking")
    print("  • 💬 Student Feedback & Course Ratings")
    print("  • 📈 Real-time Dashboard")
    
    # Check system status
    system_ready = system_status_check()
    
    if not system_ready:
        print("\n⚠️  Please ensure all required .py files are in the same directory and try again.")
        exit(1)
    
    # Main menu
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Run Comprehensive Console Demo (All Modules)")
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
            print("Version: Comprehensive University Management System v4.0")
            print("\nFeatures:")
            print("  • Integrated Managerial Control via UniversityController")
            print("  • Data Persistence for Classrooms, Staff, Students, LMS, etc.")
            print("  • 10-Tab GUI Interface with Real-time Updates")
            print("  • Classroom Scheduling & Reservations with Conflict Detection")
            print("  • Equipment & Lab Equipment Allocation Tracking")
            print("  • Software License Seat Management")
            print("  • Staff & Faculty Management (Professors)")
            print("  • People Allocation Management (Prof/Student Depts)")
            print("  • 📚 Curriculum & Course Catalogue Management")
            print("  • 🎓 Learning Management System (LMS)")
            print("  • 📝 Student Study Planning Tools")
            print("  • 📊 Gradebook & Feedback System")
            print("  • Real-time Dashboard with System Statistics")
            
            print("\nModules:")
            print("  - Classroom_Manager.py")
            print("  - equipment_management.py")
            print("  - Student_Manager.py")
            print("  - Curriculum_Manager.py")
            print("  - LMS_Manager.py")
            print("  - Staff_Manager.py")
            print("  - University_Controller.py")
            print("  - GUI.py")
            
        elif choice == "4":
            print("\nThank you for using the University Management System!")
            print("Goodbye! 👋")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
