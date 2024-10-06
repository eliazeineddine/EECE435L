
import tkinter as tk
from tkinter import ttk, messagebox
from school_system import SchoolSystem
from person import Student, Instructor
from course import Course

class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        
        # Set the window size
        self.root.geometry("600x400")
        
        # Initialize the school system (backend)
        self.school_system = SchoolSystem()
        self.school_system.load_data()  # Load existing data

        # Add a notebook widget (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        
        # Create three tabs for Student, Instructor, and Course
        self.student_tab = ttk.Frame(self.notebook)
        self.instructor_tab = ttk.Frame(self.notebook)
        self.course_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.student_tab, text='Students')
        self.notebook.add(self.instructor_tab, text='Instructors')
        self.notebook.add(self.course_tab, text='Courses')
        
        self.notebook.pack(expand=True, fill='both')

        # Initialize forms for each tab
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()

    def create_student_form(self):
        # Create a form for adding students
        ttk.Label(self.student_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.student_name_entry = ttk.Entry(self.student_tab)
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.student_tab, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        self.student_age_entry = ttk.Entry(self.student_tab)
        self.student_age_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.student_tab, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        self.student_email_entry = ttk.Entry(self.student_tab)
        self.student_email_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.student_tab, text="Student ID:").grid(row=3, column=0, padx=10, pady=10)
        self.student_id_entry = ttk.Entry(self.student_tab)
        self.student_id_entry.grid(row=3, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.student_tab, text="Add Student", command=self.add_student)
        add_button.grid(row=4, column=1, pady=10)

    def create_instructor_form(self):
        # Create a form for adding instructors
        ttk.Label(self.instructor_tab, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.instructor_name_entry = ttk.Entry(self.instructor_tab)
        self.instructor_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.instructor_tab, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        self.instructor_age_entry = ttk.Entry(self.instructor_tab)
        self.instructor_age_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.instructor_tab, text="Email:").grid(row=2, column=0, padx=10, pady=10)
        self.instructor_email_entry = ttk.Entry(self.instructor_tab)
        self.instructor_email_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.instructor_tab, text="Instructor ID:").grid(row=3, column=0, padx=10, pady=10)
        self.instructor_id_entry = ttk.Entry(self.instructor_tab)
        self.instructor_id_entry.grid(row=3, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.instructor_tab, text="Add Instructor", command=self.add_instructor)
        add_button.grid(row=4, column=1, pady=10)

    def create_course_form(self):
        # Create a form for adding courses
        ttk.Label(self.course_tab, text="Course Name:").grid(row=0, column=0, padx=10, pady=10)
        self.course_name_entry = ttk.Entry(self.course_tab)
        self.course_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.course_tab, text="Course ID:").grid(row=1, column=0, padx=10, pady=10)
        self.course_id_entry = ttk.Entry(self.course_tab)
        self.course_id_entry.grid(row=1, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.course_tab, text="Add Course", command=self.add_course)
        add_button.grid(row=2, column=1, pady=10)

    # Methods to handle adding students, instructors, and courses
    def add_student(self):
        name = self.student_name_entry.get()
        age = int(self.student_age_entry.get())
        email = self.student_email_entry.get()
        student_id = self.student_id_entry.get()

        if name and age and email and student_id:
            try:
                student = Student(name, age, email, student_id)
                self.school_system.students.append(student)
                self.school_system.save_data()  # Save to file after addition
                messagebox.showinfo("Success", f"Student {name} added!")
            except ValueError as e:
                messagebox.showwarning("Input Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def add_instructor(self):
        name = self.instructor_name_entry.get()
        age = int(self.instructor_age_entry.get())
        email = self.instructor_email_entry.get()
        instructor_id = self.instructor_id_entry.get()

        if name and age and email and instructor_id:
            try:
                instructor = Instructor(name, age, email, instructor_id)
                self.school_system.instructors.append(instructor)
                self.school_system.save_data()  # Save to file after addition
                messagebox.showinfo("Success", f"Instructor {name} added!")
            except ValueError as e:
                messagebox.showwarning("Input Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def add_course(self):
        course_name = self.course_name_entry.get()
        course_id = self.course_id_entry.get()

        if course_name and course_id:
            course = Course(course_id, course_name)
            self.school_system.courses.append(course)
            self.school_system.save_data()  # Save to file after addition
            messagebox.showinfo("Success", f"Course {course_name} added!")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()
