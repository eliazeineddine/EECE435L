import json
import re

class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self._email = email  # Private attribute

    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if self.validate_email(value):
            self._email = value
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        }

    @classmethod
    def from_dict(cls, data, courses):
        student = cls(data['name'], data['age'], data['email'], data['student_id'])
        for course_id in data['registered_courses']:
            course = next((c for c in courses if c.course_id == course_id), None)
            if course:
                student.register_course(course)
        return student

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        }

    @classmethod
    def from_dict(cls, data, courses):
        instructor = cls(data['name'], data['age'], data['email'], data['instructor_id'])
        for course_id in data['assigned_courses']:
            course = next((c for c in courses if c.course_id == course_id), None)
            if course:
                instructor.assign_course(course)
        return instructor

class Course:
    def __init__(self, course_id, course_name, instructor=None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }

    @classmethod
    def from_dict(cls, data, instructors, students):
        course = cls(data['course_id'], data['course_name'])
        if data['instructor_id']:
            instructor = next((i for i in instructors if i.instructor_id == data['instructor_id']), None)
            if instructor:
                course.instructor = instructor
                instructor.assigned_courses.append(course)
        for student_id in data['enrolled_students']:
            student = next((s for s in students if s.student_id == student_id), None)
            if student:
                course.add_student(student)
                student.registered_courses.append(course)
        return course

class SchoolManagementSystem:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []

    def add_student(self, student):
        if isinstance(student, Student):
            self.students.append(student)
        else:
            raise TypeError("Object must be an instance of Student")

    def add_instructor(self, instructor):
        if isinstance(instructor, Instructor):
            self.instructors.append(instructor)
        else:
            raise TypeError("Object must be an instance of Instructor")

    def add_course(self, course):
        if isinstance(course, Course):
            self.courses.append(course)
        else:
            raise TypeError("Object must be an instance of Course")

    def save_data(self, filename):
        data = {
            'students': [student.to_dict() for student in self.students],
            'instructors': [instructor.to_dict() for instructor in self.instructors],
            'courses': [course.to_dict() for course in self.courses]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.instructors = [Instructor.from_dict(instructor_data, []) for instructor_data in data['instructors']]
        self.students = [Student.from_dict(student_data, []) for student_data in data['students']]
        self.courses = [Course.from_dict(course_data, self.instructors, self.students) for course_data in data['courses']]

    def validate_age(self, age):
        try:
            age = int(age)
            return age >= 0
        except ValueError:
            return False

# Example usage
if __name__ == "__main__":
    sms = SchoolManagementSystem()

    # Create and add a student
    student1 = Student("Alice", 20, "alice@example.com", "S001")
    sms.add_student(student1)

    # Create and add an instructor
    instructor1 = Instructor("Dr. Smith", 45, "smith@example.com", "I001")
    sms.add_instructor(instructor1)

    # Create and add a course
    course1 = Course("C001", "Introduction to Python", instructor1)
    sms.add_course(course1)

    # Register student for the course
    student1.register_course(course1)

    # Save data to a file
    sms.save_data("school_data.json")

    # Load data from the file
    new_sms = SchoolManagementSystem()
    new_sms.load_data("school_data.json")

    # Verify loaded data
    print(f"Loaded Students: {len(new_sms.students)}")
    print(f"Loaded Instructors: {len(new_sms.instructors)}")
    print(f"Loaded Courses: {len(new_sms.courses)}")