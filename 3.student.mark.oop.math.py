import math
import numpy as np
import curses

class Student:
    def __init__(self, student_id, name, dob):
        self.__id = student_id
        self.__name = name
        self.__dob = dob
        self.__gpa = 0.0
        self.__credits = {}
    
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def set_gpa(self, gpa):
        self.__gpa = gpa

    def get_gpa(self):
        return self.__gpa

    def add_credits(self, course_id, credit):
        self.__credits[course_id] = credit

    def get_credits(self):
        return self.__credits

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, DoB: {self.__dob}, GPA: {self.__gpa:.1f}"


class Course:
    def __init__(self, course_id, name, credit):
        self.__id = course_id
        self.__name = name
        self.__credit = credit

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credit(self):
        return self.__credit

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, Credit: {self.__credit}"


class MarkManager:
    def __init__(self):
        self.marks = {}

    def input_mark(self, course_id, students):
        if course_id not in self.marks:
            self.marks[course_id] = {}
        for student in students:
            mark = float(input(f"Enter marks for {student.get_name()} (ID: {student.get_id()}): "))
            rounded_mark = math.floor(mark * 10) / 10  # Round down to 1 decimal place
            self.marks[course_id][student.get_id()] = rounded_mark

    def show_marks(self, course_id, students):
        if course_id not in self.marks or not self.marks[course_id]:
            print("No marks available for this course.")
            return

        print(f"Marks for course ID: {course_id}:")
        for student_id, mark in self.marks[course_id].items():
            student_name = next((s.get_name() for s in students if s.get_id() == student_id), "Unknown")
            print(f"Student ID: {student_id}, Name: {student_name}, Mark: {mark}")


class SchoolManager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.mark_manager = MarkManager()

    def input_students(self):
        num_students = int(input("Enter the number of students in the class: "))
        for _ in range(num_students):
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            dob = input("Enter student date of birth (DD/MM/YYYY): ")
            self.students.append(Student(student_id, name, dob))

    def input_courses(self):
        num_courses = int(input("Enter the number of courses: "))
        for _ in range(num_courses):
            course_id = input("Enter course ID: ")
            name = input("Enter course name: ")
            credit = int(input("Enter course credit: "))
            course = Course(course_id, name, credit)
            self.courses.append(course)
            for student in self.students:
                student.add_credits(course_id, credit)

    def list_students(self):
        if not self.students:
            print("No students available.")
        else:
            print("Students:")
            for student in self.students:
                print(student)

    def list_courses(self):
        if not self.courses:
            print("No courses available.")
        else:
            print("Courses:")
            for course in self.courses:
                print(course)

    def input_marks(self):
        course_id = input("Enter course ID to input marks: ")
        course_exists = any(course.get_id() == course_id for course in self.courses)
        if course_exists:
            self.mark_manager.input_mark(course_id, self.students)
        else:
            print("Course not found.")

    def show_marks(self):
        course_id = input("Enter course ID to show marks: ")
        self.mark_manager.show_marks(course_id, self.students)

    def calculate_gpa(self):
        for student in self.students:
            total_credits = 0
            weighted_sum = 0
            for course in self.courses:
                course_id = course.get_id()
                credit = course.get_credit()
                if course_id in self.mark_manager.marks and student.get_id() in self.mark_manager.marks[course_id]:
                    total_credits += credit
                    weighted_sum += self.mark_manager.marks[course_id][student.get_id()] * credit
            if total_credits > 0:
                student.set_gpa(weighted_sum / total_credits)

    def sort_students_by_gpa(self):
        self.calculate_gpa()
        self.students.sort(key=lambda s: s.get_gpa(), reverse=True)

    def display_sorted_students(self):
        self.sort_students_by_gpa()
        print("Students sorted by GPA (Descending):")
        for student in self.students:
            print(student)

    def curses_ui(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to the Student Management System!")
        stdscr.addstr(1, 0, "Press any key to start...")
        stdscr.refresh()
        stdscr.getch()

    def main_menu(self):
        while True:
            print("\nMenu:")
            print("1. Input student information")
            print("2. Input course information")
            print("3. Input marks for a course")
            print("4. List students")
            print("5. List courses")
            print("6. Show marks for a course")
            print("7. Calculate and display sorted GPA")
            print("0. Exit")

            choice = int(input("Choose an option: "))
            if choice == 1:
                self.input_students()
            elif choice == 2:
                self.input_courses()
            elif choice == 3:
                self.input_marks()
            elif choice == 4:
                self.list_students()
            elif choice == 5:
                self.list_courses()
            elif choice == 6:
                self.show_marks()
            elif choice == 7:
                self.display_sorted_students()
            elif choice == 0:
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    school_manager = SchoolManager()
    curses.wrapper(school_manager.curses_ui)
    school_manager.main_menu()
