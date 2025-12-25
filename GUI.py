# GUI.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import os

# Import all the modules
from Classroom_Manager import Scheduler, Classroom, Reservation
from equipment_management import (
    EquipmentManager, Equipment, 
    LicenseManager, SoftwareLicense, 
    PersonAllocationManager, LaboratoryEquipmentManager
)
from Student_Manager import StudentManager
from Curriculum_Manager import CurriculumManager, Course, StudentPlanner
from LMS_Manager import LMSManager, LMSContent, Assignment, Quiz, ContentType, AssignmentType, Gradebook, Feedback
from Staff_Manager import StaffManager # Import StaffManager
from University_Controller import UniversityController # Import the new Controller


class UniversityManagementGUI:
       def __init__(self, root):
        self.root = root
        self.root.title("Integrated University System v5.0 WITH DATABASE")
        self.root.geometry("1400x900")
        
        # Initialize the Controller
        self.controller = UniversityController()
        
        # Map controller managers to local variables for compatibility
        self.scheduler = self.controller.scheduler
        self.eq_manager = self.controller.equipment_mgr  # Primary name
        self.student_manager = self.controller.student_mgr
        self.curriculum_manager = self.controller.curriculum_mgr
        self.lms_manager = self.controller.lms_mgr
        self.staff_manager = self.controller.staff_mgr
        self.student_planner = self.controller.student_planner
        self.person_manager = self.controller.person_mgr
        
        # Aliases for backward compatibility with existing GUI methods
        self.eq_manager = self.controller.equipment_mgr  # Alias for equipment tabs
        self.license_manager = self.controller.license_mgr
        self.lab_eq_manager = self.controller.lab_eq_mgr

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()        # Overview first
        self.create_student_tab()          # Student info
        self.create_staff_tab()            # Staff & Faculty Tab
        self.create_curriculum_tab()       # Courses and Planning
        self.create_classroom_tab()        # Scheduling
        self.create_lms_tab()              # Learning Content & Assessments
        self.create_equipment_tab()        # Resources
        self.create_license_tab()
        self.create_lab_equipment_tab()
        self.create_people_tab()           # Allocation
        self.create_student_portal_tab()   # Student View
        self.create_database_tab()         # Database Management Tab
        
        # Initial data loading/refreshing
        self.refresh_all_data()

def refresh_all_data(self):
        """Call refresh methods for all relevant tabs in a robust way."""
        methods = [
            'refresh_dashboard', 'list_students', 'refresh_staff', 'refresh_courses',
            'refresh_classroom_info', 'refresh_lms_content', 'refresh_equipment_info',
            'refresh_license_info', 'refresh_lab_equipment_info', 'refresh_people_info',
            'update_student_portal_comboboxes', 'refresh_study_plan_display'
        ]
        for m in methods:
            fn = getattr(self, m, None)
            if callable(fn):
                try:
                    fn()
                except Exception as e:
                    # Keep initialization resilient; log a concise warning with method name
                    try:
                        print(f"Warning: refresh_all_data encountered an error in {m}: {e}")
                    except Exception:
                        pass
        

def setup_managers(self):
        """Removed this method as managers are now initialized via the Controller."""
        pass

