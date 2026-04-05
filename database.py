import sqlite3


def create_database():

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    # Rounds table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        course TEXT,
        score INTEGER,
        course_rating REAL,
        slope_rating INTEGER,
        differential REAL
    )
    """)

    # Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating REAL,
        slope INTEGER
    )
    """)

    conn.commit()

    # Insert sample courses if table empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]

    if count == 0:

        courses = [
("St Andrews Old Course", 73.2, 132),
("Augusta National", 76.2, 148),
("Pebble Beach", 74.7, 143),
("Royal Troon", 71.5, 128),
("Royal Birkdale", 74.1, 133)
]

        cursor.executemany(
            "INSERT INTO courses (name, rating, slope) VALUES (?, ?, ?)",
            courses
        )

    conn.commit()
    conn.close()


def get_courses():

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, rating, slope FROM courses")

    courses = cursor.fetchall()

    conn.close()

    return courses


def add_round(date, course, score, course_rating, slope_rating, differential):

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rounds (date, course, score, course_rating, slope_rating, differential)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, course, score, course_rating, slope_rating, differential))

    conn.commit()
    conn.close()


def get_rounds():

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rounds ORDER BY date DESC")

    rounds = cursor.fetchall()

    conn.close()

    return rounds


def delete_round(round_id):

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rounds WHERE id = ?", (round_id,))

    conn.commit()
    conn.close()


def get_differentials():

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT differential FROM rounds ORDER BY date ASC")

    data = cursor.fetchall()

    conn.close()

    return [row[0] for row in data]


def get_statistics():

    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(score), MIN(score), MAX(score) FROM rounds")

    stats = cursor.fetchone()

    conn.close()

    return stats