# main_integration.py - COMPLETE UPDATED VERSION WITH DATABASE LOCK FIX
import os
from datetime import datetime, timedelta
import atexit
import signal
import sys

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
from Staff_Manager import StaffManager
from University_Controller import UniversityController

# Global variable to track active database connections
_active_connections = []

def cleanup_database_connections():
    """Force close all database connections before exit"""
    print("\n🔧 Cleaning up database connections...")
    for conn_info in _active_connections:
        try:
            if hasattr(conn_info, 'close'):
                conn_info.close()
                print(f"  Closed connection: {conn_info}")
        except:
            pass
    _active_connections.clear()

# Register cleanup handlers
atexit.register(cleanup_database_connections)

def signal_handler(signum, frame):
    """Handle termination signals"""
    cleanup_database_connections()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

# --- Console Demo Function ---
def setup_and_demo_system():
    """Initializes and demonstrates the integrated system via console output."""
    
    print("--- 📚 System Initialization (Console Demo) ---")
    
    # Initialize the Controller
    controller = UniversityController()

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
        
        # 2. Allocate Lab Equipment
        controller.lab_eq_mgr.allocate_lab_equipment("L001", "S001")
        print(f"Lab Equipment L001 (Microscope) allocated to S001.")

        # 3. Test Database License if available
        print("\n--- 💾 Database Integration Test ---")
        try:
            # Try to use database features
            test_student_data = {
                'student_id': 'TEST999',
                'first_name': 'Database',
                'last_name': 'Test',
                'department': 'Computer Science',
                'enrollment_year': 2024,
                'email': 'db.test@uni.edu'
            }
            
            result = controller.register_new_student(test_student_data)
            print(f"Database student registration: {result}")
            
            # Try to get student from database
            student_db = controller.get_student_from_db('TEST999')
            if student_db:
                print(f"Retrieved from DB: {student_db['first_name']} {student_db['last_name']}")
            
            # Clean up test student
            if hasattr(controller, 'database') and controller.database:
                cursor = controller.database.conn.cursor()
                cursor.execute("DELETE FROM students WHERE student_id = 'TEST999'")
                controller.database.conn.commit()
                print("Cleaned up test student")
            
        except Exception as db_error:
            print(f"Database features not available: {db_error}")
            
    except Exception as e:
        print(f"Error during Equipment/License Demo: {e}")

    print("\n--- 🧑‍🎓 Student, Staff & People Demo ---")
    try:
        # 1. Retrieve Student Record
        student_007 = controller.student_mgr.get_student("007")
        print("Retrieved Student 007:")
        if student_007:
            controller.student_mgr.print_student(student_007)
        else:
            print("Student 007 not found")

        # 2. Update Student's Allocation
        print("Assigning student 007 to 'Field Operations' department...")
        controller.person_mgr.assign_student("007", "Field Operations")
        
        # 3. Add a Professor and assign them
        prof_id = "P003"
        prof_name = "Dr. Alex Lee"
        prof_dept = "Electrical Engineering"
        controller.staff_mgr.add_professor(prof_id, prof_name, prof_dept, "alex.lee@uni.edu")
        print(f"Added Professor {prof_name} (ID: {prof_id}).")

        # Assign Professor to Course
        course_to_assign = "EE201"
        try:
            msg = controller.assign_professor_to_course(prof_id, course_to_assign)
            print(f"Assignment result: {msg}")
        except ValueError as e:
            print(f"Error assigning professor to course: {e}")

        # 4. Edit student record
        print("Editing Maria's (001) record...")
        controller.student_mgr.edit_student("001", {"email": "maria.newmail@uni.edu", "gpa": 2.5})
        updated_maria = controller.student_mgr.get_student("001")
        print("Updated Maria:")
        if updated_maria:
            controller.student_mgr.print_student(updated_maria)
        
        # 5. Delete a student using the Controller
        print("Deleting student 002 (Mark Magdy) using the Controller...")
        delete_message = controller.delete_student_fully("002")
        print(f"Deletion result: {delete_message}")
        
    except Exception as e:
        print(f"Error during Student/Staff/People Demo: {e}")

    print("\n--- 📚 Curriculum & LMS Demo ---")
    try:
        # 1. List all courses
        courses = controller.curriculum_mgr.list_courses()
        print(f"Total courses in catalogue: {len(courses)}")
        print("Sample courses:")
        for course in courses[:3]:
            print(f"  • {course.course_code}: {course.course_name} ({course.credits} credits)")
        
        # 2. Show student study plans
        print("\nStudent study plans:")
        maria_plan = controller.student_planner.get_study_plan("001")
        if maria_plan:
            print("Maria's plan:")
            for semester, course_list in maria_plan.items():
                print(f"  {semester}: {', '.join(course_list)}")
        
        # 3. Enroll student in a new course
        print("\nEnrolling student 001 in ME101...")
        try:
            msg = controller.enroll_student_in_course("001", "ME101")
            print(f"Enrollment result: {msg}")
        except ValueError as e:
            print(f"Enrollment failed: {e}")

    except Exception as e:
        print(f"Error during Curriculum/LMS Demo: {e}")
    
    # Clean up controller's database connection
    try:
        controller.cleanup()
    except:
        pass

    print("\n" + "="*50)
    print("✅ COMPREHENSIVE CONSOLE DEMO COMPLETED SUCCESSFULLY!")
    print("="*50)

