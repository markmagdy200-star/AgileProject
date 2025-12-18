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
    curriculum_manager = CurriculumManager()  # NEW
    student_planner = StudentPlanner()        # NEW
    lms_manager = LMSManager()               # NEW

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
    
    # NEW: Add Curriculum Data
    print("\n" + "="*50)
    print("📚 CURRICULUM MODULE INITIALIZATION")
    print("="*50)
    
    # Add sample courses
    sample_courses = [
        Course("CS101", "Introduction to Programming", 3, "Computer Engineering", 
              "Basic programming concepts with Python", ["None"]),
        Course("CS201", "Data Structures", 4, "Computer Engineering", 
              "Advanced data structures and algorithms", ["CS101"]),
        Course("ME101", "Engineering Mechanics", 3, "Mechanical Engineering",
              "Basic mechanics principles and applications"),
        Course("EE201", "Circuit Analysis", 4, "Electrical Engineering",
              "Analysis of electrical circuits and systems")
    ]
    
    for course in sample_courses:
        try:
            course.is_core = True  # Mark as core courses
            curriculum_manager.add_course(course)
            print(f"Added course: {course.course_code} - {course.course_name}")
        except Exception as e:
            print(f"Course {course.course_code} already exists or error: {e}")
    
    # Enroll students in courses
    curriculum_manager.enroll_student("CS101", "001")  # Maria
    curriculum_manager.enroll_student("CS101", "002")  # Mark
    curriculum_manager.enroll_student("CS201", "001")  # Maria
    curriculum_manager.enroll_student("ME101", "002")  # Mark
    
    print("\nStudent enrollments:")
    print("  Maria (001) enrolled in: CS101, CS201")
    print("  Mark (002) enrolled in: CS101, ME101")
    
    # NEW: Create study plans
    student_planner.create_study_plan("001", "Fall 2024", ["CS101", "CS201"])
    student_planner.create_study_plan("002", "Fall 2024", ["CS101", "ME101"])
    print("\nCreated study plans for Fall 2024 semester")
    
    # NEW: Add LMS Data
    print("\n" + "="*50)
    print("🎓 LMS MODULE INITIALIZATION")
    print("="*50)
    
    # Add LMS content
    content = LMSContent(
        "CONT_001",
        "CS101",
        "Introduction to Python",
        ContentType.VIDEO,
        "https://example.com/python-intro",
        "Basic Python programming tutorial"
    )
    lms_manager.add_content(content)
    print(f"Added LMS content: {content.title}")
    
    # Create assignment
    assignment = Assignment(
        "ASSIGN_001",
        "CS101",
        "Python Basics Assignment",
        "Complete the following Python exercises",
        "2024-12-15",
        100,
        AssignmentType.HOMEWORK
    )
    lms_manager.create_assignment(assignment)
    print(f"Created assignment: {assignment.title}")
    
    # Student submits assignment
    assignment.submit_assignment("001", "My Python assignment submission")
    assignment.grade_assignment("001", 85, "Good work!")
    lms_manager.create_assignment(assignment)  # Save with submission
    
    print("Maria (001) submitted and graded assignment: 85/100")
    
    # Create quiz
    quiz = Quiz(
        "QUIZ_001",
        "CS101",
        "Python Fundamentals Quiz",
        [
            {"question": "What is Python?", "options": ["A snake", "A programming language", "A type of food", "A car"], "correct_answer": 1},
            {"question": "What symbol is used for comments?", "options": ["//", "#", "/*", "<!--"], "correct_answer": 1},
            {"question": "Which is a Python data type?", "options": ["int", "string", "list", "All of the above"], "correct_answer": 3}
        ]
    )
    lms_manager.create_quiz(quiz)
    print(f"Created quiz: {quiz.title}")
    
    # Student takes quiz
    quiz_score = quiz.take_quiz("001", [1, 1, 3])
    lms_manager.create_quiz(quiz)  # Save with attempt
    print(f"Maria (001) took quiz and scored: {quiz_score:.1f}%")
    
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
    
    print("\n" + "="*50 + "\n")
    
    print("--- 📚 Curriculum & LMS Demo ---")
    
    # 1. List all courses
    courses = curriculum_manager.list_courses()
    print(f"Total courses in catalogue: {len(courses)}")
    print("Sample courses:")
    for course in courses[:3]:  # Show first 3
        print(f"  • {course.course_code}: {course.course_name} ({course.credits} credits)")
    
    # 2. Show student study plans
    print("\nStudent study plans:")
    maria_plan = student_planner.get_study_plan("001")
    mark_plan = student_planner.get_study_plan("002")
    
    print("Maria's Fall 2024 plan:")
    for semester, course_list in maria_plan.items():
        print(f"  {semester}: {', '.join(course_list)}")
    
    print("Mark's Fall 2024 plan:")
    for semester, course_list in mark_plan.items():
        print(f"  {semester}: {', '.join(course_list)}")
    
    # 3. Show LMS content for CS101
    print("\nLMS Content for CS101:")
    cs101_content = lms_manager.get_course_content("CS101")
    for content in cs101_content:
        print(f"  • {content.title} ({content.content_type.value})")
    
    # 4. Show assignment submissions
    print("\nAssignment submissions for CS101:")
    cs101_assignment = lms_manager.get_assignment("ASSIGN_001")
    if cs101_assignment:
        for student_id, submission in cs101_assignment.submissions.items():
            print(f"  Student {student_id}: {submission.get('grade', 'Not graded')}/100")
    
    # 5. Show quiz results
    print("\nQuiz results for CS101:")
    cs101_quiz = lms_manager.get_quiz("QUIZ_001")
    if cs101_quiz and "001" in cs101_quiz.attempts:
        attempt = cs101_quiz.attempts["001"]
        print(f"  Student 001: {attempt['score']:.1f}%")
    
    print("\n" + "="*50)
    print("✅ COMPREHENSIVE DEMO COMPLETED SUCCESSFULLY!")
    print("="*50)


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
        print("   • 📚 Curriculum & Course Catalogue Management")
        print("   • 🎓 Learning Management System (LMS)")
        print("   • 📝 Student Study Planning")
        print("   • 📊 Gradebook & Feedback System")
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
        print("  - Curriculum_Manager.py")     # NEW
        print("  - LMS_Manager.py")           # NEW
        print("  - GUI.py")


