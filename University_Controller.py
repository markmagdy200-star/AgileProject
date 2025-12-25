# University_Controller.py - FIXED VERSION WITH DATABASE LOCK FIX
from Student_Manager import StudentManager
from Curriculum_Manager import CurriculumManager
from LMS_Manager import LMSManager
from Classroom_Manager import Scheduler, Classroom
from equipment_management import EquipmentManager, LicenseManager, PersonAllocationManager, LaboratoryEquipmentManager, SoftwareLicense
from Staff_Manager import StaffManager
from datetime import datetime
import sqlite3
import atexit

# Check if database module is available
try:
    from database_schema import UniversityDatabase, DatabaseIntegration
    DATABASE_AVAILABLE = True
except ImportError:
    print("Database module not found. Running in legacy mode.")
    DATABASE_AVAILABLE = False

class UniversityController:
    def __init__(self):
        # Initialize all individual managers
        self.student_mgr = StudentManager()
        self.curriculum_mgr = CurriculumManager()
        self.lms_mgr = LMSManager()
        self.scheduler = Scheduler()
        self.equipment_mgr = EquipmentManager()
        self.license_mgr = LicenseManager()
        self.person_mgr = PersonAllocationManager()
        self.lab_eq_mgr = LaboratoryEquipmentManager()
        self.staff_mgr = StaffManager()

        # Initialize StudentPlanner
        from Curriculum_Manager import StudentPlanner
        self.student_planner = StudentPlanner()
        
        # Store database availability as instance variable
        self.database_available = DATABASE_AVAILABLE
        self.database = None
        self.db_integration = None
        
        # Register cleanup on exit
        atexit.register(self.cleanup)
        
        if self.database_available:
            try:
                # Use timeout to handle concurrent access
                self.database = UniversityDatabase("university_system.db")
                self.db_integration = DatabaseIntegration(self)
                print("Database initialized successfully")
                
                # Auto-sync existing data
                self.auto_sync_to_database()
            except sqlite3.OperationalError as e:
                if "locked" in str(e):
                    print(f"⚠️ Database is locked by another process. Running in read-only mode.")
                    print(f"  Try closing other instances or use: main_integration.py")
                    self.database_available = False
                else:
                    print(f"Database initialization error: {e}. Running in legacy mode.")
                    self.database_available = False
            except Exception as e:
                print(f"Database initialization error: {e}. Running in legacy mode.")
                self.database_available = False
        else:
            print("Running without database integration")

    def cleanup(self):
        """Clean up database connections before exit"""
        if hasattr(self, 'database') and self.database:
            try:
                self.database.close()
                self.database = None
            except Exception as e:
                print(f"Warning: Error closing database: {e}")
        
        # Also try to close any open connections in integration
        if hasattr(self, 'db_integration') and self.db_integration:
            try:
                if hasattr(self.db_integration.db, 'close'):
                    self.db_integration.db.close()
            except:
                pass

    def auto_sync_to_database(self):
        """Automatically sync existing data to database on startup"""
        if not self.database_available or not self.db_integration:
            return
            
        try:
            print("Syncing existing data to database...")
            # Use try-except for each sync operation
            try:
                self.db_integration.sync_student_data()
            except Exception as e:
                print(f"Auto-sync warning: {e}")
                
            try:
                self.db_integration.sync_course_enrollments()
            except Exception as e:
                print(f"Auto-sync warning: {e}")
                
            try:
                self.db_integration.sync_classroom_reservations()
            except Exception as e:
                print(f"Auto-sync warning: {e}")
                
        except Exception as e:
            print(f"Auto-sync error: {e}")
            # Don't crash if sync fails, just continue

    # --- MODIFIED METHODS FOR DATABASE INTEGRATION ---
    
    def register_new_student(self, student_data):
        """Adds student to StudentManager AND Database"""
        if self.student_mgr.student_exists(student_data.get("student_id")):
            raise ValueError("Student ID already exists.")
        
        # 1. Add to StudentManager
        self.student_mgr.add_student(student_data)
        
        # 2. Add to Database (if available)
        if self.database_available and self.database:
            try:
                self.database.add_student(student_data)
                return f"Student {student_data['student_id']} registered successfully in both systems."
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e) and "email" in str(e):
                    # Email constraint violation - common with sample data
                    print(f"Warning: Email already exists in database for student {student_data['student_id']}")
                    return f"Student {student_data['student_id']} registered (email already in use in DB)"
                else:
                    print(f"Failed to add student to database: {e}")
                    return f"Student {student_data['student_id']} registered (database error: {e})"
            except Exception as e:
                print(f"Failed to add student to database: {e}")
                return f"Student {student_data['student_id']} registered (database error: {e})"
        
        return f"Student {student_data['student_id']} registered successfully."

    def delete_student_fully(self, student_id):
        """Removes student from Records AND Database"""
        # 1. Check existence
        if not self.student_mgr.student_exists(student_id):
            return "Student not found."

        # 2. Delete from Database FIRST (if available)
        if self.database_available and self.database:
            try:
                cursor = self.database.conn.cursor()
                cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                self.database.conn.commit()
            except Exception as e:
                print(f"Failed to delete student from database: {e}")

        # 3. Get enrolled courses to unenroll
        courses_enrolled = self.curriculum_mgr.get_student_courses(student_id)
        for course in courses_enrolled:
            try:
                self.curriculum_mgr.unenroll_student(course.course_code, student_id)
            except Exception as e:
                print(f"Warning: Could not unenroll student {student_id} from {course.course_code}: {e}")

        # 4. Delete Basic Record
        deleted = self.student_mgr.delete_student(student_id)
        
        # 5. Remove from Student Planner
        if student_id in self.student_planner.student_plans:
            del self.student_planner.student_plans[student_id]
            self.student_planner.save_plans()

        if deleted:
            return f"Student {student_id} removed from all systems."
        else:
            return "Student record found but could not be deleted."

    def enroll_student_in_course(self, student_id, course_code):
        """Checks if student and course exist before enrolling - WITH DATABASE"""
        # 1. Validation
        if not self.student_mgr.student_exists(student_id):
            raise ValueError(f"Student with ID {student_id} does not exist in records.")
        
        course = self.curriculum_mgr.get_course(course_code)
        if not course:
            raise ValueError(f"Course with code {course_code} does not exist.")

        # 2. Enroll in Curriculum Manager
        try:
            self.curriculum_mgr.enroll_student(course_code, student_id)
        except ValueError as e:
            raise e

        # 3. Enroll in Database (if available)
        if self.database_available and self.database:
            try:
                success = self.database.enroll_student_in_course(student_id, course_code)
                if not success:
                    print(f"Info: Student {student_id} already enrolled in {course_code} in database")
            except Exception as e:
                print(f"Failed to enroll in database: {e}")

        # 4. Ensure Gradebook exists
        gb = self.lms_mgr.get_gradebook(course_code)
        self.lms_mgr.save_gradebook(gb)
        
        return f"Student {student_id} successfully enrolled in {course_code}."

    def assign_professor_to_course(self, prof_id, course_code):
        """Links Staff Manager and Curriculum Manager - WITH DATABASE"""
        # 1. Check Prof exists
        if not self.staff_mgr.get_professor(prof_id):
            raise ValueError(f"Professor with ID {prof_id} not found.")
        
        # 2. Check Course exists
        course = self.curriculum_mgr.get_course(course_code)
        if not course:
            raise ValueError(f"Course with code {course_code} not found.")
        
        # 3. Update Curriculum Manager
        try:
            self.curriculum_mgr.assign_professor(course_code, prof_id)
        except ValueError as e:
            raise e
        
        # 4. Update Staff Manager
        try:
            msg = self.staff_mgr.assign_course_to_prof(prof_id, course_code)
        except ValueError as e:
            raise ValueError(f"Failed to assign course in Staff Manager: {e}")
        
        # 5. Update Database (if available)
        if self.database_available and self.database:
            try:
                cursor = self.database.conn.cursor()
                cursor.execute(
                    "UPDATE courses SET professor_id = ? WHERE course_code = ?",
                    (prof_id, course_code)
                )
                self.database.conn.commit()
            except Exception as e:
                print(f"Failed to update database: {e}")
        
        return f"Professor {prof_id} assigned to {course_code}."

    def schedule_class_session(self, course_code, room_id, start_time_str, end_time_str):
        """Schedules a room for a specific course - WITH DATABASE"""
        # 1. Validate Course
        course = self.curriculum_mgr.get_course(course_code)
        if not course:
            raise ValueError("Invalid Course Code")

        # 2. Parse datetime strings
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            raise ValueError("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS or ISO format.")
        
        # 3. Validate Room & Reserve in Scheduler
        reserved_by = f"Course: {course_code}"
        result = self.scheduler.reserve_classroom(room_id, start_time, end_time, reserved_by)
        
        # 4. Add to Database (if available)
        if self.database_available and self.database:
            try:
                reservation_data = {
                    'classroom_id': room_id,
                    'reserved_by': reserved_by,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'purpose': f"Class session for {course_code}"
                }
                self.database.create_reservation(reservation_data)
            except Exception as e:
                print(f"Failed to add reservation to database: {e}")
        
        return result

    # --- NEW DATABASE QUERY METHODS ---
    
    def get_student_from_db(self, student_id):
        """Get student from database"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        cursor = self.database.conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        return dict(student) if student else None
    
    def get_all_students_from_db(self):
        """Get all students from database"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        cursor = self.database.conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY student_id")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_course_details_from_db(self, course_code):
        """Get course with professor info from database"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        cursor = self.database.conn.cursor()
        cursor.execute('''
        SELECT c.*, p.name as professor_name, p.email as professor_email
        FROM courses c
        LEFT JOIN professors p ON c.professor_id = p.professor_id
        WHERE c.course_code = ?
        ''', (course_code,))
        course = cursor.fetchone()
        return dict(course) if course else None
    
    def generate_enrollment_report_db(self):
        """Generate enrollment report from database"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        return self.database.generate_enrollment_report()
    
    def generate_maintenance_report_db(self):
        """Generate maintenance report from database"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        return self.database.generate_maintenance_report()
    
    # --- EAV METHODS FOR LICENSES AND ANNOUNCEMENTS ---
    
    def create_software_license(self, license_id, name, total_seats):
        """Create software license using EAV system"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        entity_id = self.database.create_license_entity(license_id, name, total_seats)
        
        # Also add to LicenseManager for backward compatibility
        self.license_mgr.add_license(SoftwareLicense(license_id, name, total_seats))
        
        return f"License {name} created with {total_seats} seats (Entity ID: {entity_id})"
    
    def create_announcement(self, title, content, target_type, target_value):
        """Create announcement using EAV system"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        entity_id = self.database.create_announcement_entity(
            title, content, target_type, target_value
        )
        return f"Announcement '{title}' created (Entity ID: {entity_id})"
    
    def get_all_announcements(self):
        """Get all announcements from EAV system"""
        if not self.database_available or not self.database:
            raise ValueError("Database not available")
        
        return self.database.get_entities_by_type('announcement')
    
    def close_database(self):
        """Close database connection properly - legacy method, use cleanup() instead"""
        self.cleanup()
    
    # --- UTILITY METHODS ---
    
    def is_database_available(self):
        """Check if database is available"""
        return self.database_available and self.database is not None
    
    def get_database_status(self):
        """Get database connection status"""
        if not self.database_available:
            return "Database module not available"
        if not self.database:
            return "Database not initialized"
        
        try:
            cursor = self.database.conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return "Connected and working"
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                return f"Database locked by another process"
            return f"Database error: {e}"
        except Exception as e:
            return f"Database error: {e}"
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except:
            pass

# Optional: Test function
def test_controller():
    """Test the controller functionality"""
    print("Testing University Controller...")
    controller = UniversityController()
    
    print(f"Database available: {controller.database_available}")
    print(f"Database status: {controller.get_database_status()}")
    
    # Test student operations
    try:
        students = controller.student_mgr.list_students()
        print(f"Found {len(students)} students in manager")
        
        if controller.database_available:
            db_students = controller.get_all_students_from_db()
            print(f"Found {len(db_students)} students in database")
    except Exception as e:
        print(f"Test error: {e}")
    
    controller.cleanup()
    print("Test completed.")

if __name__ == "__main__":
    test_controller()