# Add this method to the UniversityManagementGUI class
def create_database_tab(self):
    """Create database management tab"""
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="Database")
    
    # Notebook for database operations
    db_notebook = ttk.Notebook(frame)
    db_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Tab 1: Database Queries
    query_frame = ttk.Frame(db_notebook)
    db_notebook.add(query_frame, text="Query Data")
    
    # Query interface
    query_input = ttk.LabelFrame(query_frame, text="Database Queries", padding=10)
    query_input.pack(fill=tk.X, padx=10, pady=5)
    
    # Student query
    ttk.Label(query_input, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
    self.db_student_id = ttk.Entry(query_input, width=20)
    self.db_student_id.grid(row=0, column=1, pady=2, padx=5)
    
    ttk.Button(query_input, text="Get Student from DB", 
              command=self.get_student_from_db_gui).grid(row=0, column=2, padx=5)
    
    # Course query
    ttk.Label(query_input, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=2)
    self.db_course_code = ttk.Entry(query_input, width=20)
    self.db_course_code.grid(row=1, column=1, pady=2, padx=5)
    
    ttk.Button(query_input, text="Get Course from DB", 
              command=self.get_course_from_db_gui).grid(row=1, column=2, padx=5)
    
    # Reports
    ttk.Button(query_input, text="Generate Enrollment Report", 
              command=self.generate_enrollment_report_gui).grid(row=2, column=0, pady=10, padx=5)
    ttk.Button(query_input, text="Generate Maintenance Report", 
              command=self.generate_maintenance_report_gui).grid(row=2, column=1, pady=10, padx=5)
    ttk.Button(query_input, text="List All Students from DB", 
              command=self.list_all_students_db_gui).grid(row=2, column=2, pady=10, padx=5)
    
    # Display area
    query_display_frame = ttk.LabelFrame(query_frame, text="Query Results", padding=10)
    query_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    self.db_query_display = scrolledtext.ScrolledText(query_display_frame, height=20, wrap=tk.WORD)
    self.db_query_display.pack(fill=tk.BOTH, expand=True)
    
    # Tab 2: EAV Management
    eav_frame = ttk.Frame(db_notebook)
    db_notebook.add(eav_frame, text="EAV System")
    
    # License management
    license_frame = ttk.LabelFrame(eav_frame, text="Software License (EAV)", padding=10)
    license_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(license_frame, text="License ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
    self.license_id_entry = ttk.Entry(license_frame, width=25)
    self.license_id_entry.grid(row=0, column=1, pady=2, padx=5)
    
    ttk.Label(license_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
    self.license_name_entry = ttk.Entry(license_frame, width=25)
    self.license_name_entry.grid(row=1, column=1, pady=2, padx=5)
    
    ttk.Label(license_frame, text="Total Seats:").grid(row=2, column=0, sticky=tk.W, pady=2)
    self.license_seats_entry = ttk.Entry(license_frame, width=25)
    self.license_seats_entry.grid(row=2, column=1, pady=2, padx=5)
    
    ttk.Button(license_frame, text="Create License (EAV)", 
              command=self.create_license_eav_gui).grid(row=3, column=0, columnspan=2, pady=10)
    
    # Announcement management
    announcement_frame = ttk.LabelFrame(eav_frame, text="Announcement (EAV)", padding=10)
    announcement_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(announcement_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=2)
    self.announcement_title_entry = ttk.Entry(announcement_frame, width=40)
    self.announcement_title_entry.grid(row=0, column=1, pady=2, padx=5)
    
    ttk.Label(announcement_frame, text="Content:").grid(row=1, column=0, sticky=tk.W, pady=2)
    self.announcement_content_entry = tk.Text(announcement_frame, height=3, width=40)
    self.announcement_content_entry.grid(row=1, column=1, pady=2, padx=5)
    
    ttk.Label(announcement_frame, text="Target Type:").grid(row=2, column=0, sticky=tk.W, pady=2)
    self.announcement_target_type = ttk.Combobox(announcement_frame, values=["course", "department", "all"], width=38)
    self.announcement_target_type.grid(row=2, column=1, pady=2, padx=5)
    
    ttk.Label(announcement_frame, text="Target Value:").grid(row=3, column=0, sticky=tk.W, pady=2)
    self.announcement_target_value = ttk.Entry(announcement_frame, width=40)
    self.announcement_target_value.grid(row=3, column=1, pady=2, padx=5)
    
    ttk.Button(announcement_frame, text="Create Announcement (EAV)", 
              command=self.create_announcement_eav_gui).grid(row=4, column=0, columnspan=2, pady=10)
    
    ttk.Button(announcement_frame, text="List All Announcements", 
              command=self.list_announcements_gui).grid(row=5, column=0, columnspan=2, pady=5)
    
    # EAV Display
    eav_display_frame = ttk.LabelFrame(eav_frame, text="EAV Data", padding=10)
    eav_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    self.eav_display = scrolledtext.ScrolledText(eav_display_frame, height=10, wrap=tk.WORD)
    self.eav_display.pack(fill=tk.BOTH, expand=True)
    # ... (rest of the GUI class methods below) ...

    # -----------------------------------------------------
    # NEW: Staff Tab
    # -----------------------------------------------------
    def create_staff_tab(self):
        """Create Staff management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Staff & Faculty")
        
        # Left panel - Professor Management
        input_frame = ttk.LabelFrame(frame, text="Add Professor", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Professor ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.staff_prof_id = ttk.Entry(input_frame)
        self.staff_prof_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.staff_prof_name = ttk.Entry(input_frame)
        self.staff_prof_name.grid(row=1, column=1, pady=2)

        ttk.Label(input_frame, text="Department:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.staff_prof_dept = ttk.Entry(input_frame)
        self.staff_prof_dept.grid(row=2, column=1, pady=2)

        ttk.Label(input_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.staff_prof_email = ttk.Entry(input_frame)
        self.staff_prof_email.grid(row=3, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add Professor", command=self.add_professor_gui).grid(row=4, columnspan=2, pady=10)
        
        # Middle panel - Assign Course to Professor
        assign_frame = ttk.LabelFrame(frame, text="Assign Course to Professor", padding=10)
        assign_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(assign_frame, text="Professor ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.assign_prof_id_entry = ttk.Entry(assign_frame)
        self.assign_prof_id_entry.grid(row=0, column=1, pady=2)
        
        ttk.Label(assign_frame, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.assign_course_code_entry = ttk.Entry(assign_frame)
        self.assign_course_code_entry.grid(row=1, column=1, pady=2)
        
        ttk.Button(assign_frame, text="Assign Course", command=self.assign_course_to_prof_gui).grid(row=2, columnspan=2, pady=10)

        # Right panel - Display
        self.staff_display = scrolledtext.ScrolledText(frame, height=20, width=50, wrap=tk.WORD)
        self.staff_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Button(frame, text="Refresh Staff List", command=self.refresh_staff).pack(side=tk.BOTTOM, pady=5)

        self.refresh_staff() # Initial load

    def add_professor_gui(self):
        try:
            prof_id = self.staff_prof_id.get()
            name = self.staff_prof_name.get()
            dept = self.staff_prof_dept.get()
            email = self.staff_prof_email.get()
            
            if not all([prof_id, name, dept]):
                messagebox.showwarning("Input Error", "Professor ID, Name, and Department are required.")
                return

            message = self.staff_manager.add_professor(prof_id, name, dept, email)
            messagebox.showinfo("Success", message)
            self.staff_prof_id.delete(0, tk.END)
            self.staff_prof_name.delete(0, tk.END)
            self.staff_prof_dept.delete(0, tk.END)
            self.staff_prof_email.delete(0, tk.END)
            self.refresh_staff()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {str(e)}")

    def assign_course_to_prof_gui(self):
        try:
            prof_id = self.assign_prof_id_entry.get()
            course_code = self.assign_course_code_entry.get()

            if not all([prof_id, course_code]):
                messagebox.showwarning("Input Error", "Professor ID and Course Code are required.")
                return

            # Use the Controller for integrated assignment
            message = self.controller.assign_professor_to_course(prof_id, course_code)
            messagebox.showinfo("Success", message)
            
            self.assign_prof_id_entry.delete(0, tk.END)
            self.assign_course_code_entry.delete(0, tk.END)
            self.refresh_staff()
            self.refresh_courses() # Courses list might be updated
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {str(e)}")

    def refresh_staff(self):
        self.staff_display.delete(1.0, tk.END)
        professors = self.staff_manager.get_all_professors()
        if not professors:
            self.staff_display.insert(tk.END, "No professors added yet.")
            return

        for prof_data in professors:
            self.staff_display.insert(tk.END, f"ID: {prof_data.get('id', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Name: {prof_data.get('name', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Department: {prof_data.get('department', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Email: {prof_data.get('email', 'N/A')}\n")
            courses = prof_data.get('courses_taught', [])
            self.staff_display.insert(tk.END, f"Courses Taught: {', '.join(courses) if courses else 'None'}\n")
            self.staff_display.insert(tk.END, "-"*30 + "\n")
    
    # -----------------------------------------------------
    # Classroom Methods
    # -----------------------------------------------------
    def get_classroom_ids(self):
        return [room.id for room in self.scheduler.classrooms]
    
    def add_classroom(self):
        try:
            room_id = self.classroom_id.get()
            capacity_str = self.capacity.get()
            location = self.location.get()
            
            if not room_id or not capacity_str:
                messagebox.showwarning("Input Error", "Classroom ID and Capacity are required.")
                return
            
            capacity = int(capacity_str)
            
            self.scheduler.add_classroom(Classroom(id=room_id, capacity=capacity, location=location))
            messagebox.showinfo("Success", f"Classroom {room_id} added successfully!")
            self.classroom_id.delete(0, tk.END)
            self.capacity.delete(0, tk.END)
            self.location.delete(0, tk.END)
            self.refresh_classroom_info()
            # Update combobox values
            self.maintenance_room['values'] = self.get_classroom_ids()
            self.reserve_room['values'] = self.get_classroom_ids()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add classroom: {str(e)}")
    
    def report_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            description = self.maintenance_desc.get()
            
            if not room_id or not description:
                messagebox.showwarning("Input Error", "Please select a classroom and provide a description.")
                return

            result = self.scheduler.report_maintenance(room_id, description)
            messagebox.showinfo("Success", result)
            self.maintenance_desc.delete(0, tk.END)
            self.refresh_classroom_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to report maintenance: {str(e)}")
    
    def resolve_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            if not room_id:
                messagebox.showwarning("Input Error", "Please select a classroom to resolve maintenance.")
                return

            result = self.scheduler.resolve_maintenance(room_id)
            messagebox.showinfo("Success", result)
            self.maintenance_desc.delete(0, tk.END)
            self.refresh_classroom_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resolve maintenance: {str(e)}")
    
    def make_reservation(self):
        try:
            room_id = self.reserve_room.get()
            reserved_by = self.reserved_by.get()
            
            if not room_id or not reserved_by:
                messagebox.showwarning("Input Error", "Please select a room and enter who it's reserved by.")
                return

            # For simplicity, reserve for the next hour
            now = datetime.now()
            start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            
            result = self.scheduler.reserve_classroom(room_id, start_time, end_time, reserved_by)
            messagebox.showinfo("Reservation Status", result)
            self.reserved_by.delete(0, tk.END)
            self.refresh_classroom_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make reservation: {str(e)}")
    
    def refresh_classroom_info(self):
        self.classroom_display.delete(1.0, tk.END)
        if not self.scheduler.classrooms:
            self.classroom_display.insert(tk.END, "No classrooms added yet.")
            return

        info = "=== CLASSROOMS ===\n\n"
        for room in self.scheduler.classrooms:
            info += f"ID: {room.id}\n"
            info += f"Capacity: {room.capacity}\n"
            info += f"Location: {room.location if room.location else 'N/A'}\n"
            info += f"Maintenance: {'YES' if room.is_under_maintenance else 'NO'}\n"
            if room.maintenance_notes:
                info += f"Maintenance Notes: {', '.join(room.maintenance_notes)}\n"
            
            # Show reservations for this room
            room_reservations = [r for r in self.scheduler.reservations if r.classroom_id == room.id]
            if room_reservations:
                info += "Reservations:\n"
                for res in room_reservations:
                    info += f"  - Res ID {res.id} by {res.reserved_by}: {res.start.strftime('%Y-%m-%d %H:%M')} to {res.end.strftime('%H:%M')}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.classroom_display.insert(tk.END, info)
    
    # -----------------------------------------------------
    # Equipment Methods
    # -----------------------------------------------------
    def get_equipment_ids(self):
        return list(self.eq_manager.equipment_list.keys())
    
    def add_equipment(self):
        try:
            eq_id = self.eq_id.get()
            name = self.eq_name.get()
            category = self.eq_category.get()
            
            if not all([eq_id, name, category]):
                messagebox.showwarning("Input Error", "Equipment ID, Name, and Category are required.")
                return

            self.eq_manager.add_equipment(Equipment(eq_id, name, category))
            messagebox.showinfo("Success", f"Equipment '{name}' (ID: {eq_id}) added successfully!")
            self.eq_id.delete(0, tk.END)
            self.eq_name.delete(0, tk.END)
            self.eq_category.delete(0, tk.END)
            self.refresh_equipment_info()
            self.safe_set_values(self.alloc_eq_id, self.get_equipment_ids())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add equipment: {str(e)}")
    
    def allocate_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get()
            allocated_to = self.alloc_to.get()
            
            if not eq_id or not allocated_to:
                messagebox.showwarning("Input Error", "Please select an equipment and enter who it's allocated to.")
                return

            self.eq_manager.allocate_equipment(eq_id, allocated_to)
            messagebox.showinfo("Success", f"Equipment {eq_id} allocated to {allocated_to}!")
            self.alloc_to.delete(0, tk.END)
            self.refresh_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate equipment: {str(e)}")
    
    def release_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get()
            if not eq_id:
                messagebox.showwarning("Input Error", "Please select an equipment to release.")
                return

            self.eq_manager.release_equipment(eq_id)
            messagebox.showinfo("Success", f"Equipment {eq_id} released!")
            self.alloc_to.delete(0, tk.END) # Clear allocation field
            self.refresh_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release equipment: {str(e)}")
    
    def refresh_equipment_info(self):
        self.equipment_display.delete(1.0, tk.END)
        if not self.eq_manager.equipment_list:
            self.equipment_display.insert(tk.END, "No equipment added yet.")
            return

        info = "=== EQUIPMENT STATUS ===\n\n"
        for eq in self.eq_manager.track_equipment():
            info += f"ID: {eq['id']}\n"
            info += f"Name: {eq['name']}\n"
            info += f"Category: {eq['category']}\n"
            info += f"Allocated: {'Yes' if eq['allocated'] else 'No'}\n"
            if eq['allocated']:
                info += f"Allocated To: {eq['allocated_to']}\n"
                info += f"Allocation Date: {eq['allocation_date'].strftime('%Y-%m-%d %H:%M:%S') if eq['allocation_date'] else 'N/A'}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.equipment_display.insert(tk.END, info)
    
    # -----------------------------------------------------
    # License Methods
    # -----------------------------------------------------
    def get_license_ids(self):
        return list(self.license_manager.licenses.keys())
    
    def add_license(self):
        try:
            license_id = self.license_id.get()
            name = self.software_name.get()
            total_seats_str = self.total_seats.get()
            
            if not all([license_id, name, total_seats_str]):
                messagebox.showwarning("Input Error", "License ID, Software Name, and Total Seats are required.")
                return

            total_seats = int(total_seats_str)
            
            self.license_manager.add_license(SoftwareLicense(license_id, name, total_seats))
            messagebox.showinfo("Success", f"License '{name}' (ID: {license_id}) with {total_seats} seats added successfully!")
            self.license_id.delete(0, tk.END)
            self.software_name.delete(0, tk.END)
            self.total_seats.delete(0, tk.END)
            self.refresh_license_info()
            self.safe_set_values(self.alloc_license_id, self.get_license_ids())
        except ValueError:
            messagebox.showerror("Input Error", "Total seats must be a valid integer.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add license: {str(e)}")
    
    def allocate_license(self):
        try:
            license_id = self.alloc_license_id.get()
            if not license_id:
                messagebox.showwarning("Input Error", "Please select a license.")
                return

            self.license_manager.allocate(license_id)
            messagebox.showinfo("Success", f"License seat allocated for {license_id}!")
            self.refresh_license_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate license seat: {str(e)}")
    
    def release_license(self):
        try:
            license_id = self.alloc_license_id.get()
            if not license_id:
                messagebox.showwarning("Input Error", "Please select a license.")
                return
                
            self.license_manager.release(license_id)
            messagebox.showinfo("Success", f"License seat released for {license_id}!")
            self.refresh_license_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release license seat: {str(e)}")
    
    def refresh_license_info(self):
        self.license_display.delete(1.0, tk.END)
        if not hasattr(self.license_manager, 'licenses') or not self.license_manager.licenses:
            self.license_display.insert(tk.END, "No software licenses added yet.")
            return

        info = "=== SOFTWARE LICENSE STATUS ===\n\n"
        # track_licenses may return a mapping or a custom structure; support both
        try:
            tracked = self.license_manager.track_licenses()
            if isinstance(tracked, dict):
                items = tracked.values()
            else:
                items = list(tracked)
        except Exception:
            items = list(self.license_manager.licenses.values())

        for lic in items:
            if isinstance(lic, dict):
                name = lic.get('name')
                used = lic.get('used_seats', '?')
                total = lic.get('total_seats', '?')
            else:
                name = getattr(lic, 'name', str(lic))
                used = getattr(lic, 'used_seats', '?')
                total = getattr(lic, 'total_seats', '?')
            info += f"Software: {name}\n"
            info += f"Seats Used: {used}/{total}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.license_display.insert(tk.END, info)

    def safe_set_values(self, widget, values):
        """Set combobox values safely only when widget supports '-values' option."""
        try:
            if isinstance(widget, ttk.Combobox):
                widget['values'] = values
        except Exception:
            # Ignore failures during bulk refreshes to keep UI responsive
            pass
    
    # -----------------------------------------------------
    # Lab Equipment Methods
    # -----------------------------------------------------
    def get_lab_equipment_ids(self):
        return list(self.lab_eq_manager.lab_equipment.keys())
    
    def add_lab_equipment(self):
        try:
            eq_id = self.lab_eq_id.get()
            name = self.lab_eq_name.get()
            category = self.lab_eq_category.get()
            
            if not all([eq_id, name, category]):
                messagebox.showwarning("Input Error", "Lab Equipment ID, Name, and Category are required.")
                return

            self.lab_eq_manager.add_lab_equipment(Equipment(eq_id, name, category))
            messagebox.showinfo("Success", f"Lab Equipment '{name}' (ID: {eq_id}) added successfully!")
            self.lab_eq_id.delete(0, tk.END)
            self.lab_eq_name.delete(0, tk.END)
            self.lab_eq_category.delete(0, tk.END)
            self.refresh_lab_equipment_info()
            self.safe_set_values(self.alloc_lab_eq_id, self.get_lab_equipment_ids())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add lab equipment: {str(e)}")
    
    def allocate_lab_equipment(self):
        try:
            eq_id = self.alloc_lab_eq_id.get()
            allocated_to = self.alloc_lab_to.get()
            
            if not eq_id or not allocated_to:
                messagebox.showwarning("Input Error", "Please select lab equipment and enter who it's allocated to.")
                return

            self.lab_eq_manager.allocate_lab_equipment(eq_id, allocated_to)
            messagebox.showinfo("Success", f"Lab Equipment {eq_id} allocated to {allocated_to}!")
            self.alloc_lab_to.delete(0, tk.END)
            self.refresh_lab_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate lab equipment: {str(e)}")
    
    def release_lab_equipment(self):
        try:
            eq_id = self.alloc_lab_eq_id.get()
            if not eq_id:
                messagebox.showwarning("Input Error", "Please select lab equipment to release.")
                return

            self.lab_eq_manager.release_lab_equipment(eq_id)
            messagebox.showinfo("Success", f"Lab Equipment {eq_id} released!")
            self.alloc_lab_to.delete(0, tk.END) # Clear allocation field
            self.refresh_lab_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release lab equipment: {str(e)}")
    
    def refresh_lab_equipment_info(self):
        self.lab_equipment_display.delete(1.0, tk.END)
        if not self.lab_eq_manager.lab_equipment:
            self.lab_equipment_display.insert(tk.END, "No lab equipment added yet.")
            return

        info = "=== LAB EQUIPMENT STATUS ===\n\n"
        for eq in self.lab_eq_manager.track_lab_equipment():
            info += f"ID: {eq['id']}\n"
            info += f"Name: {eq['name']}\n"
            info += f"Category: {eq['category']}\n"
            info += f"Allocated: {'Yes' if eq['allocated'] else 'No'}\n"
            if eq['allocated']:
                info += f"Allocated To: {eq['allocated_to']}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.lab_equipment_display.insert(tk.END, info)
    
    # -----------------------------------------------------
    # Student Methods
    # -----------------------------------------------------
    def get_student_ids(self):
        return [s['student_id'] for s in self.student_manager.list_students()]
    
    def add_student(self):
        try:
            student_id = self.student_id.get()
            first_name = self.first_name.get()
            last_name = self.last_name.get()
            department = self.department.get()
            enrollment_year = self.enrollment_year.get()
            
            if not all([student_id, first_name, last_name, department, enrollment_year]):
                messagebox.showwarning("Input Error", "All fields (Student ID, Name, Department, Year) are required.")
                return
                
            student_data = {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "department": department,
                "enrollment_year": enrollment_year,
                # Optional fields (can be empty or pre-filled)
                "email": self.email.get() if hasattr(self, 'email') and self.email.get() else "N/A",
                "gpa": self.gpa.get() if hasattr(self, 'gpa') and self.gpa.get() else "N/A",
                "status": self.status.get() if hasattr(self, 'status') and self.status.get() else "enrolled"
            }

            # Use the Controller to register the student
            message = self.controller.register_new_student(student_data)
            messagebox.showinfo("Success", message)
            
            # Clear fields
            self.student_id.delete(0, tk.END)
            self.first_name.delete(0, tk.END)
            self.last_name.delete(0, tk.END)
            self.department.delete(0, tk.END)
            self.enrollment_year.delete(0, tk.END)
            if hasattr(self, 'email'): self.email.delete(0, tk.END)
            if hasattr(self, 'gpa'): self.gpa.delete(0, tk.END)
            if hasattr(self, 'status'): self.status.delete(0, tk.END)

            self.list_students() # Refresh display
            self.update_student_comboboxes() # Update comboboxes that use student IDs
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def get_student(self):
        try:
            student_id = self.operation_student_id.get()
            if not student_id:
                messagebox.showwarning("Input Error", "Please select or enter a Student ID.")
                return
            
            student = self.student_manager.get_student(student_id)
            if student:
                self.student_display.delete(1.0, tk.END)
                self.student_display.insert(tk.END, f"Student ID: {student.get('student_id', 'N/A')}\n")
                self.student_display.insert(tk.END, f"Name: {student.get('first_name', '')} {student.get('last_name', '')}\n")
                for key, value in student.items():
                    if key not in ["student_id", "first_name", "last_name"]:
                        self.student_display.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
            else:
                messagebox.showerror("Not Found", f"Student with ID {student_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve student: {str(e)}")

    def delete_student(self):
        try:
            student_id = self.operation_student_id.get()
            if not student_id:
                messagebox.showwarning("Input Error", "Please select or enter a Student ID to delete.")
                return
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete student {student_id} and all their records?")
            if confirm:
                # Use the Controller to perform a full deletion
                message = self.controller.delete_student_fully(student_id)
                messagebox.showinfo("Success", message)
                self.operation_student_id.set('') # Clear combobox
                self.list_students() # Refresh display
                self.update_student_comboboxes() # Update comboboxes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")

    def list_students(self):
        self.student_display.delete(1.0, tk.END)
        students = self.student_manager.list_students()
        if not students:
            self.student_display.insert(tk.END, "No students found.")
            return

        for student in students:
            self.student_display.insert(tk.END, f"ID: {student.get('student_id', 'N/A')}\n")
            self.student_display.insert(tk.END, f"Name: {student.get('first_name', '')} {student.get('last_name', '')}\n")
            self.student_display.insert(tk.END, f"Department: {student.get('department', 'N/A')}\n")
            self.student_display.insert(tk.END, f"Status: {student.get('status', 'N/A')}\n")
            self.student_display.insert(tk.END, "-"*30 + "\n")
        
        self.update_student_comboboxes() # Ensure comboboxes are updated after listing

    def update_student_comboboxes(self):
        """Updates comboboxes that list student IDs."""
        student_ids = self.get_student_ids()
        if hasattr(self, 'operation_student_id'):
            self.safe_set_values(self.operation_student_id, student_ids)
        if hasattr(self, 'portal_student'):
            self.safe_set_values(self.portal_student, student_ids)
        # Add any other comboboxes that need student IDs here

    # -----------------------------------------------------
    # People Allocation Methods
    # -----------------------------------------------------
    def assign_professor(self):
        try:
            prof_id = self.professor_id.get()
            dept = self.prof_dept.get()
            if not all([prof_id, dept]):
                messagebox.showwarning("Input Error", "Professor ID and Department are required.")
                return
            
            # Assigning just department here. Email and name are handled by Staff tab.
            self.person_manager.assign_professor(prof_id, dept)
            messagebox.showinfo("Success", f"Professor {prof_id} assigned to {dept} department.")
            self.professor_id.delete(0, tk.END)
            self.prof_dept.delete(0, tk.END)
            self.refresh_people_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign professor: {str(e)}")
    
    def assign_student(self):
        try:
            student_id = self.alloc_student_id.get()
            dept = self.student_dept.get()
            
            if not all([student_id, dept]):
                messagebox.showwarning("Input Error", "Student ID and Department are required.")
                return
                
            # Use Controller for validation if needed, or directly assign if student_manager is reliable
            if not self.student_manager.student_exists(student_id):
                raise ValueError(f"Student {student_id} does not exist.")
                
            self.person_manager.assign_student(student_id, dept)
            messagebox.showinfo("Success", f"Student {student_id} assigned to {dept} department.")
            self.alloc_student_id.delete(0, tk.END)
            self.student_dept.delete(0, tk.END)
            self.refresh_people_info()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign student: {str(e)}")
    
    def refresh_people_info(self):
        self.people_display.delete(1.0, tk.END)
        people_data = self.person_manager.track_people()
        
        self.people_display.insert(tk.END, "--- Professor Departments ---\n")
        if people_data["professors"]:
            for prof_id, dept in people_data["professors"].items():
                self.people_display.insert(tk.END, f"Professor ID: {prof_id}, Department: {dept}\n")
        else:
            self.people_display.insert(tk.END, "No professors assigned departments yet.\n")
        self.people_display.insert(tk.END, "\n")
        
        self.people_display.insert(tk.END, "--- Student Departments ---\n")
        if people_data["students"]:
            for student_id, dept in people_data["students"].items():
                self.people_display.insert(tk.END, f"Student ID: {student_id}, Department: {dept}\n")
        else:
            self.people_display.insert(tk.END, "No students assigned departments yet.\n")
        
        # Populate comboboxes if they exist
        if hasattr(self, 'alloc_student_id'):
            self.alloc_student_id['values'] = self.get_student_ids()
            # Select first student if available
            if self.get_student_ids():
                self.alloc_student_id.set(self.get_student_ids()[0])

        if hasattr(self, 'assign_prof_id_entry'):
            self.safe_set_values(self.assign_prof_id_entry, list(self.staff_manager.professors.keys()))
            if list(self.staff_manager.professors.keys()):
                self.assign_prof_id_entry.set(list(self.staff_manager.professors.keys())[0])
    
    # -----------------------------------------------------
    # Curriculum Tab Methods
    # -----------------------------------------------------
    def add_course(self):
        try:
            course_code = self.course_code.get()
            course_name = self.course_name.get()
            credits_str = self.course_credits.get()
            department = self.course_dept.get()
            description = self.course_desc.get("1.0", tk.END).strip()
            is_core = self.course_is_core.get()
            
            if not all([course_code, course_name, credits_str, department]):
                messagebox.showwarning("Input Error", "Course Code, Name, Credits, and Department are required.")
                return
            
            credits = int(credits_str)
            
            course = Course(course_code, course_name, credits, department, description)
            course.is_core = is_core
            
            self.curriculum_manager.add_course(course)
            messagebox.showinfo("Success", f"Course '{course_name}' ({course_code}) added successfully!")
            
            # Clear fields
            self.course_code.delete(0, tk.END)
            self.course_name.delete(0, tk.END)
            self.course_credits.delete(0, tk.END)
            self.course_desc.delete("1.0", tk.END)
            self.course_is_core.set(False)
            self.course_dept.set('')
            
            self.refresh_courses()
            self.update_course_comboboxes()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")

    def update_course(self):
        try:
            course_code = self.course_code.get()
            if not course_code:
                messagebox.showwarning("Input Error", "Please select a course to update (enter its code).")
                return
            
            course = self.curriculum_manager.get_course(course_code)
            if not course:
                messagebox.showerror("Not Found", f"Course {course_code} not found.")
                return

            updates = {}
            # Check if fields have new values and are different
            if self.course_name.get() and self.course_name.get() != course.course_name:
                updates["course_name"] = self.course_name.get()
            if self.course_credits.get() and int(self.course_credits.get()) != course.credits:
                updates["credits"] = int(self.course_credits.get())
            if self.course_dept.get() and self.course_dept.get() != course.department:
                updates["department"] = self.course_dept.get()
            
            description_text = self.course_desc.get("1.0", tk.END).strip()
            if description_text and description_text != course.description:
                updates["description"] = description_text
            
            if self.course_is_core.get() != course.is_core:
                updates["is_core"] = self.course_is_core.get()

            if updates:
                self.curriculum_manager.update_course(course_code, updates)
                messagebox.showinfo("Success", f"Course {course_code} updated.")
                self.refresh_courses()
            else:
                messagebox.showinfo("Info", "No changes detected for course updates.")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update course: {str(e)}")

    def delete_course(self):
        try:
            course_code = self.course_code.get()
            if not course_code:
                messagebox.showwarning("Input Error", "Please enter the Course Code to delete.")
                return
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete course {course_code}?")
            if confirm:
                if self.curriculum_manager.delete_course(course_code):
                    messagebox.showinfo("Success", f"Course {course_code} deleted.")
                    # Clear fields and refresh
                    self.course_code.delete(0, tk.END)
                    self.course_name.delete(0, tk.END)
                    self.course_credits.delete(0, tk.END)
                    self.course_desc.delete("1.0", tk.END)
                    self.course_is_core.set(False)
                    self.course_dept.set('')
                    self.refresh_courses()
                    self.update_course_comboboxes()
                else:
                    messagebox.showerror("Error", f"Course {course_code} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete course: {str(e)}")

    def refresh_courses(self):
        # Clear treeview
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        courses = self.curriculum_manager.list_courses()
        for course in courses:
            self.course_tree.insert("", tk.END, values=(
                course.course_code,
                course.course_name,
                course.credits,
                course.department,
                "Yes" if course.is_core else "No",
                len(course.students_enrolled) # Count of enrolled students
            ))
        self.update_course_comboboxes() # Update comboboxes after refresh

    def update_course_comboboxes(self):
        """Updates comboboxes that list course codes."""
        course_codes = [c.course_code for c in self.curriculum_manager.list_courses()]
        if hasattr(self, 'plan_course'):
            self.plan_course['values'] = course_codes
        if hasattr(self, 'content_course'):
            self.content_course['values'] = course_codes
        if hasattr(self, 'assign_course_code_entry'):
            self.assign_course_code_entry['values'] = course_codes
        if hasattr(self, 'feedback_course'):
            self.feedback_course['values'] = course_codes
        if hasattr(self, 'assign_course'): # From LMS tab
            self.assign_course['values'] = course_codes
        if hasattr(self, 'quiz_course'): # From LMS tab
            self.quiz_course['values'] = course_codes

    # Study Planning Methods
    def add_to_plan(self):
        try:
            student_id = self.plan_student_id.get()
            semester = self.plan_semester.get()
            course_code = self.plan_course.get()

            if not all([student_id, semester, course_code]):
                messagebox.showwarning("Input Error", "Student ID, Semester, and Course are required.")
                return

            # Check if student and course exist (Controller could do this, but direct calls are simpler here)
            if not self.student_manager.student_exists(student_id):
                messagebox.showerror("Error", f"Student {student_id} not found.")
                return
            if not self.curriculum_manager.get_course(course_code):
                messagebox.showerror("Error", f"Course {course_code} not found.")
                return

            self.student_planner.add_course_to_plan(student_id, semester, course_code)
            messagebox.showinfo("Success", f"Course {course_code} added to plan for {student_id} in {semester}.")
            self.refresh_study_plan_display() # Refresh display immediately
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course to plan: {str(e)}")

    def refresh_study_plan_display(self):
        self.plan_display_text.delete("1.0", tk.END)
        student_id = self.plan_student_id.get()
        if not student_id:
            self.plan_display_text.insert(tk.END, "Enter Student ID to view plan.")
            return
        
        plan = self.student_planner.get_study_plan(student_id)
        if not plan:
            self.plan_display_text.insert(tk.END, f"No study plan found for {student_id}.")
            return
        
        for semester, courses in plan.items():
            self.plan_display_text.insert(tk.END, f"--- {semester} ---\n")
            if courses:
                for course in courses:
                    self.plan_display_text.insert(tk.END, f"- {course}\n")
            else:
                self.plan_display_text.insert(tk.END, "  No courses planned.\n")
            self.plan_display_text.insert(tk.END, "\n")

    # -----------------------------------------------------
    # LMS Tab Methods
    # -----------------------------------------------------
    def add_lms_content(self):
        try:
            course_code = self.content_course.get()
            title = self.content_title.get()
            content_type_str = self.content_type.get()
            url_or_path = self.content_url.get()
            description = self.content_desc.get("1.0", tk.END).strip()
            
            if not all([course_code, title, content_type_str, url_or_path]):
                messagebox.showwarning("Input Error", "Course Code, Title, Type, and URL/Path are required.")
                return

            content_type = ContentType(content_type_str)
            content_id = f"CONT_{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Simple unique ID
            
            new_content = LMSContent(content_id, course_code, title, content_type, url_or_path, description)
            self.lms_manager.add_content(new_content)
            messagebox.showinfo("Success", f"Content '{title}' added successfully for {course_code}.")
            
            # Clear fields
            self.content_course.set('')
            self.content_title.delete(0, tk.END)
            self.content_type.set('')
            self.content_url.delete(0, tk.END)
            self.content_desc.delete("1.0", tk.END)
            
            self.refresh_lms_content()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add LMS content: {str(e)}")

    def refresh_lms_content(self):
        self.content_list_display.delete("1.0", tk.END)
        course_code = self.content_course.get() # Use the combobox to filter
        
        if not course_code:
            self.content_list_display.insert(tk.END, "Select a course to view its content.")
            return

        contents = self.lms_manager.get_course_content(course_code)
        if not contents:
            self.content_list_display.insert(tk.END, f"No content found for course {course_code}.")
            return
        
        for item in contents:
            self.content_list_display.insert(tk.END, f"ID: {item.content_id}\n")
            self.content_list_display.insert(tk.END, f"Title: {item.title}\n")
            self.content_list_display.insert(tk.END, f"Type: {item.content_type.value}\n")
            self.content_list_display.insert(tk.END, f"URL/Path: {item.url_or_path}\n")
            self.content_list_display.insert(tk.END, f"Description: {item.description if item.description else 'N/A'}\n")
            self.content_list_display.insert(tk.END, f"Views: {item.views}\n")
            self.content_list_display.insert(tk.END, "-"*30 + "\n")

    def create_assignment(self):
        try:
            course_code = self.assign_course.get()
            title = self.assign_title.get()
            description = "Assignment description placeholder." # Simplified for demo
            due_date = self.assign_due.get()
            max_points_str = self.assign_points.get()
            
            if not all([course_code, title, due_date, max_points_str]):
                messagebox.showwarning("Input Error", "Course Code, Title, Due Date, and Max Points are required.")
                return

            max_points = float(max_points_str)
            assignment_id = f"ASSIGN_{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Unique ID
            
            new_assignment = Assignment(assignment_id, course_code, title, description, due_date, max_points)
            self.lms_manager.create_assignment(new_assignment)
            messagebox.showinfo("Success", f"Assignment '{title}' created for {course_code}.")
            
            # Clear fields
            self.assign_course.set('')
            self.assign_title.delete(0, tk.END)
            self.assign_due.delete(0, tk.END)
            self.assign_points.delete(0, tk.END)
            
            self.refresh_assignment_display()
        except ValueError:
            messagebox.showerror("Input Error", "Max Points must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create assignment: {str(e)}")

    def create_sample_quiz(self):
        try:
            course_code = self.quiz_course.get()
            title = self.quiz_title.get()
            
            if not all([course_code, title]):
                messagebox.showwarning("Input Error", "Course Code and Quiz Title are required.")
                return
            
            quiz_id = f"QUIZ_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            # Sample questions
            sample_questions = [
                {"question": "What is Python?", "options": ["A snake", "A programming language", "A type of food", "A car"], "correct_answer": 1},
                {"question": "What symbol is used for comments?", "options": ["//", "#", "/*", "<!--"], "correct_answer": 1},
                {"question": "Which is a Python data type?", "options": ["int", "string", "list", "All of the above"], "correct_answer": 3}
            ]
            
            new_quiz = Quiz(quiz_id, course_code, title, sample_questions)
            self.lms_manager.create_quiz(new_quiz)
            messagebox.showinfo("Success", f"Sample Quiz '{title}' created for {course_code}.")
            
            # Clear fields
            self.quiz_course.set('')
            self.quiz_title.delete(0, tk.END)
            
            self.refresh_assignment_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create quiz: {str(e)}")

    def refresh_assignment_display(self):
        self.assignment_display.delete("1.0", tk.END)
        # Display assignments and quizzes from LMS
        # This is a simplified display; a real app would list per course or by type
        self.assignment_display.insert(tk.END, "--- Assignments ---\n")
        # Placeholder: In a real app, you'd fetch assignments per course.
        self.assignment_display.insert(tk.END, "Example: Python Basics Assignment (CS101) - Due 2024-12-15\n")
        self.assignment_display.insert(tk.END, "Example: Data Structures HW1 (CS201) - Due 2025-01-10\n\n")

        self.assignment_display.insert(tk.END, "--- Quizzes ---\n")
        # Placeholder: In a real app, you'd fetch quizzes per course.
        self.assignment_display.insert(tk.END, "Example: Python Fundamentals Quiz (CS101)\n")
        self.assignment_display.insert(tk.END, "Example: Circuits Quiz 1 (EE201)\n")

    # -----------------------------------------------------
    # Student Portal Tab Methods
    # -----------------------------------------------------
    def update_student_portal_comboboxes(self):
        student_ids = self.get_student_ids()
        if hasattr(self, 'portal_student'):
            self.portal_student['values'] = student_ids
            if student_ids:
                self.portal_student.set(student_ids[0]) # Set default value

    def load_student_portal(self):
        student_id = self.portal_student.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please select a student.")
            return

        self.load_student_grades(student_id)
        self.load_student_course_content(student_id)
        # Update feedback combobox with courses the student is enrolled in
        self.update_feedback_course_combobox(student_id)

    def load_student_grades(self, student_id):
        self.grades_display.delete("1.0", tk.END)
        grades_data = {}
        try:
            # Iterate through all courses and get gradebook if student is enrolled
            student_courses = self.curriculum_manager.get_student_courses(student_id)
            if not student_courses:
                self.grades_display.insert(tk.END, "Student is not enrolled in any courses.")
                return
                
            for course in student_courses:
                course_code = course.course_code
                gradebook = self.lms_manager.get_gradebook(course_code)
                student_grades = gradebook.get_student_grades(student_id)
                if student_grades and student_grades.get("assignments"): # Only display if there are grades
                    grades_data[course_code] = student_grades
                    
            if not grades_data:
                self.grades_display.insert(tk.END, "No grades available yet for this student.")
                return
                
            for course_code, grades in grades_data.items():
                self.grades_display.insert(tk.END, f"--- Course: {course_code} ---\n")
                self.grades_display.insert(tk.END, f"Final Grade: {grades.get('final_grade', 'N/A'):.2f}\n\n")
                
                self.grades_display.insert(tk.END, "Assignments:\n")
                for assign_id, details in grades.get('assignments', {}).items():
                    self.grades_display.insert(tk.END, f"  - {assign_id}: {details.get('grade', 'N/A')}/{details.get('max', 'N/A')}\n")
                self.grades_display.insert(tk.END, "\n")

                self.grades_display.insert(tk.END, "Quizzes:\n")
                for quiz_id, details in grades.get('quizzes', {}).items():
                    self.grades_display.insert(tk.END, f"  - {quiz_id}: {details.get('grade', 'N/A')}/{details.get('max', 'N/A')}\n")
                self.grades_display.insert(tk.END, "\n")

                self.grades_display.insert(tk.END, "Exams:\n")
                for exam_id, details in grades.get('exams', {}).items():
                    self.grades_display.insert(tk.END, f"  - {exam_id}: {details.get('grade', 'N/A')}/{details.get('max', 'N/A')}\n")
                self.grades_display.insert(tk.END, "\n" + "="*40 + "\n\n")
                
        except Exception as e:
            self.grades_display.insert(tk.END, f"Error loading grades: {e}")

    def load_student_course_content(self, student_id):
        self.portal_content_display.delete("1.0", tk.END)
        student_courses = self.curriculum_manager.get_student_courses(student_id)
        if not student_courses:
            self.portal_content_display.insert(tk.END, "Student is not enrolled in any courses.")
            return

        for course in student_courses:
            self.portal_content_display.insert(tk.END, f"--- Course: {course.course_code} ({course.course_name}) ---\n")
            course_content = self.lms_manager.get_course_content(course.course_code)
            if course_content:
                for item in course_content:
                    self.portal_content_display.insert(tk.END, f"  - {item.title} ({item.content_type.value}): {item.url_or_path}\n")
            else:
                self.portal_content_display.insert(tk.END, "  No content available for this course.\n")
            self.portal_content_display.insert(tk.END, "\n")

    def update_feedback_course_combobox(self, student_id):
        """Populates the feedback course combobox with courses the student is enrolled in."""
        student_courses = self.curriculum_manager.get_student_courses(student_id)
        course_codes = [course.course_code for course in student_courses]
        self.feedback_course['values'] = course_codes
        if course_codes:
            self.feedback_course.set(course_codes[0]) # Set default to the first course

    def submit_feedback(self):
        try:
            student_id = self.portal_student.get() # Use the selected student in the portal
            course_code = self.feedback_course.get()
            rating_str = self.feedback_rating.get()
            feedback_text = self.feedback_text.get("1.0", tk.END).strip()
            
            if not all([student_id, course_code, rating_str]):
                messagebox.showwarning("Input Error", "Please select a student, course, and rating.")
                return
                
            rating = int(rating_str)
            
            # Get the feedback object for the course
            course_feedback = self.lms_manager.get_feedback(course_code)
            # Add the feedback
            course_feedback.add_feedback(student_id, feedback_text, rating)
            # Save the updated feedback object
            self.lms_manager.save_feedback(course_feedback)
            
            messagebox.showinfo("Success", "Feedback submitted successfully!")
            
            # Clear fields
            self.feedback_rating.set('')
            self.feedback_text.delete("1.0", tk.END)
            self.refresh_feedback_display(course_code) # Refresh display for the submitted course
        except ValueError:
            messagebox.showerror("Input Error", "Rating must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit feedback: {str(e)}")

    def refresh_feedback_display(self, course_code=None):
        self.feedback_display.delete("1.0", tk.END)
        if not course_code:
            self.feedback_display.insert(tk.END, "Select a course to view feedback.")
            return

        try:
            course_feedback = self.lms_manager.get_feedback(course_code)
            if not course_feedback.feedbacks:
                self.feedback_display.insert(tk.END, f"No feedback available for {course_code} yet.")
                return

            avg_rating = course_feedback.get_average_rating()
            self.feedback_display.insert(tk.END, f"Average Rating: {avg_rating:.2f}\n\n")
            
            for fb in course_feedback.feedbacks:
                self.feedback_display.insert(tk.END, f"Student: {fb['student_id']}\n")
                self.feedback_display.insert(tk.END, f"Rating: {fb['rating']}/5\n")
                self.feedback_display.insert(tk.END, f"Date: {fb['date']}\n")
                self.feedback_display.insert(tk.END, f"Feedback: {fb['feedback']}\n")
                self.feedback_display.insert(tk.END, "-"*30 + "\n")
        except Exception as e:
            self.feedback_display.insert(tk.END, f"Error loading feedback: {e}")
        
    # -----------------------------------------------------
    # Dashboard Tab
    # -----------------------------------------------------
    def refresh_dashboard(self):
        self.dashboard_display.delete(1.0, tk.END)
        
        self.dashboard_display.insert(tk.END, "--- System Overview ---\n\n")
        
        # Classroom Stats
        self.dashboard_display.insert(tk.END, f"Total Classrooms: {len(self.scheduler.classrooms)}\n")
        under_maintenance = sum(1 for room in self.scheduler.classrooms if room.is_under_maintenance)
        self.dashboard_display.insert(tk.END, f"Classrooms Under Maintenance: {under_maintenance}\n")
        self.dashboard_display.insert(tk.END, f"Current Reservations: {len(self.scheduler.reservations)}\n\n")
        
        # Student Stats
        students = self.student_manager.list_students()
        self.dashboard_display.insert(tk.END, f"Total Registered Students: {len(students)}\n")
        enrolled_students = sum(1 for s in students if s.get('status', 'enrolled') == 'enrolled')
        self.dashboard_display.insert(tk.END, f"Enrolled Students: {enrolled_students}\n\n")
        
        # Course Stats
        courses = self.curriculum_manager.list_courses()
        self.dashboard_display.insert(tk.END, f"Total Courses in Catalogue: {len(courses)}\n")
        core_courses = len([c for c in courses if c.is_core])
        self.dashboard_display.insert(tk.END, f"Core Courses: {core_courses}\n\n")
        
        # Equipment Stats
        total_equipment = len(self.eq_manager.equipment_list)
        allocated_equipment = sum(1 for eq in self.eq_manager.track_equipment() if eq['allocated'])
        self.dashboard_display.insert(tk.END, f"Total Equipment: {total_equipment}\n")
        self.dashboard_display.insert(tk.END, f"Allocated Equipment: {allocated_equipment}\n\n")
        
        # License Stats
        total_licenses = len(self.license_manager.licenses)
        total_seats_available = sum(lic['total_seats'] - lic['used_seats'] for lic in self.license_manager.track_licenses().values())
        self.dashboard_display.insert(tk.END, f"Total Software Licenses: {total_licenses}\n")
        self.dashboard_display.insert(tk.END, f"Total Available License Seats: {total_seats_available}\n\n")

        # Professor Stats
        professors = self.staff_manager.get_all_professors()
        self.dashboard_display.insert(tk.END, f"Total Professors: {len(professors)}\n")
        # Assign course count could be complex, simplified here
        courses_assigned = sum(len(p.get('courses_taught', [])) for p in professors)
        self.dashboard_display.insert(tk.END, f"Total Courses Assigned to Professors: {courses_assigned}\n\n")

        self.dashboard_display.insert(tk.END, "\n--- End of Overview ---\n")


    # -----------------------------------------------------
    # Helper methods for GUI updates (e.g., comboboxes)
    # -----------------------------------------------------
    def update_comboboxes(self):
        """Updates all comboboxes across the GUI."""
        self.update_student_comboboxes()
        self.update_course_comboboxes()
        self.refresh_classroom_info() # This implicitly updates classroom comboboxes
        self.refresh_equipment_info() # This implicitly updates equipment comboboxes
        self.refresh_license_info() # This implicitly updates license comboboxes
        self.refresh_lab_equipment_info() # This implicitly updates lab equipment comboboxes
        self.refresh_people_info() # This implicitly updates person related comboboxes
        self.update_student_portal_comboboxes() # Explicitly update student portal combobox
        # Add these helper methods to the UniversityManagementGUI class:

def get_student_from_db_gui(self):
    """Get student from database"""
    student_id = self.db_student_id.get()
    if not student_id:
        messagebox.showwarning("Input Error", "Please enter Student ID")
        return
    
    try:
        student = self.controller.get_student_from_db(student_id)
        
        self.db_query_display.delete(1.0, tk.END)
        if student:
            self.db_query_display.insert(tk.END, "=== STUDENT FROM DATABASE ===\n\n")
            for key, value in student.items():
                self.db_query_display.insert(tk.END, f"{key}: {value}\n")
        else:
            self.db_query_display.insert(tk.END, f"Student {student_id} not found in database")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to get student: {str(e)}")
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, f"Error: {str(e)}")

def get_course_from_db_gui(self):
    """Get course from database"""
    course_code = self.db_course_code.get()
    if not course_code:
        messagebox.showwarning("Input Error", "Please enter Course Code")
        return
    
    try:
        course = self.controller.get_course_details_from_db(course_code)
        
        self.db_query_display.delete(1.0, tk.END)
        if course:
            self.db_query_display.insert(tk.END, "=== COURSE FROM DATABASE ===\n\n")
            for key, value in course.items():
                self.db_query_display.insert(tk.END, f"{key}: {value}\n")
        else:
            self.db_query_display.insert(tk.END, f"Course {course_code} not found in database")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to get course: {str(e)}")
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, f"Error: {str(e)}")

def generate_enrollment_report_gui(self):
    """Generate enrollment report"""
    try:
        report = self.controller.generate_enrollment_report_db()
        
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, "=== ENROLLMENT REPORT ===\n\n")
        self.db_query_display.insert(tk.END, f"Total Students: {report['total_students']}\n")
        self.db_query_display.insert(tk.END, f"Total Courses: {report['total_courses']}\n\n")
        self.db_query_display.insert(tk.END, "=== By Department ===\n")
        for dept in report['department_stats']:
            self.db_query_display.insert(tk.END, f"{dept['department']}: {dept['student_count']} students\n")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to generate report: {str(e)}")
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, f"Error: {str(e)}")

def generate_maintenance_report_gui(self):
    """Generate maintenance report"""
    try:
        report = self.controller.generate_maintenance_report_db()
        
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, "=== MAINTENANCE REPORT ===\n\n")
        self.db_query_display.insert(tk.END, f"Total Reports: {report['total_reports']}\n")
        self.db_query_display.insert(tk.END, f"Resolved: {report['resolved']}\n")
        self.db_query_display.insert(tk.END, f"Pending: {report['pending']}\n\n")
        self.db_query_display.insert(tk.END, "=== By Classroom ===\n")
        for classroom in report['classroom_reports']:
            self.db_query_display.insert(tk.END, 
                f"{classroom['classroom_id']} ({classroom['location']}): {classroom['report_count']} reports\n")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to generate report: {str(e)}")
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, f"Error: {str(e)}")

def list_all_students_db_gui(self):
    """List all students from database"""
    try:
        students = self.controller.get_all_students_from_db()
        
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, "=== ALL STUDENTS IN DATABASE ===\n\n")
        for student in students:
            self.db_query_display.insert(tk.END, f"ID: {student['student_id']}\n")
            self.db_query_display.insert(tk.END, f"Name: {student['first_name']} {student['last_name']}\n")
            self.db_query_display.insert(tk.END, f"Department: {student['department']}\n")
            self.db_query_display.insert(tk.END, f"Status: {student['status']}\n")
            self.db_query_display.insert(tk.END, f"Email: {student.get('email', 'N/A')}\n")
            self.db_query_display.insert(tk.END, "-" * 40 + "\n")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to list students: {str(e)}")
        self.db_query_display.delete(1.0, tk.END)
        self.db_query_display.insert(tk.END, f"Error: {str(e)}")

def create_license_eav_gui(self):
    """Create license using EAV"""
    license_id = self.license_id_entry.get()
    name = self.license_name_entry.get()
    seats_str = self.license_seats_entry.get()
    
    if not all([license_id, name, seats_str]):
        messagebox.showwarning("Input Error", "All license fields are required")
        return
    
    try:
        seats = int(seats_str)
        result = self.controller.create_software_license(license_id, name, seats)
        messagebox.showinfo("Success", result)
        
        # Clear fields
        self.license_id_entry.delete(0, tk.END)
        self.license_name_entry.delete(0, tk.END)
        self.license_seats_entry.delete(0, tk.END)
        
    except ValueError as e:
        messagebox.showerror("Input Error", f"Seats must be a number: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create license: {str(e)}")

def create_announcement_eav_gui(self):
    """Create announcement using EAV"""
    title = self.announcement_title_entry.get()
    content = self.announcement_content_entry.get("1.0", tk.END).strip()
    target_type = self.announcement_target_type.get()
    target_value = self.announcement_target_value.get()
    
    if not all([title, content, target_type]):
        messagebox.showwarning("Input Error", "Title, Content, and Target Type are required")
        return
    
    try:
        result = self.controller.create_announcement(title, content, target_type, target_value)
        messagebox.showinfo("Success", result)
        
        # Clear fields
        self.announcement_title_entry.delete(0, tk.END)
        self.announcement_content_entry.delete("1.0", tk.END)
        self.announcement_target_value.delete(0, tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create announcement: {str(e)}")

def list_announcements_gui(self):
    """List all announcements"""
    try:
        announcements = self.controller.get_all_announcements()
        
        self.eav_display.delete(1.0, tk.END)
        if not announcements:
            self.eav_display.insert(tk.END, "No announcements found")
            return
        
        for ann in announcements:
            self.eav_display.insert(tk.END, f"Title: {ann['name']}\n")
            self.eav_display.insert(tk.END, f"Type: {ann['entity_type']}\n")
            for key, value in ann['properties'].items():
                self.eav_display.insert(tk.END, f"  {key}: {value}\n")
            self.eav_display.insert(tk.END, "-" * 40 + "\n")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to list announcements: {str(e)}")
        self.eav_display.delete(1.0, tk.END)
        self.eav_display.insert(tk.END, f"Error: {str(e)}")


# --- Sample Data Initialization ---
# This function will be called within setup_managers, which is now called by the Controller.
# The Controller initializes managers with persistence, so sample data will be loaded from files if they exist.
# If running for the first time, this will seed the data.

def initialize_system_with_sample_data(controller: UniversityController):
    """
    Seeds the system with sample data if data files are missing or empty.
    """
    print("Initializing system with sample data if files are missing or empty...")

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

    # Sample Equipment - FIXED
    if not controller.equipment_mgr.equipment_list:
        print("  - Adding sample equipment...")
        try:
            controller.equipment_mgr.add_equipment(Equipment("E001", "Projector", "AV"))
            controller.equipment_mgr.add_equipment(Equipment("E002", "Whiteboard", "Stationery"))
            controller.equipment_mgr.add_equipment(Equipment("E003", "Sound System", "AV"))
            print("    Sample equipment added.")
        except Exception as e:
            print(f"    Error adding sample equipment: {e}")

    # Sample Lab Equipment - FIXED
    if not controller.lab_eq_mgr.lab_equipment:
        print("  - Adding sample lab equipment...")
        try:
            controller.lab_eq_mgr.add_lab_equipment(Equipment("L001", "Microscope", "Biology"))
            controller.lab_eq_mgr.add_lab_equipment(Equipment("L002", "Centrifuge", "Chemistry"))
            print("    Sample lab equipment added.")
        except Exception as e:
            print(f"    Error adding sample lab equipment: {e}")

    # Sample Licenses - FIXED
    if not controller.license_mgr.licenses:
        print("  - Adding sample licenses...")
        try:
            controller.license_mgr.add_license(SoftwareLicense("S001", "DesignSuite", 10))
            controller.license_mgr.add_license(SoftwareLicense("S002", "ProgrammingIDE", 5))
            print("    Sample licenses added.")
        except Exception as e:
            print(f"    Error adding sample licenses: {e}")
            
    # Sample Staff (Professors)
    if not controller.staff_mgr.professors:
        print("  - Adding sample professors...")
        try:
            controller.staff_mgr.add_professor("P001", "Dr. Emily Carter", "Computer Engineering", "emily.carter@uni.edu")
            controller.staff_mgr.add_professor("P002", "Prof. John Smith", "Mechanical Engineering", "john.smith@uni.edu")
            print("    Sample professors added.")
        except Exception as e:
            print(f"    Error adding sample professors: {e}")

    # Ensure sample students exist (add missing ones even if some records exist)
    print("  - Ensuring sample students exist...")
    sample_students = [
        {"student_id": "001", "first_name": "Maria", "last_name": "Ibraheem", 
            "department": "Computer Engineering", "enrollment_year": 2019, "email": "maria@example.edu",
            "gpa": 2.2, "status": "enrolled"},
        {"student_id": "002", "first_name": "Mark", "last_name": "Magdy", 
            "department": "Mechanical Engineering", "enrollment_year": 2020, "email": "mark@example.edu",
            "gpa": 3.5, "status": "enrolled"},
        {"student_id": "007", "first_name": "James", "last_name": "Bond", 
            "department": "Spy School", "enrollment_year": 2021}
    ]
    any_added = False
    for s in sample_students:
        try:
            if not controller.student_mgr.student_exists(s["student_id"]):
                controller.student_mgr.add_student(s)
                print(f"    Added sample student {s['student_id']}")
                any_added = True
        except Exception as e:
            print(f"    Error adding sample student {s.get('student_id')}: {e}")
    if not any_added:
        print("    Sample students already present or none needed.")

    # Sample Curriculum Data
    if not controller.curriculum_mgr.list_courses():
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
                controller.curriculum_mgr.add_course(course)
            print("    Sample courses added.")
        except Exception as e:
            print(f"    Error adding sample courses: {e}")

    # Sample Student Enrollments & Plan (robust checks)
    try:
        # Enroll students if not already enrolled (only if student records exist)
        def safe_enroll(sid, course_code):
            if not controller.student_mgr.student_exists(sid):
                print(f"    Skipping enrollment for {sid}: student record not found.")
                return
            course = controller.curriculum_mgr.get_course(course_code)
            if not course:
                print(f"    Skipping enrollment for {sid}: course {course_code} not found.")
                return
            if sid in course.students_enrolled:
                return
            try:
                controller.enroll_student_in_course(sid, course_code)
            except Exception as e:
                print(f"    Could not enroll {sid} in {course_code}: {e}")

        safe_enroll("001", "CS101")
        safe_enroll("002", "CS101")
        safe_enroll("001", "CS201")
        safe_enroll("002", "ME101")

        # Create sample study plans if students exist
        def safe_plan(sid, term, courses):
            if not controller.student_mgr.student_exists(sid):
                print(f"    Skipping study plan for {sid}: student record not found.")
                return
            plan = controller.student_planner.get_study_plan(sid)
            if not plan or term not in plan:
                try:
                    controller.student_planner.create_study_plan(sid, term, courses)
                except Exception as e:
                    print(f"    Could not create study plan for {sid}: {e}")

        safe_plan("001", "Fall 2024", ["CS101", "CS201"])
        safe_plan("002", "Fall 2024", ["CS101", "ME101"])

        print("  - Sample enrollments and study plans setup.")
    except Exception as e:
        print(f"    Error setting up enrollments/plans: {e}")

    # Sample LMS Data
    cs101_content = controller.lms_mgr.get_course_content("CS101")
    if not cs101_content:
        print("  - Adding sample LMS content...")
        try:
            content = LMSContent("CONT_001", "CS101", "Introduction to Python Video", ContentType.VIDEO, "https://example.com/python-intro.mp4", "A basic Python tutorial.")
            controller.lms_mgr.add_content(content)
            
            assignment = Assignment("ASSIGN_001", "CS101", "Python Basics HW", "Complete exercises.", "2024-12-15", 100)
            controller.lms_mgr.create_assignment(assignment)
            
            quiz = Quiz("QUIZ_001", "CS101", "Python Fundamentals Quiz", [{"question": "What is Python?", "options": ["Snake", "Language", "Food"], "correct_answer": 1}])
            controller.lms_mgr.create_quiz(quiz)
            print("    Sample LMS content added.")
        except Exception as e:
            print(f"    Error adding sample LMS content: {e}")
            
    # Sample Gradebook entries
    try:
        # Ensure gradebooks are created/loaded
        gb_cs101 = controller.lms_mgr.get_gradebook("CS101")
        # Add some grades if none exist for student 001
        if "001" not in gb_cs101.grades or not gb_cs101.grades["001"].get("assignments"):
            gb_cs101.add_grade("001", "assignment", "ASSIGN_001", 85)
            gb_cs101.add_grade("001", "quiz", "QUIZ_001", 75)
            controller.lms_mgr.save_gradebook(gb_cs101)
            print("  - Sample grades added for CS101.")
    except Exception as e:
        print(f"    Error adding sample grades: {e}")

# -----------------------------------------------------
# Main GUI Application Class
# -----------------------------------------------------
class UniversityManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated University System v4.0")
        self.root.geometry("1400x900")
        
        # Initialize the Controller which initializes all managers
        self.controller = UniversityController()
        
        # Call a function to seed sample data if needed (e.g., if files don't exist)
        # This is now handled by the Manager initializers loading data, and this function seeds if empty.
        initialize_system_with_sample_data(self.controller)
        
               # Map controller managers to local variables for compatibility with existing GUI code
        self.scheduler = self.controller.scheduler
        self.eq_manager = self.controller.equipment_mgr  # FIXED: equipment_mgr
        self.student_manager = self.controller.student_mgr
        self.curriculum_manager = self.controller.curriculum_mgr
        self.lms_manager = self.controller.lms_mgr
        self.staff_manager = self.controller.staff_mgr
        self.student_planner = self.controller.student_planner
        self.person_manager = self.controller.person_mgr
        
        # ALSO add these for the equipment tabs
        self.eq_manager = self.controller.equipment_mgr  # Alias for backward compatibility
        self.license_manager = self.controller.license_mgr
        self.lab_eq_manager = self.controller.lab_eq_mgr

        # Helper: safely set combobox values only when supported
        def _safe_set(widget, values):
            try:
                if isinstance(widget, ttk.Combobox):
                    widget['values'] = values
            except Exception:
                pass
        # Bind helper as instance method for compatibility with existing calls
        self.safe_set_values = _safe_set

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs - Reordered for a more logical flow
        # Wrap tab creation in try/except so the GUI can launch even if some handlers are incomplete
        try:
            self.create_dashboard_tab()        # Overview first
        except Exception as e:
            print(f"Failed to create dashboard tab: {e}")
        try:
            self.create_student_tab()          # Student info
        except Exception as e:
            print(f"Failed to create student tab: {e}")
        try:
            self.create_staff_tab()            # Staff & Faculty Tab
        except Exception as e:
            print(f"Failed to create staff tab: {e}")
        try:
            self.create_curriculum_tab()       # Courses and Planning
        except Exception as e:
            print(f"Failed to create curriculum tab: {e}")
        try:
            self.create_classroom_tab()        # Scheduling
        except Exception as e:
            print(f"Failed to create classroom tab: {e}")
        try:
            self.create_lms_tab()              # Learning Content & Assessments
        except Exception as e:
            print(f"Failed to create LMS tab: {e}")
        try:
            self.create_equipment_tab()        # Resources
        except Exception as e:
            print(f"Failed to create equipment tab: {e}")
        try:
            self.create_license_tab()
        except Exception as e:
            print(f"Failed to create license tab: {e}")
        try:
            self.create_lab_equipment_tab()
        except Exception as e:
            print(f"Failed to create lab equipment tab: {e}")
        try:
            self.create_people_tab()           # Allocation
        except Exception as e:
            print(f"Failed to create people tab: {e}")
        try:
            self.create_student_portal_tab()   # Student View
        except Exception as e:
            print(f"Failed to create student portal tab: {e}")
        
        # Initial data loading/refreshing for all tabs
        # Wrap some refresh methods with safe wrappers to avoid a single UI issue breaking initialization
        for _name in ['update_course_comboboxes', 'update_student_comboboxes', 'refresh_people_info', 'update_student_portal_comboboxes']:
            _orig = getattr(self, _name, None)
            if callable(_orig):
                def _make_safe(fn, display_name=_name):
                    def _safe_fn():
                        try:
                            return fn()
                        except Exception as e:
                            print(f"Warning: {display_name} raised: {e}")
                    return _safe_fn
                setattr(self, _name, _make_safe(_orig))

        # Ensure widgets expected to be comboboxes are comboboxes (convert Entry -> Combobox when found)
        for _wname in ['assign_course_code_entry', 'portal_student', 'operation_student_id', 'alloc_eq_id', 'alloc_license_id', 'alloc_lab_eq_id', 'assign_prof_id_entry', 'assign_prof_course']:
            try:
                w = getattr(self, _wname, None)
                if w is not None and not isinstance(w, ttk.Combobox):
                    grid_info = w.grid_info() if hasattr(w, 'grid_info') else None
                    parent = w.master if hasattr(w, 'master') else None
                    try:
                        value = w.get()
                    except Exception:
                        value = ''
                    w.destroy()
                    new = ttk.Combobox(parent, values=[])
                    if grid_info:
                        # grid_info may contain strings for some keys; convert keys expected by grid()
                        new.grid(**grid_info)
                    setattr(self, _wname, new)
                    if value:
                        try: new.set(value)
                        except Exception: pass
            except Exception:
                pass

        try:
            self.refresh_all_data()
        except Exception as e:
            print(f"Warning: refresh_all_data encountered an error: {e}")

    def refresh_all_data(self):
        """Calls refresh methods for all relevant tabs in a robust way."""
        methods = [
            'refresh_dashboard', 'list_students', 'refresh_staff', 'refresh_courses',
            'refresh_classroom_info', 'refresh_lms_content', 'refresh_equipment_info',
            'refresh_license_info', 'refresh_lab_equipment_info', 'refresh_people_info',
            'update_student_portal_comboboxes', 'refresh_study_plan_display'
        ]
        for m in methods:
            fn = getattr(self, m, None)
            if callable(fn):
                try:
                    fn()
                except Exception as e:
                    try:
                        print(f"Warning: refresh_all_data encountered an error in {m}: {e}")
                    except Exception:
                        pass

    def setup_managers(self):
        """Removed as managers are now initialized via the Controller."""
        pass

    # -----------------------------------------------------
    # Classroom Tab Methods
    # -----------------------------------------------------
    def create_classroom_tab(self):
        """Create classroom management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Classrooms")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="Classroom Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add Classroom
        ttk.Label(input_frame, text="Classroom ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.classroom_id = ttk.Entry(input_frame)
        self.classroom_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Capacity:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.capacity = ttk.Entry(input_frame)
        self.capacity.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Location:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.location = ttk.Entry(input_frame)
        self.location.grid(row=2, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add Classroom", 
                  command=self.add_classroom).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Maintenance
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select Classroom:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.maintenance_room = ttk.Combobox(input_frame, values=self.get_classroom_ids())
        self.maintenance_room.grid(row=5, column=1, pady=2)
        
        ttk.Label(input_frame, text="Description:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.maintenance_desc = ttk.Entry(input_frame)
        self.maintenance_desc.grid(row=6, column=1, pady=2)
        
        ttk.Button(input_frame, text="Report Maintenance", 
                  command=self.report_maintenance).grid(row=7, column=0, pady=2)
        ttk.Button(input_frame, text="Resolve Maintenance", 
                  command=self.resolve_maintenance).grid(row=7, column=1, pady=2)
        
        # Reservation
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=8, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select Classroom:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.reserve_room = ttk.Combobox(input_frame, values=self.get_classroom_ids())
        self.reserve_room.grid(row=9, column=1, pady=2)
        
        ttk.Label(input_frame, text="Reserved By:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.reserved_by = ttk.Entry(input_frame)
        self.reserved_by.grid(row=10, column=1, pady=2)
        
        ttk.Button(input_frame, text="Make Reservation", 
                  command=self.make_reservation).grid(row=11, column=0, columnspan=2, pady=5)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="Classroom Information", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.classroom_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.classroom_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Classroom Info", 
                  command=self.refresh_classroom_info).pack(pady=5)
        
        self.refresh_classroom_info()

    def get_classroom_ids(self):
        return [room.id for room in self.scheduler.classrooms]
    
    def add_classroom(self):
        try:
            room_id = self.classroom_id.get()
            capacity_str = self.capacity.get()
            location = self.location.get()
            
            if not room_id or not capacity_str:
                messagebox.showwarning("Input Error", "Classroom ID and Capacity are required.")
                return
            
            capacity = int(capacity_str)
            
            self.scheduler.add_classroom(Classroom(id=room_id, capacity=capacity, location=location))
            messagebox.showinfo("Success", f"Classroom {room_id} added successfully!")
            self.classroom_id.delete(0, tk.END)
            self.capacity.delete(0, tk.END)
            self.location.delete(0, tk.END)
            self.refresh_classroom_info()
            # Update combobox values
            self.maintenance_room['values'] = self.get_classroom_ids()
            self.reserve_room['values'] = self.get_classroom_ids()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add classroom: {str(e)}")
    
    def report_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            description = self.maintenance_desc.get()
            
            if not room_id or not description:
                messagebox.showwarning("Input Error", "Please select a classroom and provide a description.")
                return

            result = self.scheduler.report_maintenance(room_id, description)
            messagebox.showinfo("Success", result)
            self.maintenance_desc.delete(0, tk.END)
            self.refresh_classroom_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to report maintenance: {str(e)}")
    
    def resolve_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            if not room_id:
                messagebox.showwarning("Input Error", "Please select a classroom to resolve maintenance.")
                return

            result = self.scheduler.resolve_maintenance(room_id)
            messagebox.showinfo("Success", result)
            self.maintenance_desc.delete(0, tk.END)
            self.refresh_classroom_info()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resolve maintenance: {str(e)}")
    
    def make_reservation(self):
        try:
            room_id = self.reserve_room.get()
            reserved_by = self.reserved_by.get()
            
            if not room_id or not reserved_by:
                messagebox.showwarning("Input Error", "Please select a room and enter who it's reserved by.")
                return

            # For simplicity, reserve for the next hour
            now = datetime.now()
            start_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            
            result = self.scheduler.reserve_classroom(room_id, start_time, end_time, reserved_by)
            messagebox.showinfo("Reservation Status", result)
            self.reserved_by.delete(0, tk.END)
            self.refresh_classroom_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make reservation: {str(e)}")
    
    def refresh_classroom_info(self):
        self.classroom_display.delete(1.0, tk.END)
        if not self.scheduler.classrooms:
            self.classroom_display.insert(tk.END, "No classrooms added yet.")
            return

        info = "=== CLASSROOMS ===\n\n"
        for room in self.scheduler.classrooms:
            info += f"ID: {room.id}\n"
            info += f"Capacity: {room.capacity}\n"
            info += f"Location: {room.location if room.location else 'N/A'}\n"
            info += f"Maintenance: {'YES' if room.is_under_maintenance else 'NO'}\n"
            if room.maintenance_notes:
                info += f"Maintenance Notes: {', '.join(room.maintenance_notes)}\n"
            
            # Show reservations for this room
            room_reservations = [r for r in self.scheduler.reservations if r.classroom_id == room.id]
            if room_reservations:
                info += "Reservations:\n"
                for res in room_reservations:
                    info += f"  - Res ID {res.id} by {res.reserved_by}: {res.start.strftime('%Y-%m-%d %H:%M')} to {res.end.strftime('%H:%M')}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.classroom_display.insert(tk.END, info)
    
    # -----------------------------------------------------
    # Equipment Tab Methods
    def add_equipment(self):
        """Add equipment via EquipmentManager if available; otherwise show a message."""
        try:
            eq_id = self.eq_id.get() if hasattr(self, 'eq_id') else None
            name = self.eq_name.get() if hasattr(self, 'eq_name') else None
            category = self.eq_category.get() if hasattr(self, 'eq_category') else None
            if not all([eq_id, name]):
                messagebox.showwarning("Input Error", "Equipment ID and Name are required.")
                return
            try:
                # Prefer EquipmentManager if available
                if hasattr(self.eq_manager, 'add_equipment'):
                    self.eq_manager.add_equipment({'id': eq_id, 'name': name, 'category': category})
                else:
                    # Fallback: store in dict
                    self.eq_manager.equipment_list[eq_id] = {'name': name, 'category': category, 'allocated': False}
                messagebox.showinfo("Success", f"Equipment {eq_id} added.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add equipment: {e}")
            finally:
                if hasattr(self, 'eq_id'): self.eq_id.delete(0, tk.END)
                if hasattr(self, 'eq_name'): self.eq_name.delete(0, tk.END)
                if hasattr(self, 'eq_category'): self.eq_category.delete(0, tk.END)
                try:
                    self.refresh_equipment_info()
                except Exception:
                    pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add equipment: {e}")

    def allocate_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get() if hasattr(self, 'alloc_eq_id') else None
            to = self.alloc_to.get() if hasattr(self, 'alloc_to') else None
            if not eq_id or not to:
                messagebox.showwarning("Input Error", "Select equipment and enter allocation target.")
                return
            if hasattr(self.eq_manager, 'allocate'):
                self.eq_manager.allocate(eq_id, to)
            else:
                # Simple flag
                if eq_id in self.eq_manager.equipment_list:
                    self.eq_manager.equipment_list[eq_id]['allocated'] = True
            messagebox.showinfo("Success", f"Allocated {eq_id} to {to}.")
            try: self.refresh_equipment_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate equipment: {e}")

    def release_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get() if hasattr(self, 'alloc_eq_id') else None
            if not eq_id:
                messagebox.showwarning("Input Error", "Select equipment to release.")
                return
            if hasattr(self.eq_manager, 'release'):
                self.eq_manager.release(eq_id)
            else:
                if eq_id in self.eq_manager.equipment_list:
                    self.eq_manager.equipment_list[eq_id]['allocated'] = False
            messagebox.showinfo("Success", f"Released equipment {eq_id}.")
            try: self.refresh_equipment_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release equipment: {e}")

    def refresh_equipment_info(self):
        try:
            self.equipment_display.delete(1.0, tk.END)
            if not hasattr(self.eq_manager, 'equipment_list') or not self.eq_manager.equipment_list:
                self.equipment_display.insert(tk.END, "No equipment found.")
                return
            for eid, info in self.eq_manager.equipment_list.items():
                # Support both dict (older code) and Equipment objects
                if isinstance(info, dict):
                    name = info.get('name')
                    category = info.get('category')
                    allocated = info.get('allocated', False)
                else:
                    name = getattr(info, 'name', str(info))
                    category = getattr(info, 'category', '')
                    allocated = getattr(info, 'is_allocated', False)
                self.equipment_display.insert(tk.END, f"ID: {eid} | Name: {name} | Category: {category} | Allocated: {allocated}\n")
        except Exception as e:
            # Avoid crashing on refresh
            try:
                self.equipment_display.insert(tk.END, f"Error loading equipment: {e}")
            except Exception:
                pass
    # -----------------------------------------------------
    def create_equipment_tab(self):
        """Create equipment management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Equipment")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="Equipment Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add Equipment
        ttk.Label(input_frame, text="Equipment ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.eq_id = ttk.Entry(input_frame)
        self.eq_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.eq_name = ttk.Entry(input_frame)
        self.eq_name.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.eq_category = ttk.Entry(input_frame)
        self.eq_category.grid(row=2, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add Equipment", 
                  command=self.add_equipment).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Allocate/Release
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select Equipment:").grid(row=5, column=0, sticky=tk.W, pady=2)
        # Use safe getter in case methods aren't yet attached during initialization
        alloc_eq_values = getattr(self, 'get_equipment_ids', lambda: [])()
        self.alloc_eq_id = ttk.Combobox(input_frame, values=alloc_eq_values)
        self.alloc_eq_id.grid(row=5, column=1, pady=2)
        
        ttk.Label(input_frame, text="Allocate To:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.alloc_to = ttk.Entry(input_frame)
        self.alloc_to.grid(row=6, column=1, pady=2)
        
        ttk.Button(input_frame, text="Allocate Equipment", 
                  command=self.allocate_equipment).grid(row=7, column=0, pady=2)
        ttk.Button(input_frame, text="Release Equipment", 
                  command=self.release_equipment).grid(row=7, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="Equipment Status", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.equipment_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.equipment_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Equipment Info", 
                  command=self.refresh_equipment_info).pack(pady=5)
        
        self.refresh_equipment_info()
    
    # -----------------------------------------------------
    # License Tab Methods
    def add_license(self):
        try:
            lic_id = self.license_id.get() if hasattr(self, 'license_id') else None
            name = self.software_name.get() if hasattr(self, 'software_name') else None
            seats = self.total_seats.get() if hasattr(self, 'total_seats') else None
            if not lic_id or not name or not seats:
                messagebox.showwarning("Input Error", "License ID, Name, and Total Seats are required.")
                return
            try:
                seats_int = int(seats)
                if hasattr(self.license_manager, 'create_license'):
                    self.license_manager.create_license(lic_id, name, seats_int)
                else:
                    self.license_manager.licenses[lic_id] = {'name': name, 'total_seats': seats_int, 'used_seats': 0}
                messagebox.showinfo("Success", f"License {lic_id} added.")
            except ValueError:
                messagebox.showerror("Input Error", "Total seats must be a number.")
            finally:
                if hasattr(self, 'license_id'): self.license_id.delete(0, tk.END)
                if hasattr(self, 'software_name'): self.software_name.delete(0, tk.END)
                if hasattr(self, 'total_seats'): self.total_seats.delete(0, tk.END)
                try: self.refresh_license_info()
                except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add license: {e}")

    def allocate_license(self):
        try:
            lic = self.alloc_license_id.get() if hasattr(self, 'alloc_license_id') else None
            if not lic:
                messagebox.showwarning("Input Error", "Select a license to allocate.")
                return
            if hasattr(self.license_manager, 'allocate_seat'):
                self.license_manager.allocate_seat(lic)
            else:
                self.license_manager.licenses[lic]['used_seats'] += 1
            messagebox.showinfo("Success", f"Allocated a seat from {lic}.")
            try: self.refresh_license_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate license: {e}")

    def release_license(self):
        try:
            lic = self.alloc_license_id.get() if hasattr(self, 'alloc_license_id') else None
            if not lic:
                messagebox.showwarning("Input Error", "Select a license to release.")
                return
            if hasattr(self.license_manager, 'release_seat'):
                self.license_manager.release_seat(lic)
            else:
                self.license_manager.licenses[lic]['used_seats'] = max(0, self.license_manager.licenses[lic]['used_seats'] - 1)
            messagebox.showinfo("Success", f"Released a seat from {lic}.")
            try: self.refresh_license_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release license: {e}")

    def refresh_license_info(self):
        try:
            self.license_display.delete(1.0, tk.END)
            if not hasattr(self.license_manager, 'licenses') or not self.license_manager.licenses:
                self.license_display.insert(tk.END, "No licenses found.")
                return

            # Prefer a manager-provided tracked view, but fall back to the internal dict
            try:
                tracked = self.license_manager.track_licenses()
                if isinstance(tracked, dict):
                    entries = list(tracked.items())
                else:
                    # list of dicts or objects
                    entries = []
                    for lic in tracked:
                        if isinstance(lic, dict):
                            lid = lic.get('license_id') or lic.get('id') or 'N/A'
                            entries.append((lid, lic))
                        else:
                            lid = getattr(lic, 'license_id', None) or getattr(lic, 'license_id', 'N/A')
                            entries.append((lid, lic))
            except Exception:
                entries = list(self.license_manager.licenses.items())

            for lid, data in entries:
                if isinstance(data, dict):
                    name = data.get('name')
                    used = data.get('used_seats', '?')
                    total = data.get('total_seats', '?')
                else:
                    name = getattr(data, 'name', str(data))
                    used = getattr(data, 'used_seats', '?')
                    total = getattr(data, 'total_seats', '?')
                self.license_display.insert(tk.END, f"ID: {lid} | Name: {name} | Total: {total} | Used: {used}\n")
        except Exception as e:
            try: self.license_display.insert(tk.END, f"Error: {e}")
            except Exception: pass
    # -----------------------------------------------------
    def create_license_tab(self):
        """Create software license management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Licenses")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="License Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add License
        ttk.Label(input_frame, text="License ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.license_id = ttk.Entry(input_frame)
        self.license_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Software Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.software_name = ttk.Entry(input_frame)
        self.software_name.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Total Seats:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.total_seats = ttk.Entry(input_frame)
        self.total_seats.grid(row=2, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add License", 
                  command=self.add_license).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Allocate/Release
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select License:").grid(row=5, column=0, sticky=tk.W, pady=2)
        alloc_license_values = getattr(self, 'get_license_ids', lambda: [])()
        self.alloc_license_id = ttk.Combobox(input_frame, values=alloc_license_values)
        self.alloc_license_id.grid(row=5, column=1, pady=2)
        
        ttk.Button(input_frame, text="Allocate Seat", 
                  command=self.allocate_license).grid(row=6, column=0, pady=2)
        ttk.Button(input_frame, text="Release Seat", 
                  command=self.release_license).grid(row=6, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="License Status", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.license_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.license_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh License Info", 
                  command=self.refresh_license_info).pack(pady=5)
        
        self.refresh_license_info()
    
    # -----------------------------------------------------
    # Lab Equipment Tab Methods (consolidated robust implementation)
    def add_lab_equipment(self):
        try:
            lab_id = self.lab_eq_id.get() if hasattr(self, 'lab_eq_id') else None
            name = self.lab_eq_name.get() if hasattr(self, 'lab_eq_name') else None
            category = self.lab_eq_category.get() if hasattr(self, 'lab_eq_category') else None
            if not lab_id or not name:
                messagebox.showwarning("Input Error", "Equipment ID and Name are required.")
                return
            # Create Equipment object and register with manager
            self.lab_eq_manager.add_lab_equipment(Equipment(lab_id, name, category))
            messagebox.showinfo("Success", f"Lab Equipment {lab_id} added.")
            try:
                if hasattr(self, 'lab_eq_id'): self.lab_eq_id.delete(0, tk.END)
                if hasattr(self, 'lab_eq_name'): self.lab_eq_name.delete(0, tk.END)
                if hasattr(self, 'lab_eq_category'): self.lab_eq_category.delete(0, tk.END)
            except Exception:
                pass
            try: self.refresh_lab_equipment_info()
            except Exception: pass
            try: self.safe_set_values(self.alloc_lab_eq_id, self.get_lab_equipment_ids())
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add lab equipment: {e}")

    def allocate_lab_equipment(self):
        try:
            eq = self.alloc_lab_eq_id.get() if hasattr(self, 'alloc_lab_eq_id') else None
            target = self.alloc_lab_to.get() if hasattr(self, 'alloc_lab_to') else None
            if not eq or not target:
                messagebox.showwarning("Input Error", "Select equipment and enter a target.")
                return
            self.lab_eq_manager.allocate_lab_equipment(eq, target)
            messagebox.showinfo("Success", f"Allocated {eq} to {target}.")
            try: self.alloc_lab_to.delete(0, tk.END)
            except Exception: pass
            try: self.refresh_lab_equipment_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate lab equipment: {e}")

    def release_lab_equipment(self):
        try:
            eq = self.alloc_lab_eq_id.get() if hasattr(self, 'alloc_lab_eq_id') else None
            if not eq:
                messagebox.showwarning("Input Error", "Select equipment to release.")
                return
            self.lab_eq_manager.release_lab_equipment(eq)
            messagebox.showinfo("Success", f"Released lab equipment {eq}.")
            try: self.alloc_lab_to.delete(0, tk.END)
            except Exception: pass
            try: self.refresh_lab_equipment_info()
            except Exception: pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release lab equipment: {e}")

    def refresh_lab_equipment_info(self):
        try:
            self.lab_equipment_display.delete(1.0, tk.END)
            items = []
            if hasattr(self.lab_eq_manager, 'track_lab_equipment'):
                items = self.lab_eq_manager.track_lab_equipment()
            elif hasattr(self.lab_eq_manager, 'lab_equipment'):
                for lid, eq in self.lab_eq_manager.lab_equipment.items():
                    if isinstance(eq, dict):
                        items.append({
                            'id': lid,
                            'name': eq.get('name'),
                            'category': eq.get('category'),
                            'allocated': eq.get('allocated', False),
                            'allocated_to': eq.get('allocated_to')
                        })
                    else:
                        items.append({
                            'id': lid,
                            'name': getattr(eq, 'name', str(eq)),
                            'category': getattr(eq, 'category', ''),
                            'allocated': getattr(eq, 'is_allocated', False),
                            'allocated_to': getattr(eq, 'allocated_to', None)
                        })
            if not items:
                self.lab_equipment_display.insert(tk.END, "No lab equipment found.")
                return
            for itm in items:
                allocated = itm.get('allocated')
                allocated_to = itm.get('allocated_to')
                line = f"ID: {itm.get('id')} | Name: {itm.get('name')} | Category: {itm.get('category')} | Allocated: {allocated}"
                if allocated and allocated_to:
                    line += f" | To: {allocated_to}"
                line += "\n"
                self.lab_equipment_display.insert(tk.END, line)
        except Exception as e:
            try: self.lab_equipment_display.insert(tk.END, f"Error: {e}")
            except Exception: pass
    # -----------------------------------------------------
    def create_lab_equipment_tab(self):
        """Create lab equipment management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Lab Equipment")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="Lab Equipment Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add Lab Equipment
        ttk.Label(input_frame, text="Equipment ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lab_eq_id = ttk.Entry(input_frame)
        self.lab_eq_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.lab_eq_name = ttk.Entry(input_frame)
        self.lab_eq_name.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.lab_eq_category = ttk.Entry(input_frame)
        self.lab_eq_category.grid(row=2, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add Lab Equipment", 
                  command=self.add_lab_equipment).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Allocate/Release
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select Equipment:").grid(row=5, column=0, sticky=tk.W, pady=2)
        alloc_lab_eq_values = getattr(self, 'get_lab_equipment_ids', lambda: [])()
        self.alloc_lab_eq_id = ttk.Combobox(input_frame, values=alloc_lab_eq_values)
        self.alloc_lab_eq_id.grid(row=5, column=1, pady=2)
        
        ttk.Label(input_frame, text="Allocate To:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.alloc_lab_to = ttk.Entry(input_frame)
        self.alloc_lab_to.grid(row=6, column=1, pady=2)
        
        ttk.Button(input_frame, text="Allocate Lab Equipment", 
                  command=self.allocate_lab_equipment).grid(row=7, column=0, pady=2)
        ttk.Button(input_frame, text="Release Lab Equipment", 
                  command=self.release_lab_equipment).grid(row=7, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="Lab Equipment Status", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lab_equipment_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.lab_equipment_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Lab Equipment Info", 
                  command=self.refresh_lab_equipment_info).pack(pady=5)
        
        self.refresh_lab_equipment_info()
    
    # -----------------------------------------------------
    # Student Tab Methods
    # -----------------------------------------------------
    def create_student_tab(self):
        """Create student management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Students")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="Student Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add Student Form
        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.student_id = ttk.Entry(input_frame)
        self.student_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="First Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.first_name = ttk.Entry(input_frame)
        self.first_name.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.last_name = ttk.Entry(input_frame)
        self.last_name.grid(row=2, column=1, pady=2)
        
        ttk.Label(input_frame, text="Department:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.department = ttk.Entry(input_frame)
        self.department.grid(row=3, column=1, pady=2)
        
        ttk.Label(input_frame, text="Enrollment Year:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.enrollment_year = ttk.Entry(input_frame)
        self.enrollment_year.grid(row=4, column=1, pady=2)

        # Optional Fields
        ttk.Label(input_frame, text="Email:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.email = ttk.Entry(input_frame)
        self.email.grid(row=5, column=1, pady=2)

        ttk.Label(input_frame, text="GPA:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.gpa = ttk.Entry(input_frame)
        self.gpa.grid(row=6, column=1, pady=2)

        ttk.Label(input_frame, text="Status:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.status = ttk.Combobox(input_frame, values=["enrolled", "graduated", "withdrawn"])
        self.status.grid(row=7, column=1, pady=2)
        self.status.set("enrolled") # Default value
        
        ttk.Button(input_frame, text="Add Student", 
                  command=self.add_student).grid(row=8, column=0, columnspan=2, pady=10)
        
        # Student Operations
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Select Student:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.operation_student_id = ttk.Combobox(input_frame, values=self.get_student_ids())
        self.operation_student_id.grid(row=10, column=1, pady=2)
        
        ttk.Button(input_frame, text="Get Student Info", 
                  command=self.get_student).grid(row=11, column=0, pady=2)
        ttk.Button(input_frame, text="Delete Student", 
                  command=self.delete_student).grid(row=11, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="Student Information", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.student_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.student_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="List All Students", 
                  command=self.list_students).pack(pady=5)
        
        self.list_students() # Initial display

    def get_student_ids(self):
        return [s['student_id'] for s in self.student_manager.list_students()]
    
    def update_student_comboboxes(self):
        """Updates comboboxes that list student IDs."""
        student_ids = self.get_student_ids()
        if hasattr(self, 'operation_student_id'):
            self.safe_set_values(self.operation_student_id, student_ids)
        if hasattr(self, 'portal_student'):
            self.safe_set_values(self.portal_student, student_ids)
        # Add any other comboboxes that need student IDs here
    
    def add_student(self):
        try:
            student_id = self.student_id.get()
            first_name = self.first_name.get()
            last_name = self.last_name.get()
            department = self.department.get()
            enrollment_year = self.enrollment_year.get()
            
            if not all([student_id, first_name, last_name, department, enrollment_year]):
                messagebox.showwarning("Input Error", "All fields (Student ID, Name, Department, Year) are required.")
                return
                
            student_data = {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "department": department,
                "enrollment_year": enrollment_year,
                # Optional fields (can be empty or pre-filled)
                "email": self.email.get() if hasattr(self, 'email') and self.email.get() else "N/A",
                "gpa": self.gpa.get() if hasattr(self, 'gpa') and self.gpa.get() else "N/A",
                "status": self.status.get() if hasattr(self, 'status') and self.status.get() else "enrolled"
            }

            # Use the Controller to register the student
            message = self.controller.register_new_student(student_data)
            messagebox.showinfo("Success", message)
            
            # Clear fields
            self.student_id.delete(0, tk.END)
            self.first_name.delete(0, tk.END)
            self.last_name.delete(0, tk.END)
            self.department.delete(0, tk.END)
            self.enrollment_year.delete(0, tk.END)
            if hasattr(self, 'email'): self.email.delete(0, tk.END)
            if hasattr(self, 'gpa'): self.gpa.delete(0, tk.END)
            if hasattr(self, 'status'): self.status.delete(0, tk.END)

            self.list_students() # Refresh display
            self.update_student_comboboxes() # Update comboboxes that use student IDs
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def get_student(self):
        try:
            student_id = self.operation_student_id.get()
            if not student_id:
                messagebox.showwarning("Input Error", "Please select or enter a Student ID.")
                return
            
            student = self.student_manager.get_student(student_id)
            if student:
                self.student_display.delete(1.0, tk.END)
                self.student_display.insert(tk.END, f"Student ID: {student.get('student_id', 'N/A')}\n")
                self.student_display.insert(tk.END, f"Name: {student.get('first_name', '')} {student.get('last_name', '')}\n")
                for key, value in student.items():
                    if key not in ["student_id", "first_name", "last_name"]:
                        self.student_display.insert(tk.END, f"{key.replace('_', ' ').title()}: {value}\n")
            else:
                messagebox.showerror("Not Found", f"Student with ID {student_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve student: {str(e)}")

    def delete_student(self):
        try:
            student_id = self.operation_student_id.get()
            if not student_id:
                messagebox.showwarning("Input Error", "Please select or enter a Student ID to delete.")
                return
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete student {student_id} and all their records?")
            if confirm:
                # Use the Controller to perform a full deletion
                message = self.controller.delete_student_fully(student_id)
                messagebox.showinfo("Success", message)
                self.operation_student_id.set('') # Clear combobox
                self.list_students() # Refresh display
                self.update_student_comboboxes() # Update comboboxes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def list_students(self):
        self.student_display.delete(1.0, tk.END)
        students = self.student_manager.list_students()
        if not students:
            self.student_display.insert(tk.END, "No students found.")
            return

        for student in students:
            self.student_display.insert(tk.END, f"ID: {student.get('student_id', 'N/A')}\n")
            self.student_display.insert(tk.END, f"Name: {student.get('first_name', '')} {student.get('last_name', '')}\n")
            self.student_display.insert(tk.END, f"Department: {student.get('department', 'N/A')}\n")
            self.student_display.insert(tk.END, f"Status: {student.get('status', 'N/A')}\n")
            self.student_display.insert(tk.END, "-"*30 + "\n")
        
        self.update_student_comboboxes() # Ensure comboboxes are updated after listing

    # -----------------------------------------------------
    # Staff Tab Methods (copied into final class)
    def create_staff_tab(self):
        """Create Staff management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Staff & Faculty")
        
        # Left panel - Professor Management
        input_frame = ttk.LabelFrame(frame, text="Add Professor", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Professor ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.staff_prof_id = ttk.Entry(input_frame)
        self.staff_prof_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.staff_prof_name = ttk.Entry(input_frame)
        self.staff_prof_name.grid(row=1, column=1, pady=2)

        ttk.Label(input_frame, text="Department:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.staff_prof_dept = ttk.Entry(input_frame)
        self.staff_prof_dept.grid(row=2, column=1, pady=2)

        ttk.Label(input_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.staff_prof_email = ttk.Entry(input_frame)
        self.staff_prof_email.grid(row=3, column=1, pady=2)
        
        ttk.Button(input_frame, text="Add Professor", command=self.add_professor_gui).grid(row=4, columnspan=2, pady=10)
        
        # Middle panel - Assign Course to Professor
        assign_frame = ttk.LabelFrame(frame, text="Assign Course to Professor", padding=10)
        assign_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(assign_frame, text="Professor ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.assign_prof_id_entry = ttk.Entry(assign_frame)
        self.assign_prof_id_entry.grid(row=0, column=1, pady=2)
        
        ttk.Label(assign_frame, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.assign_course_code_entry = ttk.Entry(assign_frame)
        self.assign_course_code_entry.grid(row=1, column=1, pady=2)
        
        ttk.Button(assign_frame, text="Assign Course", command=self.assign_course_to_prof_gui).grid(row=2, columnspan=2, pady=10)

        # Right panel - Display
        self.staff_display = scrolledtext.ScrolledText(frame, height=20, width=50, wrap=tk.WORD)
        self.staff_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Button(frame, text="Refresh Staff List", command=self.refresh_staff).pack(side=tk.BOTTOM, pady=5)

        self.refresh_staff() # Initial load

    def add_professor_gui(self):
        try:
            prof_id = self.staff_prof_id.get()
            name = self.staff_prof_name.get()
            dept = self.staff_prof_dept.get()
            email = self.staff_prof_email.get()
            
            if not all([prof_id, name, dept]):
                messagebox.showwarning("Input Error", "Professor ID, Name, and Department are required.")
                return

            message = self.staff_manager.add_professor(prof_id, name, dept, email)
            messagebox.showinfo("Success", message)
            self.staff_prof_id.delete(0, tk.END)
            self.staff_prof_name.delete(0, tk.END)
            self.staff_prof_dept.delete(0, tk.END)
            self.staff_prof_email.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add professor: {e}")

    def assign_course_to_prof_gui(self):
        try:
            prof_id = self.assign_prof_id_entry.get()
            course_code = self.assign_course_code_entry.get()
            if not prof_id or not course_code:
                messagebox.showwarning("Input Error", "Professor ID and Course Code are required.")
                return
            msg = self.controller.assign_professor_to_course(prof_id, course_code)
            messagebox.showinfo("Success", msg)
            # Clear fields
            self.assign_prof_id_entry.delete(0, tk.END)
            self.assign_course_code_entry.delete(0, tk.END)
            self.refresh_staff()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign course to professor: {e}")

    def refresh_staff(self):
        self.staff_display.delete(1.0, tk.END)
        professors = self.staff_manager.get_all_professors()
        if not professors:
            self.staff_display.insert(tk.END, "No professors found.")
            return

        for prof_data in professors:
            self.staff_display.insert(tk.END, f"ID: {prof_data.get('id', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Name: {prof_data.get('name', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Department: {prof_data.get('department', 'N/A')}\n")
            self.staff_display.insert(tk.END, f"Courses Taught: {', '.join(prof_data.get('courses_taught', [])) if prof_data.get('courses_taught') else 'None'}\n")
            self.staff_display.insert(tk.END, "-"*30 + "\n")

    # People Allocation Tab Methods
    # -----------------------------------------------------
    def create_people_tab(self):
        """Create people allocation management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="People Allocation")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="People Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Professor Operations
        ttk.Label(input_frame, text="Professor ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.professor_id = ttk.Entry(input_frame)
        self.professor_id.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Department:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.prof_dept = ttk.Entry(input_frame)
        self.prof_dept.grid(row=1, column=1, pady=2)
        
        ttk.Button(input_frame, text="Assign Professor Dept", 
                  command=getattr(self, 'assign_professor', lambda: messagebox.showwarning("Not Implemented", "Assign professor not implemented yet."))).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Student Allocation
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Student ID:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.alloc_student_id = ttk.Entry(input_frame)
        self.alloc_student_id.grid(row=4, column=1, pady=2)
        
        ttk.Label(input_frame, text="Department:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.student_dept = ttk.Entry(input_frame)
        self.student_dept.grid(row=5, column=1, pady=2)
        
        ttk.Button(input_frame, text="Assign Student Dept", 
                  command=getattr(self, 'assign_student', lambda: messagebox.showwarning("Not Implemented", "Assign student not implemented yet."))).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="People Allocation Status", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.people_display = scrolledtext.ScrolledText(display_frame, height=20, width=60, wrap=tk.WORD)
        self.people_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh People Info", 
                  command=getattr(self, 'refresh_people_info', lambda: messagebox.showwarning("Not Implemented", "Refresh people info not implemented yet."))).pack(pady=5)
        
        # Try to refresh people info if that method is available and resilient
        if getattr(self, 'refresh_people_info', None):
            try:
                self.refresh_people_info()
            except Exception:
                pass
    
    # -----------------------------------------------------
    # Curriculum Tab Methods
    # -----------------------------------------------------
    def create_curriculum_tab(self):
        """Create curriculum and course catalogue management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Curriculum")
        
        # Notebook within tab for organization
        curriculum_notebook = ttk.Notebook(frame)
        curriculum_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sub-tab 1: Course Catalogue
        catalogue_frame = ttk.Frame(curriculum_notebook)
        curriculum_notebook.add(catalogue_frame, text="Course Catalogue")
        
        # Left panel - Course Management
        input_frame = ttk.LabelFrame(catalogue_frame, text="Course Management", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Course form
        ttk.Label(input_frame, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.course_code = ttk.Entry(input_frame)
        self.course_code.grid(row=0, column=1, pady=2)
        
        ttk.Label(input_frame, text="Course Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.course_name = ttk.Entry(input_frame)
        self.course_name.grid(row=1, column=1, pady=2)
        
        ttk.Label(input_frame, text="Credits:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.course_credits = ttk.Entry(input_frame)
        self.course_credits.grid(row=2, column=1, pady=2)
        
        ttk.Label(input_frame, text="Department:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.course_dept = ttk.Combobox(input_frame, values=self.curriculum_manager.departments)
        self.course_dept.grid(row=3, column=1, pady=2)
        
        ttk.Label(input_frame, text="Description:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.course_desc = tk.Text(input_frame, height=3, width=30)
        self.course_desc.grid(row=4, column=1, pady=2)
        
        self.course_is_core = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Core Course", variable=self.course_is_core).grid(row=5, column=0, columnspan=2, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Course", command=self.add_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Course", command=self.update_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Course", command=self.delete_course).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Course List
        display_frame = ttk.LabelFrame(catalogue_frame, text="Course List", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for courses
        columns = ("Code", "Name", "Credits", "Department", "Core", "Enrolled")
        self.course_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.course_tree.heading(col, text=col)
            self.course_tree.column(col, width=100, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.course_tree.yview)
        self.course_tree.configure(yscroll=scrollbar.set)
        
        self.course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(display_frame, text="Refresh Courses", command=self.refresh_courses).pack(pady=5)
        
        # Bind selection to update form fields for easier editing
        self.course_tree.bind("<<TreeviewSelect>>", self.on_course_select)
        
        # Sub-tab 2: Student Planning
        planning_frame = ttk.Frame(curriculum_notebook)
        curriculum_notebook.add(planning_frame, text="Study Planning")
        
        # Student planning interface
        planning_input = ttk.LabelFrame(planning_frame, text="Study Plan Management", padding=10)
        planning_input.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(planning_input, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.plan_student_id = ttk.Combobox(planning_input, values=self.get_student_ids())
        self.plan_student_id.grid(row=0, column=1, pady=2)
        self.plan_student_id.bind("<<ComboboxSelected>>", lambda e: self.refresh_study_plan_display()) # Refresh on selection
        
        ttk.Label(planning_input, text="Semester:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.plan_semester = ttk.Combobox(planning_input, values=["Fall 2024", "Spring 2025", "Summer 2025"])
        self.plan_semester.grid(row=1, column=1, pady=2)
        self.plan_semester.bind("<<ComboboxSelected>>", lambda e: self.refresh_study_plan_display()) # Refresh on selection

        ttk.Label(planning_input, text="Select Course:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.plan_course = ttk.Combobox(planning_input, values=self.curriculum_manager.list_courses())
        self.plan_course.grid(row=2, column=1, pady=2)
        
        ttk.Button(planning_input, text="Add Course to Plan", command=self.add_to_plan).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(planning_input, text="Remove Course from Plan", command=self.remove_from_plan).grid(row=4, column=0, columnspan=2, pady=2)
        
        # Display study plan
        plan_display_frame = ttk.LabelFrame(planning_frame, text="Current Study Plan", padding=10)
        plan_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.plan_display_text = tk.Text(plan_display_frame, height=15, wrap=tk.WORD)
        self.plan_display_text.pack(fill=tk.BOTH, expand=True)
        
        # Set default student ID if available
        if self.get_student_ids():
            self.plan_student_id.set(self.get_student_ids()[0])
            self.refresh_study_plan_display()

    def add_course(self):
        try:
            course_code = self.course_code.get()
            course_name = self.course_name.get()
            credits_str = self.course_credits.get()
            department = self.course_dept.get()
            description = self.course_desc.get("1.0", tk.END).strip()
            is_core = self.course_is_core.get()
            
            if not all([course_code, course_name, credits_str, department]):
                messagebox.showwarning("Input Error", "Course Code, Name, Credits, and Department are required.")
                return
            
            credits = int(credits_str)
            
            course = Course(course_code, course_name, credits, department, description)
            course.is_core = is_core
            
            self.curriculum_manager.add_course(course)
            messagebox.showinfo("Success", f"Course '{course_name}' ({course_code}) added successfully!")
            
            # Clear fields
            self.course_code.delete(0, tk.END)
            self.course_name.delete(0, tk.END)
            self.course_credits.delete(0, tk.END)
            self.course_desc.delete("1.0", tk.END)
            self.course_is_core.set(False)
            self.course_dept.set('')
            
            self.refresh_courses()
            self.update_course_comboboxes()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")

    def update_course(self):
        try:
            course_code = self.course_code.get()
            if not course_code:
                messagebox.showwarning("Input Error", "Please select a course to update (enter its code).")
                return
            
            course = self.curriculum_manager.get_course(course_code)
            if not course:
                messagebox.showerror("Not Found", f"Course {course_code} not found.")
                return

            updates = {}
            # Check if fields have new values and are different
            if self.course_name.get() and self.course_name.get() != course.course_name:
                updates["course_name"] = self.course_name.get()
            if self.course_credits.get() and int(self.course_credits.get()) != course.credits:
                updates["credits"] = int(self.course_credits.get())
            if self.course_dept.get() and self.course_dept.get() != course.department:
                updates["department"] = self.course_dept.get()
            
            description_text = self.course_desc.get("1.0", tk.END).strip()
            if description_text and description_text != course.description:
                updates["description"] = description_text
            
            if self.course_is_core.get() != course.is_core:
                updates["is_core"] = self.course_is_core.get()

            if updates:
                self.curriculum_manager.update_course(course_code, updates)
                messagebox.showinfo("Success", f"Course {course_code} updated.")
                self.refresh_courses()
            else:
                messagebox.showinfo("Info", "No changes detected for course updates.")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update course: {str(e)}")

    def delete_course(self):
        try:
            course_code = self.course_code.get()
            if not course_code:
                messagebox.showwarning("Input Error", "Please enter the Course Code to delete.")
                return
            
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete course {course_code}?")
            if confirm:
                if self.curriculum_manager.delete_course(course_code):
                    messagebox.showinfo("Success", f"Course {course_code} deleted.")
                    # Clear fields and refresh
                    self.course_code.delete(0, tk.END)
                    self.course_name.delete(0, tk.END)
                    self.course_credits.delete(0, tk.END)
                    self.course_desc.delete("1.0", tk.END)
                    self.course_is_core.set(False)
                    self.course_dept.set('')
                    self.refresh_courses()
                    self.update_course_comboboxes()
                else:
                    messagebox.showerror("Error", f"Course {course_code} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete course: {str(e)}")

    def refresh_courses(self):
        # Clear treeview
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        courses = self.curriculum_manager.list_courses()
        for course in courses:
            self.course_tree.insert("", tk.END, values=(
                course.course_code,
                course.course_name,
                course.credits,
                course.department,
                "Yes" if course.is_core else "No",
                len(course.students_enrolled) # Count of enrolled students
            ))
        self.update_course_comboboxes() # Update comboboxes after refresh

    def update_course_comboboxes(self):
        """Updates comboboxes that list course codes."""
        course_codes = [c.course_code for c in self.curriculum_manager.list_courses()]
        if hasattr(self, 'plan_course'):
            self.plan_course['values'] = course_codes
        if hasattr(self, 'content_course'):
            self.content_course['values'] = course_codes
        if hasattr(self, 'assign_course_code_entry'):
            self.assign_course_code_entry['values'] = course_codes
        if hasattr(self, 'feedback_course'):
            self.feedback_course['values'] = course_codes
        if hasattr(self, 'assign_course'): # From LMS tab
            self.assign_course['values'] = course_codes
        if hasattr(self, 'quiz_course'): # From LMS tab
            self.quiz_course['values'] = course_codes

    # Study Planning Methods
    def add_to_plan(self):
        try:
            student_id = self.plan_student_id.get()
            semester = self.plan_semester.get()
            course_code = self.plan_course.get()

            if not all([student_id, semester, course_code]):
                messagebox.showwarning("Input Error", "Student ID, Semester, and Course are required.")
                return

            # Check if student and course exist (Controller could do this, but direct calls are simpler here)
            if not self.student_manager.student_exists(student_id):
                messagebox.showerror("Error", f"Student {student_id} not found.")
                return
            if not self.curriculum_manager.get_course(course_code):
                messagebox.showerror("Error", f"Course {course_code} not found.")
                return

            self.student_planner.add_course_to_plan(student_id, semester, course_code)
            messagebox.showinfo("Success", f"Course {course_code} added to plan for {student_id} in {semester}.")
            self.refresh_study_plan_display() # Refresh display immediately
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course to plan: {str(e)}")

    def refresh_study_plan_display(self):
        self.plan_display_text.delete("1.0", tk.END)
        student_id = self.plan_student_id.get()
        if not student_id:
            self.plan_display_text.insert(tk.END, "Enter Student ID to view plan.")
            return
        
        plan = self.student_planner.get_study_plan(student_id)
        if not plan:
            self.plan_display_text.insert(tk.END, f"No study plan found for {student_id}.")
            return
        
        for semester, courses in plan.items():
            self.plan_display_text.insert(tk.END, f"--- {semester} ---\n")
            if courses:
                for course in courses:
                    self.plan_display_text.insert(tk.END, f"- {course}\n")
            else:
                self.plan_display_text.insert(tk.END, "  No courses planned.\n")

    def on_course_select(self, event):
        """Populates the course form fields when a course is selected in the treeview."""
        selected_item = self.course_tree.selection()
        if not selected_item:
            return
        
        item_values = self.course_tree.item(selected_item, "values")
        if item_values:
            course_code, course_name, credits, department, is_core_str, enrolled = item_values
            
            self.course_code.delete(0, tk.END)
            self.course_code.insert(0, course_code)
            self.course_name.delete(0, tk.END)
            self.course_name.insert(0, course_name)
            self.course_credits.delete(0, tk.END)
            self.course_credits.insert(0, credits)
            self.course_dept.set(department)
            self.course_desc.delete("1.0", tk.END)
            # Fetch full description from manager
            course_obj = self.curriculum_manager.get_course(course_code)
            if course_obj and course_obj.description:
                self.course_desc.insert("1.0", course_obj.description)
            self.course_is_core.set(is_core_str == "Yes")

    def remove_from_plan(self):
        try:
            student_id = self.plan_student_id.get()
            semester = self.plan_semester.get()
            course_code = self.plan_course.get()

            if not all([student_id, semester, course_code]):
                messagebox.showwarning("Input Error", "Student ID, Semester, and Course are required.")
                return
            
            # Check if the course is actually in the plan before removing
            plan = self.student_planner.get_study_plan(student_id, semester)
            if not plan or semester not in plan or course_code not in plan[semester]:
                messagebox.showwarning("Info", f"Course {course_code} is not in the plan for {student_id} in {semester}.")
                return

            # To remove, we need to re-create the list without the course
            current_courses = self.student_planner.get_study_plan(student_id, semester)[semester]
            new_courses = [c for c in current_courses if c != course_code]
            self.student_planner.create_study_plan(student_id, semester, new_courses) # Overwrite with updated list

            messagebox.showinfo("Success", f"Course {course_code} removed from plan for {student_id} in {semester}.")
            self.plan_course.set('') # Clear course selection
            self.refresh_study_plan_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove course from plan: {str(e)}")

    # -----------------------------------------------------
    # LMS Tab Methods
    # -----------------------------------------------------
    def create_lms_tab(self):
        """Create Learning Management System tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="LMS")
        
        # Notebook for LMS organization
        lms_notebook = ttk.Notebook(frame)
        lms_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sub-tab 1: Content Management
        content_frame = ttk.Frame(lms_notebook)
        lms_notebook.add(content_frame, text="Content")
        
        # Content management interface
        content_input = ttk.LabelFrame(content_frame, text="Add Course Content", padding=10)
        content_input.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(content_input, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.content_course = ttk.Combobox(content_input)
        self.content_course.grid(row=0, column=1, pady=2)
        
        ttk.Label(content_input, text="Title:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.content_title = ttk.Entry(content_input)
        self.content_title.grid(row=1, column=1, pady=2)
        
        ttk.Label(content_input, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.content_type = ttk.Combobox(content_input, values=[t.value for t in ContentType])
        self.content_type.grid(row=2, column=1, pady=2)
        
        ttk.Label(content_input, text="URL/Path:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.content_url = ttk.Entry(content_input)
        self.content_url.grid(row=3, column=1, pady=2)
        
        ttk.Label(content_input, text="Description:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.content_desc = tk.Text(content_input, height=2, width=30)
        self.content_desc.grid(row=4, column=1, pady=2)
        
        ttk.Button(content_input, text="Add Content", command=self.add_lms_content).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Content display
        content_display_frame = ttk.LabelFrame(content_frame, text="Course Content List", padding=10)
        content_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.content_list_display = scrolledtext.ScrolledText(content_display_frame, height=15, wrap=tk.WORD)
        self.content_list_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(content_display_frame, text="Refresh Content", command=self.refresh_lms_content).pack(pady=5)
        
        # Sub-tab 2: Assignments & Quizzes
        assignments_frame = ttk.Frame(lms_notebook)
        lms_notebook.add(assignments_frame, text="Assignments & Quizzes")
        
        # Assignment creation interface
        assignment_input = ttk.LabelFrame(assignments_frame, text="Create Assignment", padding=10)
        assignment_input.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(assignment_input, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.assign_course = ttk.Combobox(assignment_input)
        self.assign_course.grid(row=0, column=1, pady=2)
        
        ttk.Label(assignment_input, text="Title:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.assign_title = ttk.Entry(assignment_input)
        self.assign_title.grid(row=1, column=1, pady=2)
        
        ttk.Label(assignment_input, text="Max Points:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.assign_points = ttk.Entry(assignment_input)
        self.assign_points.grid(row=2, column=1, pady=2)
        
        ttk.Label(assignment_input, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.assign_due = ttk.Entry(assignment_input)
        self.assign_due.grid(row=3, column=1, pady=2)
        self.assign_due.insert(0, "2024-12-15") # Default due date
        
        ttk.Button(assignment_input, text="Create Assignment", command=self.create_assignment).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Quiz creation interface
        quiz_input = ttk.LabelFrame(assignments_frame, text="Create Sample Quiz", padding=10)
        quiz_input.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(quiz_input, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.quiz_course = ttk.Combobox(quiz_input)
        self.quiz_course.grid(row=0, column=1, pady=2)
        
        ttk.Label(quiz_input, text="Quiz Title:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.quiz_title = ttk.Entry(quiz_input)
        self.quiz_title.grid(row=1, column=1, pady=2)
        
        ttk.Button(quiz_input, text="Create Sample Quiz", command=self.create_sample_quiz).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Display area for assignments and quizzes
        assignment_display_frame = ttk.LabelFrame(assignments_frame, text="Assignments & Quizzes Overview", padding=10)
        assignment_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.assignment_display = scrolledtext.ScrolledText(assignment_display_frame, height=10, wrap=tk.WORD)
        self.assignment_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(assignment_display_frame, text="Refresh Overview", command=self.refresh_assignment_display).pack(pady=5)
        
        self.refresh_lms_content() # Initial load for content tab
        self.refresh_assignment_display() # Initial load for assignments/quizzes tab
        
        # Update combobox values after potentially adding courses
        try:
            self.update_course_comboboxes()
        except Exception:
            pass

    def add_lms_content(self):
        try:
            course_code = self.content_course.get()
            title = self.content_title.get()
            content_type_str = self.content_type.get()
            url_or_path = self.content_url.get()
            description = self.content_desc.get("1.0", tk.END).strip()
            
            if not all([course_code, title, content_type_str, url_or_path]):
                messagebox.showwarning("Input Error", "Course Code, Title, Type, and URL/Path are required.")
                return

            content_type = ContentType(content_type_str)
            content_id = f"CONT_{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Simple unique ID
            
            new_content = LMSContent(content_id, course_code, title, content_type, url_or_path, description)
            self.lms_manager.add_content(new_content)
            messagebox.showinfo("Success", f"Content '{title}' added successfully for {course_code}.")
            
            # Clear fields
            self.content_course.set('')
            self.content_title.delete(0, tk.END)
            self.content_type.set('')
            self.content_url.delete(0, tk.END)
            self.content_desc.delete("1.0", tk.END)
            
            self.refresh_lms_content()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add LMS content: {str(e)}")

    def refresh_lms_content(self):
        self.content_list_display.delete("1.0", tk.END)
        course_code = self.content_course.get() # Use the combobox to filter
        
        if not course_code:
            self.content_list_display.insert(tk.END, "Select a course to view its content.")
            return

        contents = self.lms_manager.get_course_content(course_code)
        if not contents:
            self.content_list_display.insert(tk.END, f"No content found for {course_code}.")
            return
        
        for item in contents:
            self.content_list_display.insert(tk.END, f"Title: {item.title}\n")
            self.content_list_display.insert(tk.END, f"Type: {item.content_type.name}\n")
            self.content_list_display.insert(tk.END, f"URL/Path: {item.url}\n")
            self.content_list_display.insert(tk.END, f"Description: {item.description}\n")
            self.content_list_display.insert(tk.END, "-"*30 + "\n")

    def create_assignment(self):
        try:
            course_code = self.assign_course.get()
            if not course_code:
                messagebox.showwarning("Input Error", "Select a course to create an assignment for.")
                return
            title = self.assign_title.get()
            desc = self.assign_desc.get("1.0", tk.END).strip()
            due_date = self.assign_due.get()
            total_points = int(self.assign_points.get()) if self.assign_points.get() else 100
            
            assignment_id = f"ASSIGN_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            assignment = Assignment(assignment_id, course_code, title, desc, due_date, total_points)
            self.lms_manager.create_assignment(assignment)
            messagebox.showinfo("Success", f"Assignment '{title}' created for {course_code}.")
            self.refresh_assignment_display()
        except ValueError:
            messagebox.showerror("Input Error", "Please provide valid values for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create assignment: {e}")

    def create_sample_quiz(self):
        try:
            course_code = self.quiz_course.get()
            title = self.quiz_title.get()
            if not course_code or not title:
                messagebox.showwarning("Input Error", "Course and Quiz Title are required.")
                return
            quiz_id = f"QUIZ_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            quiz = Quiz(quiz_id, course_code, title, [{"question": "Sample?", "options": ["A","B","C"], "correct_answer": 0}])
            self.lms_manager.create_quiz(quiz)
            messagebox.showinfo("Success", f"Quiz '{title}' created for {course_code}.")
            self.refresh_assignment_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample quiz: {e}")

    def refresh_assignment_display(self):
        self.assignment_display.delete("1.0", tk.END)
        # Display assignments and quizzes from LMS
        # This is a simplified display; a real app would list per course or by type
        self.assignment_display.insert(tk.END, "--- Assignments ---\n")
        # Placeholder: In a real app, you'd fetch assignments per course.
        self.assignment_display.insert(tk.END, "Example: Python Basics Assignment (CS101) - Due 2024-12-15\n")
        self.assignment_display.insert(tk.END, "Example: Data Structures HW1 (CS201) - Due 2025-01-10\n\n")

        self.assignment_display.insert(tk.END, "--- Quizzes ---\n")
        # Placeholder: In a real app, you'd fetch quizzes per course.
        self.assignment_display.insert(tk.END, "Example: Python Fundamentals Quiz (CS101)\n")
        self.assignment_display.insert(tk.END, "Example: Circuits Quiz 1 (EE201)\n")

    # -----------------------------------------------------
    # Student Portal Tab
    # -----------------------------------------------------
    def create_student_portal_tab(self):
        """Create student portal tab for viewing grades and content"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Student Portal")
        
        # Student selection
        select_frame = ttk.LabelFrame(frame, text="Select Student", padding=10)
        select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(select_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        portal_student_values = getattr(self, 'get_student_ids', lambda: [])()
        self.portal_student = ttk.Combobox(select_frame, values=portal_student_values)
        self.portal_student.grid(row=0, column=1, pady=2)
        ttk.Button(select_frame, text="Load Student Data", command=getattr(self, 'load_student_portal', lambda: messagebox.showwarning("Not Implemented", "Student portal not implemented yet."))).grid(row=0, column=2, padx=5)
        
        # Notebook for student views
        portal_notebook = ttk.Notebook(frame)
        portal_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Grades view
        grades_frame = ttk.Frame(portal_notebook)
        portal_notebook.add(grades_frame, text="Grades")
        
        self.grades_display = scrolledtext.ScrolledText(grades_frame, height=20, wrap=tk.WORD)
        self.grades_display.pack(fill=tk.BOTH, expand=True)
        
        # Course content view
        content_frame = ttk.Frame(portal_notebook)
        portal_notebook.add(content_frame, text="Course Content")
        
        self.portal_content_display = scrolledtext.ScrolledText(content_frame, height=20, wrap=tk.WORD)
        self.portal_content_display.pack(fill=tk.BOTH, expand=True)
        
        # Feedback view
        feedback_frame = ttk.Frame(portal_notebook)
        portal_notebook.add(feedback_frame, text="Give Feedback")
        
        feedback_input = ttk.LabelFrame(feedback_frame, text="Submit Course Feedback", padding=10)
        feedback_input.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(feedback_input, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.feedback_course = ttk.Combobox(feedback_input, values=[]) # Populated on load
        self.feedback_course.grid(row=0, column=1, pady=2)
        
        ttk.Label(feedback_input, text="Rating (1-5):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.feedback_rating = ttk.Combobox(feedback_input, values=[1, 2, 3, 4, 5])
        self.feedback_rating.grid(row=1, column=1, pady=2)
        
        ttk.Label(feedback_input, text="Feedback:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.feedback_text = tk.Text(feedback_input, height=3, width=40)
        self.feedback_text.grid(row=2, column=1, pady=2)
        
        ttk.Button(feedback_input, text="Submit Feedback", command=getattr(self, 'submit_feedback', lambda: messagebox.showwarning("Not Implemented", "Submit feedback not implemented yet."))).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Display feedback
        feedback_display_frame = ttk.LabelFrame(feedback_frame, text="Course Ratings", padding=10)
        feedback_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.feedback_display = scrolledtext.ScrolledText(feedback_display_frame, height=10, wrap=tk.WORD)
        self.feedback_display.pack(fill=tk.BOTH, expand=True)
        
        # Update combobox values if available (be robust during initialization)
        if getattr(self, 'update_student_portal_comboboxes', None):
            try:
                self.update_student_portal_comboboxes()
            except Exception:
                pass
    
    # -----------------------------------------------------
    # Dashboard Tab
    # -----------------------------------------------------
    def create_dashboard_tab(self):
        """Create dashboard tab with system overview"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        
        # Dashboard content
        dashboard_frame = ttk.LabelFrame(frame, text="System Overview", padding=20)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dashboard_display = scrolledtext.ScrolledText(dashboard_frame, height=25, width=80, wrap=tk.WORD)
        self.dashboard_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dashboard_frame, text="Refresh Dashboard", 
                  command=self.refresh_dashboard).pack(pady=10)
        
        self.refresh_dashboard() # Initial load

    def refresh_dashboard(self):
        self.dashboard_display.delete(1.0, tk.END)
        
        self.dashboard_display.insert(tk.END, "--- System Overview ---\n\n")
        
        # Classroom Stats
        self.dashboard_display.insert(tk.END, f"Total Classrooms: {len(self.scheduler.classrooms)}\n")
        under_maintenance = sum(1 for room in self.scheduler.classrooms if room.is_under_maintenance)
        self.dashboard_display.insert(tk.END, f"Classrooms Under Maintenance: {under_maintenance}\n")
        self.dashboard_display.insert(tk.END, f"Current Reservations: {len(self.scheduler.reservations)}\n\n")
        
        # Student Stats
        students = self.student_manager.list_students()
        self.dashboard_display.insert(tk.END, f"Total Registered Students: {len(students)}\n")
        enrolled_students = sum(1 for s in students if s.get('status', 'enrolled') == 'enrolled')
        self.dashboard_display.insert(tk.END, f"Enrolled Students: {enrolled_students}\n\n")
        
        # Course Stats
        courses = self.curriculum_manager.list_courses()
        self.dashboard_display.insert(tk.END, f"Total Courses in Catalogue: {len(courses)}\n")
        core_courses = len([c for c in courses if c.is_core])
        self.dashboard_display.insert(tk.END, f"Core Courses: {core_courses}\n\n")
        
        # Equipment Stats
        total_equipment = len(self.eq_manager.equipment_list)
        allocated_equipment = sum(1 for eq in self.eq_manager.track_equipment() if eq['allocated'])
        self.dashboard_display.insert(tk.END, f"Total Equipment: {total_equipment}\n")
        self.dashboard_display.insert(tk.END, f"Allocated Equipment: {allocated_equipment}\n\n")
        
        # License Stats
        total_licenses = len(self.license_manager.licenses)
        total_seats_available = sum(lic['total_seats'] - lic['used_seats'] for lic in self.license_manager.track_licenses().values())
        self.dashboard_display.insert(tk.END, f"Total Software Licenses: {total_licenses}\n")
        self.dashboard_display.insert(tk.END, f"Total Available License Seats: {total_seats_available}\n\n")

        # Professor Stats
        professors = self.staff_manager.get_all_professors()
        self.dashboard_display.insert(tk.END, f"Total Professors: {len(professors)}\n")
        # Assign course count could be complex, simplified here
        courses_assigned = sum(len(p.get('courses_taught', [])) for p in professors)
        self.dashboard_display.insert(tk.END, f"Total Courses Assigned to Professors: {courses_assigned}\n\n")

        self.dashboard_display.insert(tk.END, "\n--- End of Overview ---\n")


# --- Main Application Execution ---
def main():
    root = tk.Tk()
    app = UniversityManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

