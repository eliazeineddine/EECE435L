import json
from person import Student, Instructor
from course import Course

class SchoolSystem:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []

    def save_data(self, filename='school_data.json'):
        data = {
            "students": [student.__dict__ for student in self.students],
            "instructors": [instructor.__dict__ for instructor in self.instructors],
            "courses": [course.__dict__ for course in self.courses],
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load_data(self, filename='school_data.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.students = [Student(**student) for student in data["students"]]
                self.instructors = [Instructor(**instructor) for instructor in data["instructors"]]
                self.courses = [Course(**course) for course in data["courses"]]
        except FileNotFoundError:
            print(f"No data file found named {filename}. Starting with an empty system.")
