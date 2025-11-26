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

class UniversityManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University Management System")
        self.root.geometry("1200x800")
        
        # Initialize managers
        self.setup_managers()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_classroom_tab()
        self.create_equipment_tab()
        self.create_license_tab()
        self.create_lab_equipment_tab()
        self.create_student_tab()
        self.create_people_tab()
        self.create_dashboard_tab()
        
    def setup_managers(self):
        """Initialize all management systems"""
        self.scheduler = Scheduler()
        self.eq_manager = EquipmentManager()
        self.license_manager = LicenseManager()
        self.person_manager = PersonAllocationManager()
        self.lab_eq_manager = LaboratoryEquipmentManager()
        self.student_manager = StudentManager()
        
        # Add some sample data
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample data for demonstration"""
        # Sample classrooms
        self.scheduler.add_classroom(Classroom(id="R101", capacity=30, location="West Wing"))
        self.scheduler.add_classroom(Classroom(id="R102", capacity=50, location="East Wing"))
        self.scheduler.add_classroom(Classroom(id="R201", capacity=25, location="North Wing"))
        
        # Sample equipment
        self.eq_manager.add_equipment(Equipment("E001", "Projector", "AV"))
        self.eq_manager.add_equipment(Equipment("E002", "Whiteboard", "Stationery"))
        self.eq_manager.add_equipment(Equipment("E003", "Sound System", "AV"))
        
        # Sample lab equipment
        self.lab_eq_manager.add_lab_equipment(Equipment("L001", "Microscope", "Biology"))
        self.lab_eq_manager.add_lab_equipment(Equipment("L002", "Centrifuge", "Chemistry"))
        
        # Sample licenses
        self.license_manager.add_license(SoftwareLicense("S001", "DesignSuite", 10))
        self.license_manager.add_license(SoftwareLicense("S002", "ProgrammingIDE", 5))
        
        # Sample people
        self.person_manager.assign_professor("P001", "Computer Engineering")
        self.person_manager.assign_professor("P002", "Mechanical Engineering")
        self.person_manager.assign_student("S001", "Computer Engineering")
        
        # Sample student
        self.student_manager.add_student({
            "student_id": "007", 
            "first_name": "James", 
            "last_name": "Bond", 
            "department": "Spy School", 
            "enrollment_year": 2021
        })

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
        
        ttk.Label(input_frame, text="Maintenance:").grid(row=5, column=0, sticky=tk.W, pady=2)
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
        
        ttk.Label(input_frame, text="Reservation:").grid(row=9, column=0, sticky=tk.W, pady=2)
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
        
        self.classroom_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.classroom_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Classroom Info", 
                  command=self.refresh_classroom_info).pack(pady=5)
        
        self.refresh_classroom_info()
    
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
        
        ttk.Label(input_frame, text="Equipment ID:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.alloc_eq_id = ttk.Combobox(input_frame, values=self.get_equipment_ids())
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
        
        self.equipment_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.equipment_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Equipment Info", 
                  command=self.refresh_equipment_info).pack(pady=5)
        
        self.refresh_equipment_info()
    
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
        
        ttk.Label(input_frame, text="License ID:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.alloc_license_id = ttk.Combobox(input_frame, values=self.get_license_ids())
        self.alloc_license_id.grid(row=5, column=1, pady=2)
        
        ttk.Button(input_frame, text="Allocate Seat", 
                  command=self.allocate_license).grid(row=6, column=0, pady=2)
        ttk.Button(input_frame, text="Release Seat", 
                  command=self.release_license).grid(row=6, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="License Status", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.license_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.license_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh License Info", 
                  command=self.refresh_license_info).pack(pady=5)
        
        self.refresh_license_info()
    
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
        
        ttk.Label(input_frame, text="Equipment ID:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.alloc_lab_eq_id = ttk.Combobox(input_frame, values=self.get_lab_equipment_ids())
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
        
        self.lab_equipment_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.lab_equipment_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh Lab Equipment Info", 
                  command=self.refresh_lab_equipment_info).pack(pady=5)
        
        self.refresh_lab_equipment_info()
    
    def create_student_tab(self):
        """Create student management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Students")
        
        # Left panel - Inputs
        input_frame = ttk.LabelFrame(frame, text="Student Operations", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Add Student
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
        
        ttk.Button(input_frame, text="Add Student", 
                  command=self.add_student).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Student Operations
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Student ID:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.operation_student_id = ttk.Combobox(input_frame, values=self.get_student_ids())
        self.operation_student_id.grid(row=7, column=1, pady=2)
        
        ttk.Button(input_frame, text="Get Student", 
                  command=self.get_student).grid(row=8, column=0, pady=2)
        ttk.Button(input_frame, text="Delete Student", 
                  command=self.delete_student).grid(row=8, column=1, pady=2)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="Student Information", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.student_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.student_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="List All Students", 
                  command=self.list_students).pack(pady=5)
        
        self.list_students()
    
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
        
        ttk.Button(input_frame, text="Assign Professor", 
                  command=self.assign_professor).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Student Allocation
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(input_frame, text="Student ID:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.alloc_student_id = ttk.Entry(input_frame)
        self.alloc_student_id.grid(row=4, column=1, pady=2)
        
        ttk.Label(input_frame, text="Department:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.student_dept = ttk.Entry(input_frame)
        self.student_dept.grid(row=5, column=1, pady=2)
        
        ttk.Button(input_frame, text="Assign Student", 
                  command=self.assign_student).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Right panel - Display
        display_frame = ttk.LabelFrame(frame, text="People Allocation", padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.people_display = scrolledtext.ScrolledText(display_frame, height=20, width=60)
        self.people_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(display_frame, text="Refresh People Info", 
                  command=self.refresh_people_info).pack(pady=5)
        
        self.refresh_people_info()
    
    def create_dashboard_tab(self):
        """Create dashboard tab with system overview"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        
        # Dashboard content
        dashboard_frame = ttk.LabelFrame(frame, text="System Overview", padding=20)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dashboard_display = scrolledtext.ScrolledText(dashboard_frame, height=25, width=80)
        self.dashboard_display.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dashboard_frame, text="Refresh Dashboard", 
                  command=self.refresh_dashboard).pack(pady=10)
        
        self.refresh_dashboard()
    
    # Classroom Methods
    def get_classroom_ids(self):
        return [room.id for room in self.scheduler.classrooms]
    
    def add_classroom(self):
        try:
            room_id = self.classroom_id.get()
            capacity = int(self.capacity.get())
            location = self.location.get()
            
            self.scheduler.add_classroom(Classroom(id=room_id, capacity=capacity, location=location))
            messagebox.showinfo("Success", f"Classroom {room_id} added successfully!")
            self.refresh_classroom_info()
            # Update combobox values
            self.maintenance_room['values'] = self.get_classroom_ids()
            self.reserve_room['values'] = self.get_classroom_ids()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add classroom: {str(e)}")
    
    def report_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            description = self.maintenance_desc.get()
            
            result = self.scheduler.report_maintenance(room_id, description)
            messagebox.showinfo("Success", result)
            self.refresh_classroom_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to report maintenance: {str(e)}")
    
    def resolve_maintenance(self):
        try:
            room_id = self.maintenance_room.get()
            result = self.scheduler.resolve_maintenance(room_id)
            messagebox.showinfo("Success", result)
            self.refresh_classroom_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resolve maintenance: {str(e)}")
    
    def make_reservation(self):
        try:
            room_id = self.reserve_room.get()
            reserved_by = self.reserved_by.get()
            # Simple reservation - next available hour
            start = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            end = start + timedelta(hours=1)
            
            result = self.scheduler.reserve_classroom(room_id, start, end, reserved_by)
            messagebox.showinfo("Reservation", result)
            self.refresh_classroom_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make reservation: {str(e)}")
    
    def refresh_classroom_info(self):
        self.classroom_display.delete(1.0, tk.END)
        info = "=== CLASSROOMS ===\n\n"
        for room in self.scheduler.classrooms:
            info += f"ID: {room.id}\n"
            info += f"Capacity: {room.capacity}\n"
            info += f"Location: {room.location}\n"
            info += f"Maintenance: {'Yes' if room.is_under_maintenance else 'No'}\n"
            if room.maintenance_notes:
                info += f"Maintenance Notes: {', '.join(room.maintenance_notes)}\n"
            
            # Show reservations for this room
            room_reservations = [r for r in self.scheduler.reservations if r.classroom_id == room.id]
            if room_reservations:
                info += "Reservations:\n"
                for res in room_reservations:
                    info += f"  - {res.reserved_by}: {res.start.strftime('%Y-%m-%d %H:%M')} to {res.end.strftime('%H:%M')}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.classroom_display.insert(tk.END, info)
    
    # Equipment Methods
    def get_equipment_ids(self):
        return list(self.eq_manager.equipment_list.keys())
    
    def add_equipment(self):
        try:
            eq_id = self.eq_id.get()
            name = self.eq_name.get()
            category = self.eq_category.get()
            
            self.eq_manager.add_equipment(Equipment(eq_id, name, category))
            messagebox.showinfo("Success", f"Equipment {eq_id} added successfully!")
            self.refresh_equipment_info()
            self.alloc_eq_id['values'] = self.get_equipment_ids()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add equipment: {str(e)}")
    
    def allocate_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get()
            allocated_to = self.alloc_to.get()
            
            self.eq_manager.allocate_equipment(eq_id, allocated_to)
            messagebox.showinfo("Success", f"Equipment {eq_id} allocated to {allocated_to}!")
            self.refresh_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate equipment: {str(e)}")
    
    def release_equipment(self):
        try:
            eq_id = self.alloc_eq_id.get()
            self.eq_manager.release_equipment(eq_id)
            messagebox.showinfo("Success", f"Equipment {eq_id} released!")
            self.refresh_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release equipment: {str(e)}")
    
    def refresh_equipment_info(self):
        self.equipment_display.delete(1.0, tk.END)
        info = "=== EQUIPMENT ===\n\n"
        for eq in self.eq_manager.track_equipment():
            info += f"ID: {eq['id']}\n"
            info += f"Name: {eq['name']}\n"
            info += f"Category: {eq['category']}\n"
            info += f"Allocated: {'Yes' if eq['allocated'] else 'No'}\n"
            if eq['allocated']:
                info += f"Allocated To: {eq['allocated_to']}\n"
                info += f"Allocation Date: {eq['allocation_date']}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.equipment_display.insert(tk.END, info)
    
    # License Methods
    def get_license_ids(self):
        return list(self.license_manager.licenses.keys())
    
    def add_license(self):
        try:
            license_id = self.license_id.get()
            name = self.software_name.get()
            total_seats = int(self.total_seats.get())
            
            self.license_manager.add_license(SoftwareLicense(license_id, name, total_seats))
            messagebox.showinfo("Success", f"License {license_id} added successfully!")
            self.refresh_license_info()
            self.alloc_license_id['values'] = self.get_license_ids()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add license: {str(e)}")
    
    def allocate_license(self):
        try:
            license_id = self.alloc_license_id.get()
            self.license_manager.allocate(license_id)
            messagebox.showinfo("Success", f"License seat allocated for {license_id}!")
            self.refresh_license_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate license: {str(e)}")
    
    def release_license(self):
        try:
            license_id = self.alloc_license_id.get()
            self.license_manager.release(license_id)
            messagebox.showinfo("Success", f"License seat released for {license_id}!")
            self.refresh_license_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release license: {str(e)}")
    
    def refresh_license_info(self):
        self.license_display.delete(1.0, tk.END)
        info = "=== SOFTWARE LICENSES ===\n\n"
        for lid, details in self.license_manager.track_licenses().items():
            info += f"License ID: {lid}\n"
            info += f"Software: {details['name']}\n"
            info += f"Used Seats: {details['used_seats']}/{details['total_seats']}\n"
            info += f"Available: {details['total_seats'] - details['used_seats']}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.license_display.insert(tk.END, info)
    
    # Lab Equipment Methods
    def get_lab_equipment_ids(self):
        return list(self.lab_eq_manager.lab_equipment.keys())
    
    def add_lab_equipment(self):
        try:
            eq_id = self.lab_eq_id.get()
            name = self.lab_eq_name.get()
            category = self.lab_eq_category.get()
            
            self.lab_eq_manager.add_lab_equipment(Equipment(eq_id, name, category))
            messagebox.showinfo("Success", f"Lab Equipment {eq_id} added successfully!")
            self.refresh_lab_equipment_info()
            self.alloc_lab_eq_id['values'] = self.get_lab_equipment_ids()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add lab equipment: {str(e)}")
    
    def allocate_lab_equipment(self):
        try:
            eq_id = self.alloc_lab_eq_id.get()
            allocated_to = self.alloc_lab_to.get()
            
            self.lab_eq_manager.allocate_lab_equipment(eq_id, allocated_to)
            messagebox.showinfo("Success", f"Lab Equipment {eq_id} allocated to {allocated_to}!")
            self.refresh_lab_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to allocate lab equipment: {str(e)}")
    
    def release_lab_equipment(self):
        try:
            eq_id = self.alloc_lab_eq_id.get()
            self.lab_eq_manager.release_lab_equipment(eq_id)
            messagebox.showinfo("Success", f"Lab Equipment {eq_id} released!")
            self.refresh_lab_equipment_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to release lab equipment: {str(e)}")
    
    def refresh_lab_equipment_info(self):
        self.lab_equipment_display.delete(1.0, tk.END)
        info = "=== LAB EQUIPMENT ===\n\n"
        for eq in self.lab_eq_manager.track_lab_equipment():
            info += f"ID: {eq['id']}\n"
            info += f"Name: {eq['name']}\n"
            info += f"Category: {eq['category']}\n"
            info += f"Allocated: {'Yes' if eq['allocated'] else 'No'}\n"
            if eq['allocated']:
                info += f"Allocated To: {eq['allocated_to']}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.lab_equipment_display.insert(tk.END, info)
    
    # Student Methods
    def get_student_ids(self):
        students = self.student_manager.list_students()
        return [student['student_id'] for student in students if 'student_id' in student]
    
    def add_student(self):
        try:
            student_data = {
                "student_id": self.student_id.get(),
                "first_name": self.first_name.get(),
                "last_name": self.last_name.get(),
                "department": self.department.get(),
                "enrollment_year": self.enrollment_year.get()
            }
            
            self.student_manager.add_student(student_data)
            messagebox.showinfo("Success", f"Student {self.student_id.get()} added successfully!")
            self.operation_student_id['values'] = self.get_student_ids()
            self.list_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def get_student(self):
        try:
            student_id = self.operation_student_id.get()
            student = self.student_manager.get_student(student_id)
            
            self.student_display.delete(1.0, tk.END)
            if student:
                info = "=== STUDENT DETAILS ===\n\n"
                for key, value in student.items():
                    info += f"{key}: {value}\n"
                self.student_display.insert(tk.END, info)
            else:
                self.student_display.insert(tk.END, "Student not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get student: {str(e)}")
    
    def delete_student(self):
        try:
            student_id = self.operation_student_id.get()
            if self.student_manager.delete_student(student_id):
                messagebox.showinfo("Success", f"Student {student_id} deleted successfully!")
                self.operation_student_id['values'] = self.get_student_ids()
                self.list_students()
            else:
                messagebox.showerror("Error", "Student not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def list_students(self):
        self.student_display.delete(1.0, tk.END)
        students = self.student_manager.list_students()
        
        info = "=== ALL STUDENTS ===\n\n"
        for student in students:
            info += f"ID: {student.get('student_id', 'N/A')}\n"
            info += f"Name: {student.get('first_name', '')} {student.get('last_name', '')}\n"
            info += f"Department: {student.get('department', 'N/A')}\n"
            info += f"Enrollment Year: {student.get('enrollment_year', 'N/A')}\n"
            info += "\n" + "-"*40 + "\n\n"
        
        self.student_display.insert(tk.END, info)
    
    # People Allocation Methods
    def assign_professor(self):
        try:
            prof_id = self.professor_id.get()
            department = self.prof_dept.get()
            
            self.person_manager.assign_professor(prof_id, department)
            messagebox.showinfo("Success", f"Professor {prof_id} assigned to {department}!")
            self.refresh_people_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign professor: {str(e)}")
    
    def assign_student(self):
        try:
            student_id = self.alloc_student_id.get()
            department = self.student_dept.get()
            
            self.person_manager.assign_student(student_id, department)
            messagebox.showinfo("Success", f"Student {student_id} assigned to {department}!")
            self.refresh_people_info()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign student: {str(e)}")
    
    def refresh_people_info(self):
        self.people_display.delete(1.0, tk.END)
        people_data = self.person_manager.track_people()
        
        info = "=== PEOPLE ALLOCATION ===\n\n"
        info += "PROFESSORS:\n"
        for prof_id, dept in people_data['professors'].items():
            info += f"  {prof_id}: {dept}\n"
        
        info += "\nSTUDENTS:\n"
        for student_id, dept in people_data['students'].items():
            info += f"  {student_id}: {dept}\n"
        
        self.people_display.insert(tk.END, info)
    
    # Dashboard Methods
    def refresh_dashboard(self):
        self.dashboard_display.delete(1.0, tk.END)
        
        info = "=== UNIVERSITY MANAGEMENT SYSTEM DASHBOARD ===\n\n"
        
        # Classroom Summary
        info += "📚 CLASSROOMS:\n"
        info += f"  Total: {len(self.scheduler.classrooms)}\n"
        maintenance_count = sum(1 for room in self.scheduler.classrooms if room.is_under_maintenance)
        info += f"  Under Maintenance: {maintenance_count}\n"
        info += f"  Reservations: {len(self.scheduler.reservations)}\n\n"
        
        # Equipment Summary
        info += "🛠️ EQUIPMENT:\n"
        info += f"  General Equipment: {len(self.eq_manager.equipment_list)}\n"
        allocated_eq = sum(1 for eq in self.eq_manager.track_equipment() if eq['allocated'])
        info += f"  Allocated: {allocated_eq}\n\n"
        
        # Lab Equipment Summary
        info += "🔬 LAB EQUIPMENT:\n"
        info += f"  Total: {len(self.lab_eq_manager.lab_equipment)}\n"
        allocated_lab = sum(1 for eq in self.lab_eq_manager.track_lab_equipment() if eq['allocated'])
        info += f"  Allocated: {allocated_lab}\n\n"
        
        # License Summary
        info += "💻 SOFTWARE LICENSES:\n"
        info += f"  Total Licenses: {len(self.license_manager.licenses)}\n"
        total_seats = sum(lic.total_seats for lic in self.license_manager.licenses.values())
        used_seats = sum(lic.used_seats for lic in self.license_manager.licenses.values())
        info += f"  Total Seats: {total_seats}\n"
        info += f"  Used Seats: {used_seats}\n"
        info += f"  Available Seats: {total_seats - used_seats}\n\n"
        
        # People Summary
        info += "👥 PEOPLE:\n"
        people_data = self.person_manager.track_people()
        info += f"  Professors: {len(people_data['professors'])}\n"
        info += f"  Students: {len(people_data['students'])}\n\n"
        
        # Student Records Summary
        students = self.student_manager.list_students()
        info += "🎓 STUDENT RECORDS:\n"
        info += f"  Total Students: {len(students)}\n"
        
        self.dashboard_display.insert(tk.END, info)

def main():
    root = tk.Tk()
    app = UniversityManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()