# --- Database Demo Functions ---
def setup_and_demo_database():
    """Demonstrate the database functionality separately"""
    print("\n" + "="*60)
    print("DATABASE SYSTEM DEMO")
    print("="*60)
    
    try:
        from database_schema import demo_database, create_schema_diagram
        
        print("\n1. Creating schema diagram...")
        create_schema_diagram()
        
        print("\n2. Running database demo...")
        demo_database()
        
        print("\n✅ Database demo completed successfully!")
        print("\nThe database file 'university_demo.db' has been created.")
        print("You can explore it using SQLite Browser or command line.")
        
    except ImportError as e:
        print(f"❌ Database module not found: {e}")
        print("Please make sure 'database_schema.py' is in the same directory.")
    except Exception as e:
        print(f"❌ Error during database demo: {e}")

# --- Database Migration ---
def migrate_existing_data():
    """Migrate existing JSON data to database"""
    print("\n" + "="*60)
    print("DATA MIGRATION TO DATABASE")
    print("="*60)
    
    try:
        # Create controller with cleanup
        controller = UniversityController()
        
        # Check if database is available
        if not hasattr(controller, 'database') or controller.database is None:
            print("❌ Database not available. Please check database_schema.py")
            return
        
        # Perform full migration
        print("Migrating existing data to database...")
        try:
            # Manually sync data instead of using db_integration
            print("Syncing students...")
            students = controller.student_mgr.list_students()
            for student in students:
                try:
                    controller.database.add_student(student)
                except Exception as e:
                    print(f"  Warning: Could not add student {student.get('student_id')}: {e}")
            
            print("Syncing courses and enrollments...")
            courses = controller.curriculum_mgr.list_courses()
            for course in courses:
                # Add course to database
                course_data = {
                    'course_code': course.course_code,
                    'course_name': course.course_name,
                    'credits': course.credits,
                    'department': course.department,
                    'description': course.description,
                    'is_core': course.is_core,
                    'professor_id': course.professor_id
                }
                try:
                    controller.database.add_course(course_data)
                except Exception as e:
                    print(f"  Warning: Could not add course {course.course_code}: {e}")
                
                # Add enrollments
                for student_id in course.students_enrolled:
                    try:
                        controller.database.enroll_student_in_course(student_id, course.course_code)
                    except Exception as e:
                        print(f"  Warning: Could not enroll {student_id} in {course.course_code}: {e}")
            
            print("Syncing classrooms...")
            for classroom in controller.scheduler.classrooms:
                cursor = controller.database.conn.cursor()
                cursor.execute('''
                INSERT OR REPLACE INTO classrooms (classroom_id, capacity, location, is_under_maintenance)
                VALUES (?, ?, ?, ?)
                ''', (
                    classroom.id,
                    classroom.capacity,
                    classroom.location,
                    classroom.is_under_maintenance
                ))
            
            controller.database.conn.commit()
            print("\n✅ Migration completed successfully!")
            print("All your existing data is now in the SQLite database.")
            print("Database file: university_system.db")
            
        except Exception as sync_error:
            print(f"❌ Error during sync: {sync_error}")
        
        # Clean up
        controller.cleanup()
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")

