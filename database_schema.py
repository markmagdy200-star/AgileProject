# database_schema.py - FIXED VERSION WITH CONNECTION MANAGEMENT
import sqlite3
from datetime import datetime
import threading

class UniversityDatabase:
    def __init__(self, db_path="university.db", timeout=10.0):
        self.db_path = db_path
        self.timeout = timeout
        self.conn = None
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to SQLite database with timeout"""
        with self._lock:
            if self.conn:
                try:
                    self.conn.close()
                except:
                    pass
            
            try:
                # Add timeout and check_same_thread=False for thread safety
                self.conn = sqlite3.connect(
                    self.db_path, 
                    timeout=self.timeout,
                    check_same_thread=False
                )
                self.conn.row_factory = sqlite3.Row  # Enable dictionary-like access
                # Enable foreign keys
                self.conn.execute("PRAGMA foreign_keys = ON")
                # Set busy timeout
                self.conn.execute(f"PRAGMA busy_timeout = {int(self.timeout * 1000)}")
                return True
            except Exception as e:
                print(f"Failed to connect to database {self.db_path}: {e}")
                self.conn = None
                return False
    
    def get_connection(self):
        """Get a database connection, reconnect if needed"""
        with self._lock:
            if not self.conn:
                self.connect()
            return self.conn
    
    def execute_with_retry(self, query, params=(), max_retries=3):
        """Execute query with retry on lock"""
        with self._lock:
            for attempt in range(max_retries):
                try:
                    conn = self.get_connection()
                    if not conn:
                        raise sqlite3.OperationalError("No database connection")
                    
                    cursor = conn.cursor()
                    cursor.execute(query, params)
                    return cursor
                except sqlite3.OperationalError as e:
                    if "locked" in str(e) and attempt < max_retries - 1:
                        print(f"Database locked, retry {attempt + 1}/{max_retries}...")
                        import time
                        time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                        continue
                    raise
                except Exception as e:
                    raise
    
    def commit(self):
        """Commit transaction safely"""
        with self._lock:
            if self.conn:
                try:
                    self.conn.commit()
                except Exception as e:
                    print(f"Commit error: {e}")
    
    def rollback(self):
        """Rollback transaction safely"""
        with self._lock:
            if self.conn:
                try:
                    self.conn.rollback()
                except:
                    pass
    
    def create_tables(self):
        """Create all database tables"""
        with self._lock:
            try:
                cursor = self.get_connection().cursor()
                
                # =====================
                # 1. TRADITIONAL TABLES
                # =====================
                
                # Students table (traditional)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    department TEXT,
                    enrollment_year INTEGER,
                    gpa REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'enrolled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Staff/Professors table (traditional)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS professors (
                    professor_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    email TEXT,
                    hire_date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Courses table (traditional)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_code TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    department TEXT NOT NULL,
                    description TEXT,
                    is_core BOOLEAN DEFAULT 0,
                    professor_id TEXT,
                    semester_offered TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
                )
                ''')
                
                # Classrooms table (traditional)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS classrooms (
                    classroom_id TEXT PRIMARY KEY,
                    capacity INTEGER NOT NULL,
                    location TEXT,
                    is_under_maintenance BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Equipment table (traditional)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipment (
                    equipment_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    is_allocated BOOLEAN DEFAULT 0,
                    allocated_to TEXT,
                    allocation_date TIMESTAMP,
                    is_lab_equipment BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # =====================
                # 2. EAV TABLES (FLEXIBLE)
                # =====================
                
                # Entities table (EAV - for flexible entity storage)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS entities (
                    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,  -- e.g., 'license', 'announcement', 'feedback'
                    name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Properties table (EAV - flexible attributes)
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id INTEGER NOT NULL,
                    attribute TEXT NOT NULL,
                    value TEXT,
                    data_type TEXT DEFAULT 'text',  -- text, integer, real, boolean, json
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
                )
                ''')
                
                # =====================
                # 3. RELATIONSHIP TABLES
                # =====================
                
                # Student-Course Enrollment
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_courses (
                    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    course_code TEXT NOT NULL,
                    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    grade REAL,
                    status TEXT DEFAULT 'enrolled',
                    UNIQUE(student_id, course_code),
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
                )
                ''')
                
                # Reservations
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classroom_id TEXT NOT NULL,
                    reserved_by TEXT,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP NOT NULL,
                    purpose TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE CASCADE
                )
                ''')
                
                # Maintenance Reports
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classroom_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    reported_by TEXT,
                    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved BOOLEAN DEFAULT 0,
                    resolved_at TIMESTAMP,
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE CASCADE
                )
                ''')
                
                # Student Study Plans
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_plans (
                    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    semester TEXT NOT NULL,
                    course_code TEXT NOT NULL,
                    planned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(student_id, semester, course_code),
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
                )
                ''')
                
                # Assignments
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS assignments (
                    assignment_id TEXT PRIMARY KEY,
                    course_code TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT NOT NULL,
                    max_points REAL NOT NULL,
                    assignment_type TEXT DEFAULT 'homework',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_code) REFERENCES courses(course_code) ON DELETE CASCADE
                )
                ''')
                
                # Submissions
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS submissions (
                    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    submission_text TEXT,
                    submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    grade REAL,
                    feedback TEXT,
                    UNIQUE(assignment_id, student_id),
                    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
                ''')
                
                self.commit()
                return True
            except Exception as e:
                print(f"Error creating tables: {e}")
                self.rollback()
                return False
    
    # =====================
    # EAV METHODS
    # =====================
    
    def create_entity(self, entity_type, name=None):
        """Create a new entity in EAV system"""
        try:
            cursor = self.execute_with_retry(
                "INSERT INTO entities (entity_type, name) VALUES (?, ?)",
                (entity_type, name)
            )
            entity_id = cursor.lastrowid
            self.commit()
            return entity_id
        except Exception as e:
            print(f"Error creating entity: {e}")
            self.rollback()
            return None
    
    def set_property(self, entity_id, attribute, value, data_type='text'):
        """Set a property for an entity"""
        try:
            # Check if property exists
            cursor = self.execute_with_retry(
                "SELECT property_id FROM properties WHERE entity_id=? AND attribute=?",
                (entity_id, attribute)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing
                self.execute_with_retry(
                    "UPDATE properties SET value=?, data_type=? WHERE property_id=?",
                    (str(value), data_type, existing['property_id'])
                )
            else:
                # Insert new
                self.execute_with_retry(
                    "INSERT INTO properties (entity_id, attribute, value, data_type) VALUES (?, ?, ?, ?)",
                    (entity_id, attribute, str(value), data_type)
                )
            
            self.commit()
            return True
        except Exception as e:
            print(f"Error setting property: {e}")
            self.rollback()
            return False
    
    def get_property(self, entity_id, attribute):
        """Get a property value"""
        try:
            cursor = self.execute_with_retry(
                "SELECT value, data_type FROM properties WHERE entity_id=? AND attribute=?",
                (entity_id, attribute)
            )
            result = cursor.fetchone()
            
            if result:
                # Convert value based on data type
                if result['data_type'] == 'integer':
                    return int(result['value'])
                elif result['data_type'] == 'real':
                    return float(result['value'])
                elif result['data_type'] == 'boolean':
                    return result['value'].lower() == 'true'
                elif result['data_type'] == 'json':
                    import json
                    return json.loads(result['value'])
                else:
                    return result['value']
            return None
        except Exception as e:
            print(f"Error getting property: {e}")
            return None
    
    def get_all_properties(self, entity_id):
        """Get all properties for an entity as dictionary"""
        try:
            cursor = self.execute_with_retry(
                "SELECT attribute, value, data_type FROM properties WHERE entity_id=?",
                (entity_id,)
            )
            properties = {}
            for row in cursor.fetchall():
                # Convert based on data type
                value = row['value']
                if row['data_type'] == 'integer':
                    value = int(value)
                elif row['data_type'] == 'real':
                    value = float(value)
                elif row['data_type'] == 'boolean':
                    value = value.lower() == 'true'
                elif row['data_type'] == 'json':
                    import json
                    value = json.loads(value)
                
                properties[row['attribute']] = value
            return properties
        except Exception as e:
            print(f"Error getting properties: {e}")
            return {}
    
    def get_entities_by_type(self, entity_type):
        """Get all entities of a specific type with their properties"""
        try:
            cursor = self.execute_with_retry(
                "SELECT entity_id, name FROM entities WHERE entity_type=?",
                (entity_type,)
            )
            
            entities = []
            for row in cursor.fetchall():
                entity = dict(row)
                entity['properties'] = self.get_all_properties(row['entity_id'])
                entities.append(entity)
            
            return entities
        except Exception as e:
            print(f"Error getting entities: {e}")
            return []
    
    # =====================
    # EXAMPLE: Using EAV for Licenses
    # =====================
    
    def create_license_entity(self, license_id, name, total_seats):
        """Create a license using EAV"""
        entity_id = self.create_entity('license', f"License_{license_id}")
        
        if entity_id:
            self.set_property(entity_id, 'license_id', license_id)
            self.set_property(entity_id, 'name', name)
            self.set_property(entity_id, 'total_seats', total_seats, 'integer')
            self.set_property(entity_id, 'used_seats', 0, 'integer')
            self.set_property(entity_id, 'available_seats', total_seats, 'integer')
        
        return entity_id
    
    def allocate_license_seat(self, license_entity_id):
        """Allocate a license seat"""
        used_seats = self.get_property(license_entity_id, 'used_seats') or 0
        total_seats = self.get_property(license_entity_id, 'total_seats')
        
        if used_seats < total_seats:
            self.set_property(license_entity_id, 'used_seats', used_seats + 1, 'integer')
            self.set_property(license_entity_id, 'available_seats', total_seats - (used_seats + 1), 'integer')
            return True
        return False
    
    # =====================
    # EXAMPLE: Using EAV for Announcements
    # =====================
    
    def create_announcement_entity(self, title, content, target_type, target_value):
        """Create an announcement using EAV"""
        entity_id = self.create_entity('announcement', title)
        
        if entity_id:
            self.set_property(entity_id, 'title', title)
            self.set_property(entity_id, 'content', content)
            self.set_property(entity_id, 'target_type', target_type)
            self.set_property(entity_id, 'target_value', target_value)
            self.set_property(entity_id, 'created_by', 'system')
            self.set_property(entity_id, 'created_at', datetime.now().isoformat())
            self.set_property(entity_id, 'is_active', True, 'boolean')
        
        return entity_id
    
    # =====================
    # TRADITIONAL METHODS
    # =====================
    
    def add_student(self, student_data):
        """Add a student (traditional)"""
        try:
            cursor = self.execute_with_retry('''
            INSERT OR REPLACE INTO students 
            (student_id, first_name, last_name, email, department, enrollment_year, gpa, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_data['student_id'],
                student_data['first_name'],
                student_data['last_name'],
                student_data.get('email'),
                student_data.get('department'),
                student_data.get('enrollment_year'),
                student_data.get('gpa', 0.0),
                student_data.get('status', 'enrolled')
            ))
            self.commit()
            return student_data['student_id']
        except Exception as e:
            print(f"Error adding student: {e}")
            self.rollback()
            raise
    
    def add_professor(self, professor_data):
        """Add a professor (traditional)"""
        try:
            cursor = self.execute_with_retry('''
            INSERT OR REPLACE INTO professors 
            (professor_id, name, department, email, hire_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                professor_data['professor_id'],
                professor_data['name'],
                professor_data['department'],
                professor_data.get('email'),
                professor_data.get('hire_date')
            ))
            self.commit()
            return professor_data['professor_id']
        except Exception as e:
            print(f"Error adding professor: {e}")
            self.rollback()
            raise
    
    def add_course(self, course_data):
        """Add a course (traditional) - FIXED to handle missing professors"""
        try:
            # Check if professor exists
            prof_id = course_data.get('professor_id')
            if prof_id:
                cursor = self.execute_with_retry(
                    "SELECT professor_id FROM professors WHERE professor_id = ?",
                    (prof_id,)
                )
                if not cursor.fetchone():
                    # Professor doesn't exist, set to NULL
                    prof_id = None
            
            cursor = self.execute_with_retry('''
            INSERT OR REPLACE INTO courses 
            (course_code, course_name, credits, department, description, is_core, professor_id, semester_offered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_data['course_code'],
                course_data['course_name'],
                course_data['credits'],
                course_data['department'],
                course_data.get('description', ''),
                course_data.get('is_core', False),
                prof_id,  # Will be NULL if professor doesn't exist
                course_data.get('semester_offered', 'Fall 2024')
            ))
            self.commit()
            return course_data['course_code']
        except Exception as e:
            print(f"Error adding course: {e}")
            self.rollback()
            raise
    def enroll_student_in_course(self, student_id, course_code):
        """Enroll student in course"""
        try:
            cursor = self.execute_with_retry('''
            INSERT OR IGNORE INTO student_courses (student_id, course_code)
            VALUES (?, ?)
            ''', (student_id, course_code))
            self.commit()
            return cursor.rowcount > 0  # Returns True if row was inserted
        except Exception as e:
            print(f"Error enrolling student: {e}")
            self.rollback()
            return False
    
    def create_reservation(self, reservation_data):
        """Create a classroom reservation"""
        try:
            cursor = self.execute_with_retry('''
            INSERT INTO reservations 
            (classroom_id, reserved_by, start_time, end_time, purpose)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                reservation_data['classroom_id'],
                reservation_data.get('reserved_by'),
                reservation_data['start_time'],
                reservation_data['end_time'],
                reservation_data.get('purpose')
            ))
            self.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating reservation: {e}")
            self.rollback()
            raise
    
    def add_assignment(self, assignment_data):
        """Add an assignment"""
        try:
            cursor = self.execute_with_retry('''
            INSERT INTO assignments 
            (assignment_id, course_code, title, description, due_date, max_points, assignment_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                assignment_data['assignment_id'],
                assignment_data['course_code'],
                assignment_data['title'],
                assignment_data.get('description'),
                assignment_data['due_date'],
                assignment_data['max_points'],
                assignment_data.get('assignment_type', 'homework')
            ))
            self.commit()
        except Exception as e:
            print(f"Error adding assignment: {e}")
            self.rollback()
            raise
    
    # =====================
    # QUERY METHODS
    # =====================
    
    def get_student_courses(self, student_id):
        """Get all courses for a student"""
        try:
            cursor = self.execute_with_retry('''
            SELECT c.*, sc.grade, sc.status 
            FROM courses c
            JOIN student_courses sc ON c.course_code = sc.course_code
            WHERE sc.student_id = ?
            ''', (student_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting student courses: {e}")
            return []
    
    def get_course_students(self, course_code):
        """Get all students in a course"""
        try:
            cursor = self.execute_with_retry('''
            SELECT s.*, sc.grade, sc.status 
            FROM students s
            JOIN student_courses sc ON s.student_id = sc.student_id
            WHERE sc.course_code = ?
            ''', (course_code,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting course students: {e}")
            return []
    
    def get_available_classrooms(self, start_time, end_time):
        """Get classrooms not reserved during a time period"""
        try:
            cursor = self.execute_with_retry('''
            SELECT * FROM classrooms 
            WHERE classroom_id NOT IN (
                SELECT classroom_id FROM reservations 
                WHERE NOT (end_time <= ? OR start_time >= ?)
            )
            AND is_under_maintenance = 0
            ''', (start_time, end_time))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting available classrooms: {e}")
            return []
    
    def get_student_grades(self, student_id):
        """Get all grades for a student"""
        try:
            cursor = self.execute_with_retry('''
            SELECT c.course_code, c.course_name, sc.grade, sc.status
            FROM student_courses sc
            JOIN courses c ON sc.course_code = c.course_code
            WHERE sc.student_id = ?
            ''', (student_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting student grades: {e}")
            return []
    
    def get_assignment_submissions(self, assignment_id):
        """Get all submissions for an assignment"""
        try:
            cursor = self.execute_with_retry('''
            SELECT s.*, st.first_name, st.last_name
            FROM submissions s
            JOIN students st ON s.student_id = st.student_id
            WHERE s.assignment_id = ?
            ORDER BY s.submitted_date
            ''', (assignment_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting assignment submissions: {e}")
            return []
    
    # =====================
    # REPORTING METHODS
    # =====================
    
    def generate_enrollment_report(self):
        """Generate enrollment statistics"""
        try:
            cursor = self.execute_with_retry("SELECT COUNT(*) FROM students WHERE status='enrolled'")
            total_students = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM courses")
            total_courses = cursor.fetchone()[0]
            
            cursor.execute('''
            SELECT department, COUNT(*) as student_count 
            FROM students 
            WHERE status='enrolled'
            GROUP BY department
            ''')
            dept_stats = cursor.fetchall()
            
            return {
                'total_students': total_students,
                'total_courses': total_courses,
                'department_stats': [dict(row) for row in dept_stats]
            }
        except Exception as e:
            print(f"Error generating enrollment report: {e}")
            return {'total_students': 0, 'total_courses': 0, 'department_stats': []}
    
    def generate_maintenance_report(self):
        """Generate maintenance statistics"""
        try:
            cursor = self.execute_with_retry('''
            SELECT 
                COUNT(*) as total_reports,
                SUM(CASE WHEN resolved=1 THEN 1 ELSE 0 END) as resolved_reports,
                SUM(CASE WHEN resolved=0 THEN 1 ELSE 0 END) as pending_reports
            FROM maintenance_reports
            ''')
            report_stats = cursor.fetchone()
            
            cursor.execute('''
            SELECT c.classroom_id, c.location, COUNT(mr.report_id) as report_count
            FROM classrooms c
            LEFT JOIN maintenance_reports mr ON c.classroom_id = mr.classroom_id
            GROUP BY c.classroom_id
            ORDER BY report_count DESC
            ''')
            classroom_reports = cursor.fetchall()
            
            return {
                'total_reports': report_stats['total_reports'],
                'resolved': report_stats['resolved_reports'],
                'pending': report_stats['pending_reports'],
                'classroom_reports': [dict(row) for row in classroom_reports]
            }
        except Exception as e:
            print(f"Error generating maintenance report: {e}")
            return {'total_reports': 0, 'resolved': 0, 'pending': 0, 'classroom_reports': []}
    
    # =====================
    # MIGRATION FROM JSON FILES
    # =====================
    
    def migrate_from_json(self, controller):
        """Migrate data from existing JSON-based system to database"""
        print("Starting migration from JSON files to database...")
        
        try:
            # 1. FIRST: Migrate professors from staff manager
            print("Syncing professors...")
            professors = controller.staff_mgr.get_all_professors()
            for prof in professors:
                try:
                    self.add_professor({
                        'professor_id': prof.get('id'),
                        'name': prof.get('name'),
                        'department': prof.get('department'),
                        'email': prof.get('email')
                    })
                except Exception as e:
                    print(f"  Warning: Could not add professor {prof.get('id')}: {e}")
            
            # 2. Migrate students
            print("Syncing students...")
            students = controller.student_mgr.list_students()
            for student in students:
                try:
                    self.add_student(student)
                except Exception as e:
                    print(f"  Warning: Could not add student {student.get('student_id')}: {e}")
            
            # 3. Migrate courses
            print("Syncing courses and enrollments...")
            courses = controller.curriculum_mgr.list_courses()
            for course in courses:
                # Check if professor exists in database
                prof_id = course.professor_id
                
                # If professor doesn't exist, create placeholder
                if prof_id:
                    cursor = self.execute_with_retry(
                        "SELECT professor_id FROM professors WHERE professor_id = ?",
                        (prof_id,)
                    )
                    if not cursor.fetchone():
                        try:
                            # Add placeholder professor
                            self.execute_with_retry(
                                "INSERT OR IGNORE INTO professors (professor_id, name, department) VALUES (?, ?, ?)",
                                (prof_id, f"Professor {prof_id}", course.department or 'Unknown')
                            )
                            print(f"  Created placeholder professor: {prof_id}")
                        except Exception as e:
                            print(f"  Warning: Could not create placeholder professor {prof_id}: {e}")
                            prof_id = None  # Set to NULL if can't create
                
                try:
                    course_data = {
                        'course_code': course.course_code,
                        'course_name': course.course_name,
                        'credits': course.credits,
                        'department': course.department,
                        'description': course.description or '',
                        'is_core': course.is_core,
                        'professor_id': prof_id  # Will be None if professor doesn't exist
                    }
                    self.add_course(course_data)
                except Exception as e:
                    print(f"  Warning: Could not add course {course.course_code}: {e}")
                
                # 4. Migrate enrollments for this course
                for student_id in course.students_enrolled:
                    try:
                        self.enroll_student_in_course(student_id, course.course_code)
                    except Exception as e:
                        print(f"  Warning: Could not enroll {student_id} in {course.course_code}: {e}")
            
            # 5. Migrate classrooms
            print("Syncing classrooms...")
            for classroom in controller.scheduler.classrooms:
                try:
                    cursor = self.execute_with_retry('''
                    INSERT OR REPLACE INTO classrooms (classroom_id, capacity, location, is_under_maintenance)
                    VALUES (?, ?, ?, ?)
                    ''', (
                        classroom.id,
                        classroom.capacity,
                        classroom.location or '',
                        classroom.is_under_maintenance
                    ))
                    
                    # Migrate maintenance notes
                    for note in classroom.maintenance_notes:
                        self.execute_with_retry('''
                        INSERT INTO maintenance_reports (classroom_id, description)
                        VALUES (?, ?)
                        ''', (classroom.id, note))
                except Exception as e:
                    print(f"  Warning: Could not add classroom {classroom.id}: {e}")
            
            # 6. Migrate equipment
            print("Syncing equipment...")
            for equipment in controller.equipment_mgr.equipment_list.values():
                try:
                    cursor = self.execute_with_retry('''
                    INSERT OR REPLACE INTO equipment (equipment_id, name, category, is_allocated, allocated_to)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        equipment.equipment_id,
                        equipment.name,
                        equipment.category,
                        equipment.is_allocated,
                        equipment.allocated_to or ''
                    ))
                except Exception as e:
                    print(f"  Warning: Could not add equipment {equipment.equipment_id}: {e}")
            
            self.commit()
            print("\n✅ Migration completed successfully!")
            print(f"   - {len(students)} students")
            print(f"   - {len(professors)} professors")
            print(f"   - {len(courses)} courses")
            print(f"   - {len(controller.scheduler.classrooms)} classrooms")
            print("All your existing data is now in the SQLite database.")
            print("Database file: university_system.db")
            return True
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            self.rollback()
            return False
    
    def close(self):
        """Close database connection safely"""
        with self._lock:
            if self.conn:
                try:
                    # Commit any pending changes
                    self.conn.commit()
                    self.conn.close()
                    self.conn = None
                except Exception as e:
                    print(f"Warning during database close: {e}")
                finally:
                    self.conn = None
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.close()

# =====================
# INTEGRATION WITH YOUR EXISTING SYSTEM
# =====================

class DatabaseIntegration:
    """Integrates database with your existing system"""
    
    def __init__(self, controller):
        self.controller = controller
        self.db = UniversityDatabase("university_system.db")
        
    def sync_student_data(self):
        """Sync student data between JSON files and database"""
        try:
            students = self.controller.student_mgr.list_students()
            
            for student in students:
                # Use INSERT OR REPLACE to handle duplicates
                try:
                    self.db.add_student(student)
                except Exception as e:
                    print(f"Warning: Could not sync student {student.get('student_id')}: {e}")
            
            return len(students)
        except Exception as e:
            print(f"Error syncing student data: {e}")
            return 0
    
    def sync_course_enrollments(self):
        """Sync course enrollments"""
        try:
            courses = self.controller.curriculum_mgr.list_courses()
            count = 0
            
            for course in courses:
                for student_id in course.students_enrolled:
                    if self.db.enroll_student_in_course(student_id, course.course_code):
                        count += 1
            
            return count
        except Exception as e:
            print(f"Error syncing enrollments: {e}")
            return 0
    
    def sync_classroom_reservations(self):
        """Sync classroom reservations"""
        try:
            for reservation in self.controller.scheduler.reservations:
                reservation_data = {
                    'classroom_id': reservation.classroom_id,
                    'reserved_by': reservation.reserved_by,
                    'start_time': reservation.start.isoformat(),
                    'end_time': reservation.end.isoformat(),
                    'purpose': f"Reservation {reservation.id}"
                }
                self.db.create_reservation(reservation_data)
            
            return len(self.controller.scheduler.reservations)
        except Exception as e:
            print(f"Error syncing reservations: {e}")
            return 0
    
    def full_sync(self):
        """Perform full synchronization"""
        print("Starting full sync between JSON files and database...")
        try:
            student_count = self.sync_student_data()
            enrollment_count = self.sync_course_enrollments()
            reservation_count = self.sync_classroom_reservations()
            
            print(f"Sync completed: {student_count} students, {enrollment_count} enrollments, {reservation_count} reservations")
            return True
        except Exception as e:
            print(f"Error during full sync: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()

# =====================
# DEMO AND TESTING
# =====================

def demo_database():
    """Demonstrate the database functionality"""
    db = UniversityDatabase("university_demo.db")
    
    print("=" * 60)
    print("UNIVERSITY DATABASE DEMO")
    print("=" * 60)
    
    try:
        # 1. Add traditional data
        print("\n1. Adding traditional data...")
        
        # Add a student
        db.add_student({
            'student_id': 'DB001',
            'first_name': 'John',
            'last_name': 'Database',
            'email': 'john.db@uni.edu',
            'department': 'Computer Science',
            'enrollment_year': 2023,
            'gpa': 3.8
        })
        
        # Add a professor
        db.add_professor({
            'professor_id': 'PDB001',
            'name': 'Dr. Database Expert',
            'department': 'Computer Science',
            'email': 'db.expert@uni.edu'
        })
        
        # Add a course
        db.add_course({
            'course_code': 'CS500',
            'course_name': 'Database Systems',
            'credits': 3,
            'department': 'Computer Science',
            'description': 'Advanced database concepts',
            'professor_id': 'PDB001',
            'is_core': True
        })
        
        # Enroll student
        db.enroll_student_in_course('DB001', 'CS500')
        
        # 2. Demonstrate EAV system
        print("\n2. Demonstrating EAV system...")
        
        # Create a license using EAV
        license_id = db.create_license_entity('LIC001', 'Design Suite Pro', 50)
        print(f"Created license entity: {license_id}")
        
        # Add properties to license
        db.set_property(license_id, 'vendor', 'Adobe Inc.')
        db.set_property(license_id, 'expiry_date', '2025-12-31')
        db.set_property(license_id, 'annual_cost', 9999.99, 'real')
        
        # Allocate some seats
        for i in range(3):
            db.allocate_license_seat(license_id)
        
        # Get license info
        license_props = db.get_all_properties(license_id)
        print(f"License properties: {license_props}")
        
        # Create an announcement using EAV
        announcement_id = db.create_announcement_entity(
            'Database Maintenance',
            'System will be down for maintenance on Saturday',
            'department',
            'Computer Science'
        )
        print(f"Created announcement entity: {announcement_id}")
        
        # 3. Demonstrate queries
        print("\n3. Running queries...")
        
        # Get all licenses
        licenses = db.get_entities_by_type('license')
        print(f"Found {len(licenses)} licenses")
        
        for lic in licenses:
            print(f"  - {lic['name']}: {lic['properties'].get('used_seats', 0)}/{lic['properties'].get('total_seats', 0)} seats used")
        
        # Get student courses
        student_courses = db.get_student_courses('DB001')
        print(f"\nStudent DB001 is enrolled in {len(student_courses)} courses:")
        for course in student_courses:
            print(f"  - {course['course_code']}: {course['course_name']}")
        
        # Generate reports
        print("\n4. Generating reports...")
        enrollment_report = db.generate_enrollment_report()
        print(f"Total enrolled students: {enrollment_report['total_students']}")
        print(f"Total courses: {enrollment_report['total_courses']}")
        
        print("\n✅ Database demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Database demo failed: {e}")
    
    finally:
        # Always close the database
        db.close()

def create_schema_diagram():
    """Print database schema for documentation"""
    print("=" * 80)
    print("DATABASE SCHEMA - UNIVERSITY MANAGEMENT SYSTEM")
    print("=" * 80)
    
    schema = """
    ===================== TRADITIONAL TABLES =====================
    
    1. students
       ---------
       student_id (PK) | first_name | last_name | email | department
       enrollment_year | gpa | status | created_at
       
    2. professors
       -----------
       professor_id (PK) | name | department | email | hire_date | created_at
       
    3. courses
       --------
       course_code (PK) | course_name | credits | department | description
       is_core | professor_id (FK) | semester_offered | created_at
       
    4. classrooms
       -----------
       classroom_id (PK) | capacity | location | is_under_maintenance | created_at
       
    5. equipment
       ----------
       equipment_id (PK) | name | category | is_allocated | allocated_to
       allocation_date | is_lab_equipment | created_at
       
    6. reservations
       -------------
       reservation_id (PK) | classroom_id (FK) | reserved_by | start_time
       end_time | purpose | created_at
       
    7. maintenance_reports
       -------------------
       report_id (PK) | classroom_id (FK) | description | reported_by
       reported_at | resolved | resolved_at
       
    8. student_courses
       ---------------
       enrollment_id (PK) | student_id (FK) | course_code (FK) | enrollment_date
       grade | status
       
    9. study_plans
       ------------
       plan_id (PK) | student_id (FK) | semester | course_code (FK) | planned_at
       
    10. assignments
        ------------
        assignment_id (PK) | course_code (FK) | title | description | due_date
        max_points | assignment_type | created_at
        
    11. submissions
        ------------
        submission_id (PK) | assignment_id (FK) | student_id (FK) | submission_text
        submitted_date | grade | feedback
    
    ===================== EAV TABLES (FLEXIBLE) =====================
    
    12. entities
        --------
        entity_id (PK) | entity_type | name | created_at
        
    13. properties
        -----------
        property_id (PK) | entity_id (FK) | attribute | value | data_type | created_at
        
    ===================== KEY RELATIONSHIPS =====================
    
    1. courses.professor_id → professors.professor_id
    2. student_courses.student_id → students.student_id
    3. student_courses.course_code → courses.course_code
    4. reservations.classroom_id → classrooms.classroom_id
    5. maintenance_reports.classroom_id → classrooms.classroom_id
    6. study_plans.student_id → students.student_id
    7. study_plans.course_code → courses.course_code
    8. assignments.course_code → courses.course_code
    9. submissions.assignment_id → assignments.assignment_id
    10. submissions.student_id → students.student_id
    11. properties.entity_id → entities.entity_id
    """
    
    print(schema)
    print("=" * 80)
    print("EAV TABLES USED FOR:")
    print("  • Software Licenses (dynamic attributes)")
    print("  • Announcements (flexible targeting)")
    print("  • Feedback (custom fields)")
    print("  • Any other dynamic data requirements")
    print("=" * 80)

if __name__ == "__main__":
    # Show schema diagram
    create_schema_diagram()
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Create fresh database with demo data")
    print("2. View schema only")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        demo_database()
    elif choice == "2":
        create_schema_diagram()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Exiting.")