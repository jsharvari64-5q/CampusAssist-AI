import sqlite3

DB_NAME = "campusassist.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            importance INTEGER NOT NULL,
            days_left INTEGER NOT NULL,
            study_time REAL NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def add_task(subject, topic, difficulty, importance, days_left, study_time):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (subject, topic, difficulty, importance, days_left, study_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        subject,
        topic,
        difficulty,
        importance,
        days_left,
        study_time
    ))

    connection.commit()
    connection.close()


def get_tasks():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, subject, topic, difficulty, importance,
               days_left, study_time, completed
        FROM tasks
    """)

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "subject": row[1],
            "topic": row[2],
            "difficulty": row[3],
            "importance": row[4],
            "days_left": row[5],
            "study_time": row[6],
            "completed": bool(row[7])
        })

    return tasks


def mark_completed(task_id, completed=True):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = ?
        WHERE id = ?
    """, (int(completed), task_id))

    connection.commit()
    connection.close()


create_database()
