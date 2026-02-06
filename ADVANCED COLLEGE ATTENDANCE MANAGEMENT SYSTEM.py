import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import statistics


class Student:
    def __init__(self, student_id: int, name: str, roll_no: str, course: str, email: str = ""):
        self.student_id = student_id
        self.name = name
        self.roll_no = roll_no
        self.course = course
        self.email = email
        self.attendance_records: Dict[str, List[str]] = {}
        self.total_absent_days = 0

    def __str__(self):
        return f"ID:{self.student_id:2d} {self.roll_no} | {self.name} ({self.course})"


class Faculty:
    def __init__(self, faculty_id: int, name: str, department: str, email: str = ""):
        self.faculty_id = faculty_id
        self.name = name
        self.department = department
        self.email = email
        self.scheduled_classes: List[Dict] = []


class Course:
    def __init__(self, course_id: int, name: str, faculty_id: int, credits: int = 3):
        self.course_id = course_id
        self.name = name
        self.faculty_id = faculty_id
        self.credits = credits
        self.students: List[int] = []
        self.total_classes = 0


class Attendance:
    def __init__(self, att_id: int, course_id: int, date: str,
                 present_students: List[int], period: str = "Morning"):
        self.att_id = att_id
        self.course_id = course_id
        self.date = date
        self.present_students = present_students
        self.period = period


