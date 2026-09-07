import pandas as pd


def analyze_student(student_name):
    data = pd.read_csv("data/students.csv")

    student = data[data["Name"].str.lower() == student_name.lower()]

    if student.empty:
        return None, f"Student '{student_name}' was not found."

    student = student.iloc[0]

    subjects = {
        "Python": student["Python"],
        "DBMS": student["DBMS"],
        "AI": student["AI"],
        "Data Mining": student["Data_Mining"]
    }

    weak_subjects = {
        subject: mark
        for subject, mark in subjects.items()
        if mark < 60
    }

    result = f"Student: {student['Name']}\n"
    result += f"Attendance: {student['Attendance']}%\n"

    if weak_subjects:
        result += "Subjects needing improvement:\n"

        for subject, mark in weak_subjects.items():
            result += f"- {subject}: {mark}%\n"
    else:
        result += "No major weak subjects found."

    return weak_subjects, result