def system_status_check():
    """Check if all required components are available"""
    print("\n🔍 Performing System Status Check...")
    
    required_files = [
        "Classroom_Manager.py",
        "equipment_management.py", 
        "Student_Manager.py",
        "Curriculum_Manager.py",   # NEW
        "LMS_Manager.py",         # NEW
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
    print("=" * 80)
    print("              COMPREHENSIVE UNIVERSITY MANAGEMENT SYSTEM v3.0")
    print("=" * 80)
    print("\nThis system integrates:")
    print("  • Student Information Management")
    print("  • Classroom Scheduling & Reservations") 
    print("  • Equipment & Laboratory Management")
    print("  • Software License Tracking")
    print("  • People Allocation System")
    print("  • 📚 Curriculum & Course Catalogue")
    print("  • 🎓 Learning Management System (LMS)")
    print("  • 📝 Student Study Planning & Progress Tracking")
    
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
        print("1. Run Comprehensive Console Demo (All Modules)")
        print("2. Launch Full-Featured GUI Application")
        print("3. System Information")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            print("STARTING COMPREHENSIVE CONSOLE DEMO...")
            print("="*50)
            print("This demo includes:")
            print("  • Classroom Management & Reservations")
            print("  • Equipment & License Management")
            print("  • Student Records System")
            print("  • 📚 Curriculum & Course Catalogue")
            print("  • 🎓 Learning Management System")
            print("  • 📝 Student Study Planning")
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
            print("Version: Comprehensive University Management System v3.0")
            print("\nFeatures:")
            print("  • 10-Tab GUI Interface with Real-time Updates")
            print("  • Student Records with File-based Storage")
            print("  • Classroom Reservation System with Conflict Detection")
            print("  • Equipment & Lab Equipment Allocation Tracking")
            print("  • Software License Seat Management")
            print("  • Professor & Student Department Allocation")
            print("  • Maintenance Reporting System")
            print("  • 📚 Course Catalogue Management")
            print("  • 🎓 Learning Management System (LMS)")
            print("  • 📝 Student Study Planning Tools")
            print("  • 📊 Gradebook & Feedback System")
            print("  • 💬 Student Feedback & Course Ratings")
            print("  • 📈 Interactive Dashboard with System Statistics")
            print("\nModules:")
            print("  - Classroom_Manager.py")
            print("  - equipment_management.py")
            print("  - Student_Manager.py")
            print("  - Curriculum_Manager.py")
            print("  - LMS_Manager.py")
            print("  - GUI.py")
            
        elif choice == "4":
            print("\nThank you for using the University Management System!")
            print("Goodbye! 👋")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")