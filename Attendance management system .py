from datetime import datetime
from typing import List, Dict


class Student:
    def __init__(self, student_id: int, name: str, roll_no: str, course: str):
        self.student_id = student_id
        self.name = name
        self.roll_no = roll_no
        self.course = course
        self.attendance_records: Dict[str, List[str]] = {}  # course: [dates]

    def __str__(self):
        return f"ID: {self.student_id}, {self.name} ({self.roll_no}) - {self.course}"


class Faculty:
    def __init__(self, faculty_id: int, name: str, department: str):
        self.faculty_id = faculty_id
        self.name = name
        self.department = department


class Course:
    def __init__(self, course_id: int, name: str, faculty_id: int):
        self.course_id = course_id
        self.name = name
        self.faculty_id = faculty_id
        self.students: List[int] = []  # student_ids


class Attendance:
    def __init__(self, att_id: int, course_id: int, date: str,
                 present_students: List[int]):
        self.att_id = att_id
        self.course_id = course_id
        self.date = date
        self.present_students = present_students


class AttendanceManagementSystem:
    def __init__(self):
        self.students: List[Student] = []
        self.faculty: List[Faculty] = []
        self.courses: List[Course] = []
        self.attendance: List[Attendance] = []
        self.next_student_id = 1
        self.next_faculty_id = 1
        self.next_course_id = 1
        self.next_att_id = 1

    # ADMIN OPERATIONS
    def add_student(self, name: str, roll_no: str, course: str):
        student = Student(self.next_student_id, name, roll_no, course)
        self.students.append(student)
        self.next_student_id += 1
        print(f"✅ Student '{name}' added!")

    def add_faculty(self, name: str, department: str):
        faculty = Faculty(self.next_faculty_id, name, department)
        self.faculty.append(faculty)
        self.next_faculty_id += 1
        print(f"✅ Faculty '{name}' added!")

    def add_course(self, name: str, faculty_id: int):
        course = Course(self.next_course_id, name, faculty_id)
        self.courses.append(course)
        self.next_course_id += 1
        print(f"✅ Course '{name}' added!")

    def enroll_student(self, student_id: int, course_id: int):
        student = next((s for s in self.students if s.student_id == student_id), None)
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if student and course:
            course.students.append(student_id)
            print(f"✅ {student.name} enrolled in {course.name}")
        else:
            print("❌ Invalid Student/Course ID")

    # ATTENDANCE OPERATIONS
    def mark_attendance(self, course_id: int):
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if not course:
            print("❌ Course not found")
            return

        print(f"\n📚 Students in {course.name}:")
        for sid in course.students:
            student = next(s for s in self.students if s.student_id == sid)
            print(f"{sid}. {student.name}")

        present_ids = []
        while True:
            choice = input("Enter present student ID (0 to finish): ")
            if choice == '0':
                break
            if int(choice) in course.students:
                present_ids.append(int(choice))

        date = datetime.now().strftime("%Y-%m-%d")
        att = Attendance(self.next_att_id, course_id, date, present_ids)
        self.attendance.append(att)
        self.next_att_id += 1

        # Update student records
        for sid in course.students:
            student = next(s for s in self.students if s.student_id == sid)
            if course.name not in student.attendance_records:
                student.attendance_records[course.name] = []
            student.attendance_records[course.name].append(date)

        print(f"✅ Attendance marked for {len(present_ids)}/{len(course.students)} students")

    def view_attendance_report(self, student_id: int):
        student = next((s for s in self.students if s.student_id == student_id), None)
        if not student:
            print("❌ Student not found")
            return

        print(f"\n📊 {student.name} Attendance Report:")
        for course, dates in student.attendance_records.items():
            total_classes = len(dates)
            present = sum(1 for att in self.attendance
                          if student_id in att.present_students and
                          att.course_id == next(c.course_id for c in self.courses if c.name == course))
            percentage = (present / total_classes * 100) if total_classes > 0 else 0
            print(f"{course}: {present}/{total_classes} ({percentage:.1f}%)")

    def list_all_students(self):
        if not self.students:
            print("📚 No students")
            return
        print("\n👥 ALL STUDENTS:")
        for student in self.students:
            print(student)

    # DISPLAY MENU
    def display_menu(self):
        print("\n" + "=" * 50)
        print("🎓 COLLEGE ATTENDANCE SYSTEM")
        print("=" * 50)
        print("1.  👥 Add Student")
        print("2.  👨‍🏫 Add Faculty")
        print("3.  📚 Add Course")
        print("4.  📝 Enroll Student")
        print("5.  ✅ Mark Attendance")
        print("6.  📊 View Report")
        print("7.  📋 List Students")
        print("0.  ❌ Exit")
        print("=" * 50)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter choice (0-7): ").strip()

            if choice == '1':
                name = input("Student Name: ")
                roll_no = input("Roll No: ")
                course = input("Course: ")
                self.add_student(name, roll_no, course)

            elif choice == '2':
                name = input("Faculty Name: ")
                dept = input("Department: ")
                self.add_faculty(name, dept)

            elif choice == '3':
                name = input("Course Name: ")
                faculty_id = int(input("Faculty ID: "))
                self.add_course(name, faculty_id)

            elif choice == '4':
                sid = int(input("Student ID: "))
                cid = int(input("Course ID: "))
                self.enroll_student(sid, cid)

            elif choice == '5':
                cid = int(input("Course ID: "))
                self.mark_attendance(cid)

            elif choice == '6':
                sid = int(input("Student ID: "))
                self.view_attendance_report(sid)

            elif choice == '7':
                self.list_all_students()

            elif choice == '0':
                print("👋 Thank you for using Attendance System!")
                break

            else:
                print("❌ Invalid choice!")

            input("\nPress Enter to continue...")


# RUN THE SYSTEM
if __name__ == "__main__":
    system = AttendanceManagementSystem()
    system.run()
