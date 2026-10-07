import sqlite3
import pandas as pd

DB_NAME = "student_assistant.db"
CSV_FILE = "data/students.csv"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Performance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            percentage REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # Read existing CSV
    df = pd.read_csv(CSV_FILE)

    # Add students
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO students
            (student_id, name, password)
            VALUES (?, ?, ?)
        """, (
            row["Student_ID"],
            row["Name"],
            str(row["Password"])
        ))

    # Add performance
    subjects = ["Python", "DBMS", "AI", "Data_Mining"]

    for _, row in df.iterrows():
        for subject in subjects:
            cursor.execute("""
                INSERT INTO performance
                (student_id, subject, marks)
                VALUES (?, ?, ?)
            """, (
                row["Student_ID"],
                subject,
                int(row[subject])
            ))

    # Add attendance
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO attendance
            (student_id, percentage)
            VALUES (?, ?)
        """, (
            row["Student_ID"],
            float(row["Attendance"])
        ))

    connection.commit()
    connection.close()

def clean_duplicates():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Keep only one performance record for each student + subject
    cursor.execute("""
        DELETE FROM performance
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM performance
            GROUP BY student_id, subject
        )
    """)

    # Keep only one attendance record for each student
    cursor.execute("""
        DELETE FROM attendance
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM attendance
            GROUP BY student_id
        )
    """)

    connection.commit()
    connection.close()

    print("Duplicate records removed successfully!")

def get_student(student_id, password):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
        WHERE student_id = ? AND password = ?
    """, (student_id, password))

    student = cursor.fetchone()

    if not student:
        connection.close()
        return None

    student_id, name = student

    cursor.execute("""
        SELECT subject, marks
        FROM performance
        WHERE student_id = ?
    """, (student_id,))

    performance = cursor.fetchall()

    cursor.execute("""
        SELECT percentage
        FROM attendance
        WHERE student_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (student_id,))

    attendance = cursor.fetchone()

    connection.close()

    student_data = {
        "Student_ID": student_id,
        "Name": name,
        "Python": 0,
        "DBMS": 0,
        "AI": 0,
        "Data_Mining": 0,
        "Attendance": attendance[0] if attendance else 0
    }

    for subject, marks in performance:
        if subject == "Data_Mining":
            student_data["Data_Mining"] = marks
        else:
            student_data[subject] = marks

    return student_data


if __name__ == "__main__":
    clean_duplicates()