# --- GUI Launcher Function ---
def launch_comprehensive_gui():
    """Launch the comprehensive GUI application"""
    controller = None
    
    try:
        import tkinter as tk
        
        print("🚀 Launching Comprehensive University Management System GUI...")
        print("Please wait while the GUI initializes...")
        
        # Create controller
        controller = UniversityController()
        
        # Import after controller creation to avoid circular imports
        try:
            from GUI import UniversityManagementGUI
        except ImportError as e:
            print(f"❌ Error importing GUI module: {e}")
            if controller:
                controller.cleanup()
            return
        
        root = tk.Tk()
        app = UniversityManagementGUI(root)
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
        print("   • 💾 Database Management & EAV System")
        print("   • Real-time Dashboard")
        
        # Set up cleanup when window closes
        def on_closing():
            print("\n🔧 Closing GUI and cleaning up resources...")
            try:
                if controller:
                    controller.cleanup()
            except Exception as e:
                print(f"Warning during cleanup: {e}")
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error: Could not import GUI module. Make sure GUI.py and all related files are in the same directory.")
        print(f"Detailed error: {e}")
        if controller:
            controller.cleanup()
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        if controller:
            controller.cleanup()

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
        "Staff_Manager.py",
        "University_Controller.py",
        "GUI.py"
    ]
    
    optional_files = [
        "database_schema.py"
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_ok = False
    
    print("\nOptional files:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"⚠️  {file} - Missing (database features will be disabled)")
    
    if all_ok:
        print("\n✅ All required system components are ready!")
    else:
        print("\n❌ Some required components are missing. Please check the files above.")
    
    return all_ok

# --- Database Connection Test ---
def test_database_connection():
    """Test database connectivity"""
    print("\n🔍 Testing database connection...")
    try:
        import sqlite3
        
        # Test multiple connection approach
        test_conn = sqlite3.connect("test_connection.db", timeout=10.0)
        cursor = test_conn.cursor()
        
        # Create test table
        cursor.execute("CREATE TABLE IF NOT EXISTS test_connection (id INTEGER PRIMARY KEY, timestamp TEXT)")
        
        # Insert test data
        cursor.execute("INSERT INTO test_connection (timestamp) VALUES (datetime('now'))")
        test_conn.commit()
        
        # Query test data
        cursor.execute("SELECT * FROM test_connection ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        
        test_conn.close()
        
        # Clean up test file
        try:
            os.remove("test_connection.db")
        except:
            pass
            
        print("✅ Database connection test passed")
        print(f"  Last test record: {result}")
        return True
        
    except sqlite3.OperationalError as e:
        print(f"❌ Database locked error: {e}")
        print("  Suggestion: Close any other instances of the program")
        return False
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    # Display welcome message
    print("=" * 80)
    print("              COMPREHENSIVE UNIVERSITY MANAGEMENT SYSTEM v5.0")
    print("              WITH DATABASE INTEGRATION & EAV SYSTEM")
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
    print("  • 💾 SQLite Database with EAV (Entity-Attribute-Value) System")
    print("  • 📈 Real-time Dashboard")
    
    # Check system status
    system_ready = system_status_check()
    
    if not system_ready:
        print("\n⚠️  Please ensure all required .py files are in the same directory and try again.")
        exit(1)
    
    # Test database connection first
    if not test_database_connection():
        print("\n⚠️  Database connection test failed. Some features may not work.")
        print("   Try closing any other instances of this program.")
    
    # Main menu
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Run Comprehensive Console Demo (All Modules)")
        print("2. Launch Full-Featured GUI Application")
        print("3. Database Operations")
        print("4. System Information")
        print("5. Cleanup & Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n" + "="*50)
            print("STARTING COMPREHENSIVE CONSOLE DEMO...")
            print("="*50)
            setup_and_demo_system()
            
        elif choice == "2":
            print("\n" + "="*50)
            print("LAUNCHING COMPREHENSIVE GUI...")
            print("="*50)
            launch_comprehensive_gui()
            print("\nGUI session ended. Returning to main menu...")
            
        elif choice == "3":
            print("\n" + "="*50)
            print("DATABASE OPERATIONS")
            print("="*50)
            print("1. Demo Database Features")
            print("2. Migrate Existing Data to Database")
            print("3. View Database Schema")
            print("4. Test Database Integration")
            print("5. Back to Main Menu")
            
            db_choice = input("\nEnter choice (1-5): ").strip()
            
            if db_choice == "1":
                setup_and_demo_database()
            elif db_choice == "2":
                migrate_existing_data()
            elif db_choice == "3":
                try:
                    from database_schema import create_schema_diagram
                    create_schema_diagram()
                except ImportError:
                    print("❌ database_schema.py not found")
            elif db_choice == "4":
                test_database_connection()
            elif db_choice == "5":
                continue
            else:
                print("Invalid choice.")
                
        elif choice == "4":
            print("\n" + "="*50)
            print("SYSTEM INFORMATION")
            print("="*50)
            print("Version: Comprehensive University Management System v5.0")
            print("With Database Integration & EAV System")
            print("\nKey Features:")
            print("  • Dual Persistence (JSON + SQLite Database)")
            print("  • EAV System for Flexible Data (Licenses, Announcements)")
            print("  • Automatic Data Synchronization")
            print("  • 11-Tab GUI Interface with Database Tab")
            print("  • Comprehensive Reporting System")
            
            print("\nDatabase Features:")
            print("  • Traditional Tables for Structured Data")
            print("  • EAV Tables for Dynamic Data")
            print("  • Foreign Key Constraints for Data Integrity")
            print("  • Advanced Query Capabilities")
            print("  • Migration from JSON to Database")
            
        elif choice == "5":
            print("\n🔧 Performing system cleanup...")
            cleanup_database_connections()
            
            # Clean up any remaining .db files
            try:
                for db_file in ["test_connection.db", "test_integration.db"]:
                    if os.path.exists(db_file):
                        os.remove(db_file)
                        print(f"  Removed temporary file: {db_file}")
            except:
                pass
                
            print("\nThank you for using the University Management System!")
            print("Goodbye! 👋")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")