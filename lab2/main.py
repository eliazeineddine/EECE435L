from school_system import SchoolSystem
from person import Student, Instructor
from course import Course

# Initialize the school system
school = SchoolSystem()

# Add a few students and instructors for testing
student1 = Student("John Doe", 20, "john@example.com", "S001")
instructor1 = Instructor("Jane Smith", 35, "jane@example.com", "I001")

# Add student and instructor to the system
school.students.append(student1)
school.instructors.append(instructor1)

# Save the system data
school.save_data()

# Load the data back to verify
school.load_data()
print(f"Loaded Students: {[student.name for student in school.students]}")
print(f"Loaded Instructors: {[instructor.name for instructor in school.instructors]}")
