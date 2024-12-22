# domains/student.py
class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.marks = {}
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        # Round down the mark to 1 decimal place
        import math
        rounded_mark = math.floor(mark * 10) / 10
        self.marks[course_id] = rounded_mark

    def calculate_gpa(self, courses):
        total_credits = 0
        total_weighted_marks = 0
        for course_id, mark in self.marks.items():
            course = next((course for course in courses if course.course_id == course_id), None)
            if course:
                total_credits += course.credits
                total_weighted_marks += mark * course.credits
        if total_credits > 0:
            self.gpa = total_weighted_marks / total_credits

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}, DoB: {self.dob}, GPA: {self.gpa:.2f}"

# domains/course.py
class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"Course ID: {self.course_id}, Course Name: {self.name}, Credits: {self.credits}"

# domains/management.py
from .student import Student
from .course import Course
import input
import output
import json
import os
import zipfile

class ManagementSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def input_number_of_students(self):
        num_students = input.input_number_of_students()
        for _ in range(num_students):
            student = input.input_student_info()
            self.students.append(student)
        self.write_students_to_file()

    def input_student_info(self):
        return input.input_student_info()

    def input_number_of_courses(self):
        num_courses = input.input_number_of_courses()
        for _ in range(num_courses):
            course = input.input_course_info()
            self.courses.append(course)
        self.write_courses_to_file()

    def input_course_info(self):
        return input.input_course_info()

    def input_marks_for_course(self):
        course_id = input.input_course_id()
        course = next((course for course in self.courses if course.course_id == course_id), None)
        if course:
            for student in self.students:
                mark = input.input_student_mark(student)
                student.add_mark(course.course_id, mark)
            self.write_marks_to_file()
        else:
            print("Course not found.")

    def calculate_gpas(self):
        for student in self.students:
            student.calculate_gpa(self.courses)

    def sort_students_by_gpa(self):
        self.students.sort(key=lambda s: s.gpa, reverse=True)

    def list_courses(self):
        output.list_courses(self.courses)

    def list_students(self):
        output.list_students(self.students)

    def show_student_marks(self):
        course_id = input.input_course_id()
        course = next((course for course in self.courses if course.course_id == course_id), None)
        if course:
            output.show_student_marks(course, self.students)
        else:
            print("Course not found.")

    def write_students_to_file(self):
        with open('students.txt', 'w') as f:
            for student in self.students:
                f.write(f"{student.student_id},{student.name},{student.dob}\n")

    def write_courses_to_file(self):
        with open('courses.txt', 'w') as f:
            for course in self.courses:
                f.write(f"{course.course_id},{course.name},{course.credits}\n")

    def write_marks_to_file(self):
        with open('marks.txt', 'w') as f:
            for student in self.students:
                for course_id, mark in student.marks.items():
                    f.write(f"{student.student_id},{course_id},{mark}\n")

    def compress_files(self):
        with zipfile.ZipFile('students.dat', 'w') as zipf:
            zipf.write('students.txt')
            zipf.write('courses.txt')
            zipf.write('marks.txt')

    def decompress_files(self):
        with zipfile.ZipFile('students.dat', 'r') as zipf:
            zipf.extractall()

    def load_data(self):
        if os.path.exists('students.dat'):
            self.decompress_files()
            self.load_students()
            self.load_courses()
            self.load_marks()

    def load_students(self):
        with open('students.txt', 'r') as f:
            for line in f:
                student_id, name, dob = line.strip().split(',')
                student = Student(student_id, name, dob)
                self.students.append(student)

    def load_courses(self):
        with open('courses.txt', 'r') as f:
            for line in f:
                course_id, name, credits = line.strip().split(',')
                course = Course(course_id, name, int(credits))
                self.courses.append(course)

    def load_marks(self):
        with open('marks.txt', 'r') as f:
            for line in f:
                student_id, course_id, mark = line.strip().split(',')
                student = next((s for s in self.students if s.student_id == student_id), None)
                if student:
                    student.add_mark(course_id, float(mark))

    def display_ui(self):
        output.display_ui(self)

    def exit(self):
        self.compress_files()
        print("Data saved and compressed.")

# input.py
def input_number_of_students():
    return int(input("Enter the number of students in the class: "))

def input_student_info():
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    dob = input("Enter student DoB (YYYY-MM-DD): ")
    return Student(student_id, name, dob)

def input_number_of_courses():
    return int(input("Enter the number of courses: "))

def input_course_info():
    course_id = input("Enter course ID: ")
    name = input("Enter course name: ")
    credits = int(input("Enter course credits: "))
    return Course(course_id, name, credits)

def input_course_id():
    return input("Enter the course ID: ")

def input_student_mark(student):
    return float(input(f"Enter mark for student {student.name} (ID: {student.student_id}): "))

# output.py
import curses

def list_courses(courses):
    for course in courses:
        print(course)

def list_students(students):
    for student in students:
        print(student)

def show_student_marks(course, students):
    print(f"Marks for course {course.name} (ID: {course.course_id}):")
    for student in students:
        if course.course_id in student.marks:
            print(f"Student Name: {student.name}, Student ID: {student.student_id}, Mark: {student.marks[course.course_id]}")

def display_ui(system):
    curses.wrapper(_curses_ui, system)

def _curses_ui(stdscr, system):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Student Mark Management System")
    stdscr.addstr(2, 0, "1. List Courses")
    stdscr.addstr(3, 0, "2. List Students")
    stdscr.addstr(4, 0, "3. Show Student Marks")
    stdscr.addstr(5, 0, "4. Exit")
    stdscr.refresh()

    while True:
        stdscr.addstr(7, 0, "Select an option: ")
        option = stdscr.getstr(7, 18).decode()

        if option == '1':
            stdscr.clear()
            stdscr.addstr(0, 0, "Courses:")
            for i, course in enumerate(system.courses):
                stdscr.addstr(i + 1, 0, str(course))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(0, 0, "Welcome to the Student Mark Management System")
            stdscr.addstr(2, 0, "1. List Courses")
            stdscr.addstr(3, 0, "2. List Students")
            stdscr.addstr(4, 0, "3. Show Student Marks")
            stdscr.addstr(5,