

class Student:
    def __init__(self, student_id, name, dob):
        self.__id = student_id
        self.__name = name
        self.__dob = dob

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}, DoB: {self.__dob}"


class Course:
    def __init__(self, course_id, name):
        self.__id = course_id
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.__name}"


class MarkManager:
    def __init__(self):
        self.marks = {}

    def input_mark(self, course_id, students):
        if course_id not in self.marks:
            self.marks[course_id] = {}
        for student in students:
            mark = float(input(f"Enter marks for {student.get_name()} (ID: {student.get_id()}): "))
            self.marks[course_id][student.get_id()] = mark

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
            self.courses.append(Course(course_id, name))

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

    def main_menu(self):
        while True:
            print("\nMenu:")
            print("1. Input student information")
            print("2. Input course information")
            print("3. Input marks for a course")
            print("4. List students")
            print("5. List courses")
            print("6. Show marks for a course")
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
            elif choice == 0:
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    school_manager = SchoolManager()
    school_manager.main_menu()
