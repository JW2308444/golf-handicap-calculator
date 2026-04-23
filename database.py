import sqlite3


def create_database():

    # Connect to the SQLite database file
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    # Create the rounds table if it does not already exist
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

    # Create the courses table if it does not already exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating REAL,
        slope INTEGER
    )
    """)

    conn.commit()

    # Check whether the courses table already contains data
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]

    # Insert default golf courses only if the table is empty
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

    # Open the database and load all saved course details
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, rating, slope FROM courses")

    courses = cursor.fetchall()

    conn.close()

    return courses


def add_round(date, course, score, course_rating, slope_rating, differential):

    # Insert a new golf round into the rounds table
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rounds (date, course, score, course_rating, slope_rating, differential)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, course, score, course_rating, slope_rating, differential))

    conn.commit()
    conn.close()


def get_rounds():

    # Retrieve all rounds ordered by most recent date first
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rounds ORDER BY date DESC")

    rounds = cursor.fetchall()

    conn.close()

    return rounds


def delete_round(round_id):

    # Remove one round using its unique database ID
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rounds WHERE id = ?", (round_id,))

    conn.commit()
    conn.close()


def get_differentials():

    # Load all differentials in date order for analysis
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT differential FROM rounds ORDER BY date ASC")

    data = cursor.fetchall()

    conn.close()

    return [row[0] for row in data]


def get_statistics():

    # Calculate total rounds, average score, best score, and worst score
    conn = sqlite3.connect("golf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(score), MIN(score), MAX(score) FROM rounds")

    stats = cursor.fetchone()

    conn.close()

    return stats