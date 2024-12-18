import math

class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.marks = {}
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        # Round down the mark to 1 decimal place
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

class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"Course ID: {self.course_id}, Course Name: {self.name}, Credits: {self.credits}"

from domains.student import Student
from domains.course import Course

class ManagementSystem:
    def __init__(self):
        self.students = []
        self.courses = []

    def input_number_of_students(self, num_students):
        for _ in range(num_students):
            student = self.input_student_info()
            self.students.append(student)

    def input_student_info(self):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        dob = input("Enter student DoB (YYYY-MM-DD): ")
        return Student(student_id, name, dob)

    def input_number_of_courses(self, num_courses):
        for _ in range(num_courses):
            course = self.input_course_info()
            self.courses.append(course)

    def input_course_info(self):
        course_id = input("Enter course ID: ")
        name = input("Enter course name: ")
        credits = int(input("Enter course credits: "))
        return Course(course_id, name, credits)

    def input_marks_for_course(self):
        course_id = input("Enter the course ID to input marks: ")
        course = next((course for course in self.courses if course.course_id == course_id), None)
        if course:
            for student in self.students:
                mark = float(input(f"Enter mark for student {student.name} (ID: {student.student_id}): "))
                student.add_mark(course.course_id, mark)
        else:
            print("Course not found.")

    def calculate_gpas(self):
        for student in self.students:
            student.calculate_gpa(self.courses)

    def sort_students_by_gpa(self):
        self.students.sort(key=lambda s: s.gpa, reverse=True)

    def list_courses(self):
        for course in self.courses:
            print(course)

    def list_students(self):
        for student in self.students:
            print(student)

    def show_student_marks(self):
        course_id = input("Enter the course ID to show marks: ")
        course = next((course for course in self.courses if course.course_id == course_id), None)
        if course:
            print(f"Marks for course {course.name} (ID: {course.course_id}):")
            for student in self.students:
                if course.course_id in student.marks:
                    print(f"Student Name: {student.name}, Student ID: {student.student_id}, Mark: {student.marks[course.course_id]}")
        else:
            print("Course not found.")

from domains.management import ManagementSystem

def input_data(system):
    num_students = int(input("Enter the number of students in the class: "))
    system.input_number_of_students(num_students)

    num_courses = int(input("Enter the number of courses: "))
    system.input_number_of_courses(num_courses)

    system.input_marks_for_course()
    system.calculate_gpas()

import curses

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
            stdscr.addstr(5, 0, "4. Exit")
            stdscr.refresh()

        elif option == '2':
            system.sort_students_by_gpa()
            stdscr.clear()
            stdscr.addstr(0, 0, "Students:")
            for i, student in enumerate(system.students):
                stdscr.addstr(i + 1, 0, str(student))
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(0, 0, "Welcome to the Student Mark Management System")
            stdscr.addstr(2, 0, "1. List Courses")
            stdscr.addstr(3, 0, "2. List Students")
            stdscr.addstr(4, 0, "3. Show Student Marks")
            stdscr.addstr(5, 0, "4. Exit")
            stdscr.refresh()

        elif option == '3':
            stdscr.addstr(8, 0, "Enter the course ID: ")
            course_id = stdscr.getstr(8, 19).decode()
            course = next((course for course in system.courses if course.course_id == course_id), None)
            if course:
                stdscr.clear()
                stdscr.addstr(0, 0, f"Marks for course {course.name} (ID: {course.course_id}):")
                for i, student in enumerate(system.students):
                    if course.course_id in student.marks:
                        stdscr.addstr(i + 1, 0, f"Student Name: {student.name}, Student ID: {student.student_id}, Mark: {student.marks[course.course_id]}")
                stdscr.refresh()
                stdscr.getch()
            else:
                stdscr.addstr(9, 0, "Course not found.")
                stdscr.refresh()
                stdscr.getch()
            stdscr.clear()
            stdscr.refresh()
            stdscr.addstr(0, 0, "Welcome to the Student Mark Management System")
            stdscr.addstr(2, 0, "1. List Courses")
            stdscr.addstr(3, 0, "2. List Students")
            stdscr.addstr(4, 0, "3. Show Student Marks")
            stdscr.addstr(5,