from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SEARCH ----------------
@app.route("/search")
def search_page():
    return render_template("search.html")

# ---------------- CHECK CALLER ----------------
@app.route("/check_caller", methods=["POST"])
def check_caller():
    number = request.form["number"]
    org = request.form["org"]

    conn = sqlite3.connect("trusted_numbers.db")
    c = conn.cursor()
    c.execute(
        "SELECT organization, trust_level FROM trusted_numbers WHERE number=? AND organization=?",
        (number, org)
    )
    result = c.fetchone()
    conn.close()

    if result:
        return render_template(
            "result_yes.html",
            organization=result[0],
            trust_level=result[1]
        )
    else:
        return render_template(
            "result_no.html",
            number=number,
            org=org
        )

# ---------------- REPORT SPAM ----------------
@app.route("/report_spam", methods=["GET", "POST"])
def report_spam():
    number = request.args.get("number")
    org = request.args.get("org")

    if request.method == "POST":
        reason = request.form["reason"]

        conn = sqlite3.connect("trusted_numbers.db")
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS spam_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            organization TEXT,
            reason TEXT
        )
        """)

        c.execute(
            "INSERT INTO spam_reports (number, organization, reason) VALUES (?, ?, ?)",
            (number, org, reason)
        )

        conn.commit()
        conn.close()

        # ✅ REDIRECT TO SUCCESS PAGE
        return redirect(url_for("spam_success"))

    return render_template("report_spam.html", number=number, org=org)
@app.route("/spam_success")
def spam_success():
    return render_template("spam_success.html")


# ---------------- RISK LEVEL ----------------
@app.route("/risk", methods=["GET", "POST"])
@app.route("/risk", methods=["GET", "POST"])
def risk():
    risk_level = None
    report_count = 0

    if request.method == "POST":
        number = request.form["number"]

        conn = sqlite3.connect("trusted_numbers.db")
        c = conn.cursor()

        # Count spam reports for this number
        c.execute(
            "SELECT COUNT(*) FROM spam_reports WHERE number=?",
            (number,)
        )
        report_count = c.fetchone()[0]
        conn.close()

        # Decide risk level
        if report_count == 0:
            risk_level = "Low"
        elif report_count <= 2:
            risk_level = "Medium"
        else:
            risk_level = "High"

    return render_template(
        "risk_level.html",
        risk_level=risk_level,
        report_count=report_count
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
