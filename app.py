from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL,
            semester TEXT NOT NULL,
            subject TEXT NOT NULL,
            faculty TEXT NOT NULL,
            overall_rating INTEGER NOT NULL,
            teaching_quality INTEGER NOT NULL,
            course_content INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            sentiment TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_feedback():

    data = request.json

    name = data["name"]
    email = data["email"]
    course = data["course"]
    semester = data["semester"]
    subject = data["subject"]
    faculty = data["faculty"]
    overall_rating = data["overall_rating"]
    teaching_quality = data["teaching_quality"]
    course_content = data["course_content"]
    feedback = data["feedback"]

    polarity = TextBlob(feedback).sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (name, email, course, semester, subject, faculty,
         overall_rating, teaching_quality, course_content,
         feedback, sentiment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        course,
        semester,
        subject,
        faculty,
        overall_rating,
        teaching_quality,
        course_content,
        feedback,
        sentiment
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Feedback submitted successfully!",
        "sentiment": sentiment
    })
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard-data")
def dashboard_data():

    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment = 'Positive'"
    )
    positive = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment = 'Neutral'"
    )
    neutral = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM feedback WHERE sentiment = 'Negative'"
    )
    negative = cursor.fetchone()[0]

    cursor.execute("""
        SELECT name, course, subject, overall_rating, sentiment
        FROM feedback
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    feedback = []

    for row in rows:
        feedback.append({
            "name": row[0],
            "course": row[1],
            "subject": row[2],
            "rating": row[3],
            "sentiment": row[4]
        })

    cursor.execute("""
        SELECT overall_rating, COUNT(*)
        FROM feedback
        GROUP BY overall_rating
        ORDER BY overall_rating
    """)

    rating_rows = cursor.fetchall()

    ratings = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }

    for row in rating_rows:
        ratings[str(row[0])] = row[1]

    conn.close()

    return jsonify({
        "total": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "feedback": feedback,
        "ratings": ratings
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)