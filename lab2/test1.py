import tkinter as tk
from tkinter import ttk, messagebox
from school_management_system import SchoolManagementSystem, Student, Instructor, Course

class SchoolManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("800x600")
        
        self.sms = SchoolManagementSystem()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_display_tab()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_student_tab(self):
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Add Student")
        
        ttk.Label(student_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.student_name = ttk.Entry(student_frame)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(student_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.student_age = ttk.Entry(student_frame)
        self.student_age.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(student_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.student_email = ttk.Entry(student_frame)
        self.student_email.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(student_frame, text="Student ID:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.student_id = ttk.Entry(student_frame)
        self.student_id.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(student_frame, text="Add Student", command=self.add_student).grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Label(student_frame, text="Register for Course:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.student_course_var = tk.StringVar()
        self.student_course_dropdown = ttk.Combobox(student_frame, textvariable=self.student_course_var)
        self.student_course_dropdown.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Button(student_frame, text="Register", command=self.register_student_for_course).grid(row=6, column=0, columnspan=2, pady=10)

    def create_instructor_tab(self):
        instructor_frame = ttk.Frame(self.notebook)
        self.notebook.add(instructor_frame, text="Add Instructor")
        
        ttk.Label(instructor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.instructor_name = ttk.Entry(instructor_frame)
        self.instructor_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(instructor_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.instructor_age = ttk.Entry(instructor_frame)
        self.instructor_age.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(instructor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.instructor_email = ttk.Entry(instructor_frame)
        self.instructor_email.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(instructor_frame, text="Instructor ID:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.instructor_id = ttk.Entry(instructor_frame)
        self.instructor_id.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(instructor_frame, text="Add Instructor", command=self.add_instructor).grid(row=4, column=0, columnspan=2, pady=10)

    def create_course_tab(self):
        course_frame = ttk.Frame(self.notebook)
        self.notebook.add(course_frame, text="Add Course")
        
        ttk.Label(course_frame, text="Course ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.course_id = ttk.Entry(course_frame)
        self.course_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(course_frame, text="Course Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.course_name = ttk.Entry(course_frame)
        self.course_name.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(course_frame, text="Instructor:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.course_instructor_var = tk.StringVar()
        self.course_instructor_dropdown = ttk.Combobox(course_frame, textvariable=self.course_instructor_var)
        self.course_instructor_dropdown.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(course_frame, text="Add Course", command=self.add_course).grid(row=3, column=0, columnspan=2, pady=10)

    def create_display_tab(self):
        display_frame = ttk.Frame(self.notebook)
        self.notebook.add(display_frame, text="Display Records")
        
        self.tree = ttk.Treeview(display_frame, columns=('ID', 'Name', 'Age', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Email', text='Email')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        refresh_button = ttk.Button(display_frame, text="Refresh", command=self.refresh_display)
        refresh_button.pack(pady=10)
        
        search_frame = ttk.Frame(display_frame)
        search_frame.pack(pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_records).pack(side='left')

    def add_student(self):
        try:
            student = Student(
                self.student_name.get(),
                int(self.student_age.get()),
                self.student_email.get(),
                self.student_id.get()
            )
            self.sms.add_student(student)
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_student_fields()
            self.refresh_display()
            self.update_course_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_instructor(self):
        try:
            instructor = Instructor(
                self.instructor_name.get(),
                int(self.instructor_age.get()),
                self.instructor_email.get(),
                self.instructor_id.get()
            )
            self.sms.add_instructor(instructor)
            messagebox.showinfo("Success", "Instructor added successfully!")
            self.clear_instructor_fields()
            self.refresh_display()
            self.update_course_dropdowns()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_course(self):
        instructor = next((i for i in self.sms.get_all_instructors() if i.name == self.course_instructor_var.get()), None)
        course = Course(
            self.course_id.get(),
            self.course_name.get(),
            instructor
        )
        self.sms.add_course(course)
        messagebox.showinfo("Success", "Course added successfully!")
        self.clear_course_fields()
        self.refresh_display()
        self.update_course_dropdowns()

    def register_student_for_course(self):
        student_id = self.student_id.get()
        course_name = self.student_course_var.get()
        course = next((c for c in self.sms.get_all_courses() if c.course_name == course_name), None)
        if course:
            self.sms.register_student_for_course(student_id, course.course_id)
            messagebox.showinfo("Success", f"Student registered for {course_name}")
        else:
            messagebox.showerror("Error", "Course not found")

    def clear_student_fields(self):
        self.student_name.delete(0, 'end')
        self.student_age.delete(0, 'end')
        self.student_email.delete(0, 'end')
        self.student_id.delete(0, 'end')

    def clear_instructor_fields(self):
        self.instructor_name.delete(0, 'end')
        self.instructor_age.delete(0, 'end')
        self.instructor_email.delete(0, 'end')
        self.instructor_id.delete(0, 'end')

    def clear_course_fields(self):
        self.course_id.delete(0, 'end')
        self.course_name.delete(0, 'end')
        self.course_instructor_var.set('')

    def refresh_display(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for student in self.sms.get_all_students():
            self.tree.insert('', 'end', values=(student.student_id, student.name, student.age, student.email))
        for instructor in self.sms.get_all_instructors():
            self.tree.insert('', 'end', values=(instructor.instructor_id, instructor.name, instructor.age, instructor.email))

    def search_records(self):
        query = self.search_entry.get().lower()
        results = []
        for student in self.sms.get_all_students():
            if query in student.name.lower() or query in student.student_id.lower():
                results.append((student.student_id, student.name, student.age, student.email))
        for instructor in self.sms.get_all_instructors():
            if query in instructor.name.lower() or query in instructor.instructor_id.lower():
                results.append((instructor.instructor_id, instructor.name, instructor.age, instructor.email))
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for result in results:
            self.tree.insert('', 'end', values=result)

    def update_course_dropdowns(self):
        course_names = [course.course_name for course in self.sms.get_all_courses()]
        self.student_course_dropdown['values'] = course_names
        self.course_instructor_dropdown['values'] = [instructor.name for instructor in self.sms.get_all_instructors()]

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = SchoolManagementApp()
    app.mainloop()
