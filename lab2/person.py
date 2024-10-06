from re import match

class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)

    def validate_email(self, email):
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format")

    def validate_age(self, age):
        if age >= 0:
            return age
        else:
            raise ValueError("Age must be non-negative")

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        self.registered_courses.append(course)

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        self.assigned_courses.append(course)
