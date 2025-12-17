class StaffMember:
    def  __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        # Initialize an empty performance dictionary for tasks and their statuses
        self.performance = {}  
    
    def assign_task(self, task):
        if task not in self.performance:
            self.performance[task] = [] 
    
    def complete_task(self, task):
        if task in self.performance:
            self.performance[task].append(True)   # True signifies that the task was completed
        else:
            print("This staff member does not have this task assigned.")
    
    def fail_to_complete_task(self, task):
        if task in self.performance:
            self.performance[task].append(False)  # False signifies that the task was not completed
        else:
            print("This staff member does not have this task assigned.")
    
    def view_performance(self):
        if len(self.performance) == 0:
            return "No tasks assigned yet."
        
        performance_str = ""
        for task, statuses in self.performance.items():
            success_rate = sum(statuses)/len(statuses)*100    # Calculate the completion rate of a particular task
            performance_str += f"Task: {task} | Completion Rate: {success_rate}%\n" 
        
        return performance_str
    
    def issue_reward(self, reward):
        """Issues the specified reward to the staff member."""
        print(f"{self.name} has been issued {reward}.")
    
    def view_payroll(self):
        """This method should return a dictionary containing pay details. 
        This is just an example and will need to be replaced with actual implementation"""
        raise NotImplementedError("Method not implemented")
        
    def request_leave(self, start_date: str, end_date: str):
        """This method should handle the creation of a leave request. 
        This is just an example and will need to be replaced with actual implementation"""
        raise NotImplementedError("Method not implemented")
        
    def view_leave(self):
        """This method should return a dictionary containing details about current leave requests. 
        This is just an example and will need to be replaced with actual implementation"""
        raise NotImplementedError("Method not implemented")
    
    def view_benefits(self):
        """This method should return a dictionary containing benefits of the staff member. 
        This is just an example and will need to be replaced with actual implementation"""
        raise NotImplementedError("Method not implemented")
    
    
class HumanResources:
    def __init__(self):
        self.professors = {}
        self.teachingAssistants = {}
        
    def add_professor(self, prof: Professor):
        self.professors[prof.name] = prof
    
    def add_ta(self, ta: TeachingAssistant):
        self.teachingAssistants[ta.name] = ta
        
    def view_staff_info(self, name: str):
        if name in self.professors:
            prof = self.professors[name]
            print(f"{prof.name}'s Office Hours: {prof.office_hours}\nEmail: {prof.email} | Phone: {prof.phone}\nCourses: {prof.courses}")
        elif name in self.teachingAssistants:
            ta = self.teachingAssistants[name]
            print(f"{ta.name}'s Contact Information:\nEmail: {ta.email} | Phone: {ta.phone}\nCourse: {ta.course}")
        else:
            print("Staff member not found.")
            
class DepartmentHead:
    def __init__(self):
        self.research = {}
        
    def publish_research(self, name: str, research: dict):
        # Assume research is a dictionary with key-value pairs of topic and paper link.
        self.research[name] = research 
            
class UniversityHead:
    def __init__(self):
        self.activities = {}
        
    def manage_activity(self, name: str, activity: dict):
        # Assume activity is a dictionary with key-value pairs of event and date.
        self.activities[name] = activity 

class Professor(StaffMember):  # Inherits from StaffMember
    def __init__(self, name, email, phone, office_hours, courses):
        super().__init__(name, email, phone)
        self.office_hours = office_hours    
        self.courses = courses  
        
class TeachingAssistant(StaffMember):  # Inherits from StaffMember
    def __init__(self, name, email, phone, course):
        super().__init__(name, email, phone)
        self.course = course
