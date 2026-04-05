from flask import Flask, render_template, request, Response
from handicap import calculate_differential, handicap_progression
from database import create_database, add_round, get_rounds, delete_round, get_courses
import csv
import io

app = Flask(__name__)

create_database()


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard")
def home():

    rounds = get_rounds()

    rounds_played = len(rounds)

    scores = [r[3] for r in rounds]
    differentials = [r[6] for r in rounds]

    if scores:
        best_score = min(scores)
        worst_score = max(scores)
    else:
        best_score = "-"
        worst_score = "-"

    handicap = "-"

    if len(differentials) >= 3:
        last20 = differentials[:20]
        sorted_diffs = sorted(last20)
        best8 = sorted_diffs[:8]
        handicap = round(sum(best8) / len(best8), 2)

    progression = handicap_progression(rounds)

    return render_template(
        "index.html",
        handicap=handicap,
        rounds_played=rounds_played,
        best_score=best_score,
        worst_score=worst_score,
        differentials=differentials,
        progression=progression
    )


@app.route("/add-round", methods=["GET", "POST"])
def add_round_page():

    courses = get_courses()

    if request.method == "POST":

        date = request.form["date"]
        course = request.form["course"]
        score = int(request.form["score"])
        course_rating = float(request.form["course_rating"])
        slope_rating = int(request.form["slope_rating"])

        differential = calculate_differential(score, course_rating, slope_rating)

        add_round(date, course, score, course_rating, slope_rating, differential)

    return render_template("add_round.html", courses=courses)


@app.route("/rounds")
def rounds_page():
    rounds = get_rounds()
    return render_template("rounds.html", rounds=rounds)


@app.route("/delete/<int:round_id>")
def delete_round_route(round_id):
    delete_round(round_id)
    return rounds_page()


@app.route("/handicap-details")
def handicap_details():

    rounds = get_rounds()
    last20 = rounds[:20]

    differentials = [r[6] for r in last20]
    sorted_diffs = sorted(differentials)
    best8 = sorted_diffs[:8]

    handicap = None
    if best8:
        handicap = round(sum(best8) / len(best8), 2)

    return render_template(
        "handicap_details.html",
        rounds=last20,
        best8=best8,
        handicap=handicap
    )


@app.route("/export")
def export_csv():

    rounds = get_rounds()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Date",
        "Course",
        "Score",
        "Course Rating",
        "Slope Rating",
        "Differential"
    ])

    for r in rounds:
        writer.writerow([r[1], r[2], r[3], r[4], r[5], r[6]])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=golf_rounds.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)