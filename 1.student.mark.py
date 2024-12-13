# Data storage
students = []
courses = []
marks = {}

# Input functions
def input_number_of_students():
    num_students = int(input("Enter the number of students in the class: "))
    return num_students

def input_student_information():
    student_id = input("Enter student ID: ")
    student_name = input("Enter student name: ")
    student_dob = input("Enter student date of birth (DD/MM/YYYY): ")
    return {"id": student_id, "name": student_name, "dob": student_dob}

def input_number_of_courses():
    num_courses = int(input("Enter the number of courses: "))
    return num_courses

def input_course_information():
    course_id = input("Enter course ID: ")
    course_name = input("Enter course name: ")
    return {"id": course_id, "name": course_name}

def input_student_marks(course_id):
    if not students:
        print("No students available to assign marks.")
        return

    course_found = False
    for course in courses:
        if course["id"] == course_id:
            course_found = True
            break

    if not course_found:
        print("Course not found!")
        return

    if course_id not in marks:
        marks[course_id] = {}

    for student in students:
        mark = float(input(f"Enter marks for {student['name']} (ID: {student['id']}): "))
        marks[course_id][student["id"]] = mark

# Listing functions
def list_courses():
    if not courses:
        print("No courses available.")
        return
    print("Courses:")
    for course in courses:
        print(f"ID: {course['id']}, Name: {course['name']}")

def list_students():
    if not students:
        print("No students available.")
        return
    print("Students:")
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, DoB: {student['dob']}")

def show_student_marks(course_id):
    if course_id not in marks:
        print("No marks available for this course.")
        return

    print(f"Marks for course ID: {course_id}")
    for student_id, mark in marks[course_id].items():
        student_name = next((s["name"] for s in students if s["id"] == student_id), "Unknown")
        print(f"Student ID: {student_id}, Name: {student_name}, Mark: {mark}")

# Main execution loop
def main():
    while True:
        print("\nMenu:")
        print("1. Input number of students and their information")
        print("2. Input number of courses and their information")
        print("3. Select a course and input marks for students")
        print("4. List all courses")
        print("5. List all students")
        print("6. Show student marks for a course")
        print("0. Exit")

        choice = int(input("Choose an option: "))
        
        if choice == 1:
            num_students = input_number_of_students()
            for _ in range(num_students):
                students.append(input_student_information())
        elif choice == 2:
            num_courses = input_number_of_courses()
            for _ in range(num_courses):
                courses.append(input_course_information())
        elif choice == 3:
            course_id = input("Enter the course ID to input marks: ")
            input_student_marks(course_id)
        elif choice == 4:
            list_courses()
        elif choice == 5:
            list_students()
        elif choice == 6:
            course_id = input("Enter the course ID to show marks: ")
            show_student_marks(course_id)
        elif choice == 0:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
