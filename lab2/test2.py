import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QLineEdit, QPushButton, QComboBox, 
                             QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from test import SchoolManagementSystem, Student, Instructor, Course

class SchoolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.sms = SchoolManagementSystem()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_display_tab()

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        save_action = file_menu.addAction('Save Data')
        save_action.triggered.connect(self.save_data)

        load_action = file_menu.addAction('Load Data')
        load_action.triggered.connect(self.load_data)

        export_action = file_menu.addAction('Export to CSV')
        export_action.triggered.connect(self.export_to_csv)

    def create_student_tab(self):
        student_widget = QWidget()
        student_layout = QVBoxLayout(student_widget)

        form_layout = QHBoxLayout()
        student_layout.addLayout(form_layout)

        left_form = QVBoxLayout()
        right_form = QVBoxLayout()
        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)

        self.student_name = self.create_input_field("Name:", left_form)
        self.student_age = self.create_input_field("Age:", left_form)
        self.student_email = self.create_input_field("Email:", right_form)
        self.student_id = self.create_input_field("Student ID:", right_form)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        student_layout.addWidget(add_button)

        self.course_dropdown = QComboBox()
        student_layout.addWidget(QLabel("Register for Course:"))
        student_layout.addWidget(self.course_dropdown)

        register_button = QPushButton("Register for Course")
        register_button.clicked.connect(self.register_student_for_course)
        student_layout.addWidget(register_button)

        self.tab_widget.addTab(student_widget, "Add Student")

    def create_instructor_tab(self):
        instructor_widget = QWidget()
        instructor_layout = QVBoxLayout(instructor_widget)

        form_layout = QHBoxLayout()
        instructor_layout.addLayout(form_layout)

        left_form = QVBoxLayout()
        right_form = QVBoxLayout()
        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)

        self.instructor_name = self.create_input_field("Name:", left_form)
        self.instructor_age = self.create_input_field("Age:", left_form)
        self.instructor_email = self.create_input_field("Email:", right_form)
        self.instructor_id = self.create_input_field("Instructor ID:", right_form)

        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)
        instructor_layout.addWidget(add_button)

        self.tab_widget.addTab(instructor_widget, "Add Instructor")

    def create_course_tab(self):
        course_widget = QWidget()
        course_layout = QVBoxLayout(course_widget)

        self.course_id = self.create_input_field("Course ID:", course_layout)
        self.course_name = self.create_input_field("Course Name:", course_layout)

        self.instructor_dropdown = QComboBox()
        course_layout.addWidget(QLabel("Instructor:"))
        course_layout.addWidget(self.instructor_dropdown)

        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        course_layout.addWidget(add_button)

        self.tab_widget.addTab(course_widget, "Add Course")

    def create_display_tab(self):
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])
        display_layout.addWidget(self.table)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_display)
        display_layout.addWidget(refresh_button)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_layout.addWidget(search_button)
        display_layout.addLayout(search_layout)

        self.tab_widget.addTab(display_widget, "Display Records")

    def create_input_field(self, label, layout):
        layout.addWidget(QLabel(label))
        input_field = QLineEdit()
        layout.addWidget(input_field)
        return input_field

    def add_student(self):
        try:
            student = Student(
                self.student_name.text(),
                int(self.student_age.text()),
                self.student_email.text(),
                self.student_id.text()
            )
            self.sms.add_student(student)
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.clear_student_fields()
            self.refresh_display()
            self.update_course_dropdowns()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_instructor(self):
        try:
            instructor = Instructor(
                self.instructor_name.text(),
                int(self.instructor_age.text()),
                self.instructor_email.text(),
                self.instructor_id.text()
            )
            self.sms.add_instructor(instructor)
            QMessageBox.information(self, "Success", "Instructor added successfully!")
            self.clear_instructor_fields()
            self.refresh_display()
            self.update_course_dropdowns()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_course(self):
        instructor = next((i for i in self.sms.instructors if i.name == self.instructor_dropdown.currentText()), None)
        course = Course(
            self.course_id.text(),
            self.course_name.text(),
            instructor
        )
        self.sms.add_course(course)
        if instructor:
            instructor.assign_course(course)
        QMessageBox.information(self, "Success", "Course added successfully!")
        self.clear_course_fields()
        self.refresh_display()
        self.update_course_dropdowns()

    def register_student_for_course(self):
        student = next((s for s in self.sms.students if s.student_id == self.student_id.text()), None)
        course = next((c for c in self.sms.courses if c.course_name == self.course_dropdown.currentText()), None)
        if student and course:
            student.register_course(course)
            QMessageBox.information(self, "Success", f"{student.name} registered for {course.course_name}")
        else:
            QMessageBox.critical(self, "Error", "Student or course not found")

    def clear_student_fields(self):
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()

    def clear_instructor_fields(self):
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()

    def clear_course_fields(self):
        self.course_id.clear()
        self.course_name.clear()
        self.instructor_dropdown.setCurrentIndex(0)

    def refresh_display(self):
        self.table.setRowCount(0)
        for student in self.sms.students:
            self.add_table_row(student.student_id, student.name, student.age, student.email)
        for instructor in self.sms.instructors:
            self.add_table_row(instructor.instructor_id, instructor.name, instructor.age, instructor.email)

    def add_table_row(self, *args):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for i, arg in enumerate(args):
            self.table.setItem(row, i, QTableWidgetItem(str(arg)))

    def update_course_dropdowns(self):
        self.course_dropdown.clear()
        self.course_dropdown.addItems([course.course_name for course in self.sms.courses])
        self.instructor_dropdown.clear()
        self.instructor_dropdown.addItems([instructor.name for instructor in self.sms.instructors])

    def search_records(self):
        search_term = self.search_input.text().lower()
        self.table.setRowCount(0)
        for student in self.sms.students:
            if search_term in student.name.lower() or search_term in student.student_id.lower():
                self.add_table_row(student.student_id, student.name, student.age, student.email)
        for instructor in self.sms.instructors:
            if search_term in instructor.name.lower() or search_term in instructor.instructor_id.lower():
                self.add_table_row(instructor.instructor_id, instructor.name, instructor.age, instructor.email)

    def save_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if filename:
            self.sms.save_data(filename)
            QMessageBox.information(self, "Success", f"Data saved to {filename}")

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json)")
        if filename:
            try:
                self.sms.load_data(filename)
                self.refresh_display()
                self.update_course_dropdowns()
                QMessageBox.information(self, "Success", f"Data loaded from {filename}")
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", f"File {filename} not found")

    def export_to_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Name', 'Age', 'Email', 'Type'])
                for student in self.sms.students:
                    writer.writerow([student.student_id, student.name, student.age, student.email, 'Student'])
                for instructor in self.sms.instructors:
                    writer.writerow([instructor.instructor_id, instructor.name, instructor.age, instructor.email, 'Instructor'])
            QMessageBox.information(self, "Success", f"Data exported to {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())