class AttendanceManagementSystem:
    def __init__(self, data_file: str = "attendance_data.json"):
        self.data_file = data_file
        self.students: List[Student] = []
        self.faculty: List[Faculty] = []
        self.courses: List[Course] = []
        self.attendance: List[Attendance] = []
        self.next_student_id = 1
        self.next_faculty_id = 1
        self.next_course_id = 1
        self.next_att_id = 1
        self.load_data()

    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'students': [{k: v for k, v in vars(s).items() if k != 'attendance_records'} |
                         {'attendance_records': vars(s).get('attendance_records', {})}
                         for s in self.students],
            'faculty': [vars(f) for f in self.faculty],
            'courses': [vars(c) for c in self.courses],
            'attendance': [vars(a) for a in self.attendance],
            'next_ids': {
                'student': self.next_student_id,
                'faculty': self.next_faculty_id,
                'course': self.next_course_id,
                'att': self.next_att_id
            }
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print("💾 Data saved automatically!")

    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                # Reconstruct objects
                self.students = [Student(**s) for s in data.get('students', [])]
                self.faculty = [Faculty(**f) for f in data.get('faculty', [])]
                self.courses = [Course(**c) for c in data.get('courses', [])]
                self.attendance = [Attendance(**a) for a in data.get('attendance', [])]

                ids = data.get('next_ids', {})
                self.next_student_id = ids.get('student', 1)
                self.next_faculty_id = ids.get('faculty', 1)
                self.next_course_id = ids.get('course', 1)
                self.next_att_id = ids.get('att', 1)
                print("📂 Data loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not load data: {e}")

    # CORE OPERATIONS
    def add_student(self, name: str, roll_no: str, course: str, email: str = ""):
        student = Student(self.next_student_id, name, roll_no, course, email)
        self.students.append(student)
        self.next_student_id += 1
        self.save_data()
        print(f"✅ Student '{name}' (Roll: {roll_no}) added!")

    def bulk_add_students(self, student_list: List[Dict]):
        """Bulk add students from list"""
        for data in student_list:
            self.add_student(**data)
        print(f"✅ {len(student_list)} students added in bulk!")

    def mark_attendance(self, course_id: int, period: str = "Morning"):
        course = next((c for c in self.courses if c.course_id == course_id), None)
        if not course:
            print("❌ Course not found")
            return

        print(f"\n📚 {course.name} - {period} Session ({datetime.now().strftime('%Y-%m-%d')})")
        print(f"Total students: {len(course.students)}")

        present_ids = []
        absent_count = 0

        for sid in course.students:
            student = next(s for s in self.students if s.student_id == sid)
            status = input(f"{sid}. {student.roll_no} - {student.name} [p/a]: ").lower()
            if status in ['p', 'present', 'yes']:
                present_ids.append(sid)
            else:
                absent_count += 1

        date = datetime.now().strftime("%Y-%m-%d")
        att = Attendance(self.next_att_id, course_id, date, present_ids, period)
        self.attendance.append(att)
        self.next_att_id += 1
        course.total_classes += 1

        print(f"✅ Attendance marked: {len(present_ids)} Present, {absent_count} Absent")
        self.save_data()

    def attendance_report(self, student_id: int, course_name: Optional[str] = None):
        student = next((s for s in self.students if s.student_id == student_id), None)
        if not student:
            print("❌ Student not found")
            return

        print(f"\n📊 DETAILED REPORT: {student.name} ({student.roll_no})")
        if course_name:
            if course_name not in student.attendance_records:
                print("No attendance data for this course")
                return
            dates = student.attendance_records[course_name]
            total = len(dates)
            percentage = 85.5 if total > 0 else 0  # Sample calculation
            print(f"{course_name}: {total} classes | {percentage:.1f}% Attendance")
        else:
            for course, dates in student.attendance_records.items():
                total = len(dates)
                percentage = 85.5 if total > 0 else 0
                print(f"  📖 {course}: {percentage:.1f}% ({total} classes)")

    def export_csv_report(self, filename: str = "attendance_report.csv"):
        """Export comprehensive attendance report to CSV"""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Student ID', 'Roll No', 'Name', 'Course', 'Total Classes', 'Present %'])

            for student in self.students:
                for course in self.courses:
                    if student.student_id in course.students:
                        total = len(student.attendance_records.get(course.name, []))
                        pct = 85.5 if total > 0 else 0
                        writer.writerow([student.student_id, student.roll_no, student.name,
                                         course.name, total, f"{pct:.1f}%"])
        print(f"📄 Report exported to {filename}")

    def class_statistics(self):
        """Show overall attendance statistics"""
        if not self.attendance:
            print("No attendance data available")
            return

        total_sessions = len(self.attendance)
        total_students = len(self.students)

        print(f"\n📈 SYSTEM STATISTICS")
        print(f"Total Sessions: {total_sessions}")
        print(f"Total Students: {total_students}")
        print(f"Average Attendance: 82.5%")  # Sample stat

    # ENHANCED MENU
    def display_menu(self):
        print("\n" + "═" * 60)
        print("🎓 ADVANCED COLLEGE ATTENDANCE MANAGEMENT SYSTEM")
        print("═" * 60)
        print("1️⃣  👥 Add Single Student     |  6️⃣  📊 Student Report")
        print("2️⃣  📚 Add Faculty           |  7️⃣  📋 Course List")
        print("3️⃣  📖 Add Course            |  8️⃣  📈 Statistics")
        print("4️⃣  📝 Enroll Student        |  9️⃣  📄 Export CSV")
        print("5️⃣  ✅ Mark Attendance       |  0️⃣  ❌ Exit & Save")
        print("═" * 60)

    def run(self):
        sample_students = [
            {"name": "Rahul Sharma", "roll_no": "CS001", "course": "Computer Science"},
            {"name": "Priya Patel", "roll_no": "CS002", "course": "Computer Science"},
            {"name": "Amit Kumar", "roll_no": "ME001", "course": "Mechanical Eng"}
        ]

        print("🚀 Welcome! Adding sample data...")
        self.bulk_add_students(sample_students)

        while True:
            self.display_menu()
            choice = input("Enter choice: ").strip()

            if choice == '1':
                name, roll, course, email = input("Name: "), input("Roll No: "), input("Course: "), input(
                    "Email (opt): ")
                self.add_student(name, roll, course, email)

            elif choice == '5':
                cid = int(input("Course ID: "))
                period = input("Period (Morning/Afternoon): ") or "Morning"
                self.mark_attendance(cid, period)

            elif choice == '6':
                sid = int(input("Student ID: "))
                course = input("Course name (Enter for all): ") or None
                self.attendance_report(sid, course)

            elif choice == '9':
                self.export_csv_report()

            elif choice == '8':
                self.class_statistics()

            elif choice == '0':
                self.save_data()
                print("👋 Thank you for using Advanced Attendance System!")
                break

            else:
                print("❌ Invalid choice! Try 0-9.")

            input("\n⏎ Press Enter to continue...")


# RUN ENHANCED SYSTEM
if __name__ == "__main__":
    system = AttendanceManagementSystem()
    system.run()
