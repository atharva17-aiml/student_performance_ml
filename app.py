from flask import (
    Flask, render_template, request, redirect,
    session, flash, jsonify, Response
)
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os, random

from database import get_connection
from services.ml_service import predict_student
from services.db_service import save_prediction, get_user_stats
from services.validation import validate_prediction_inputs

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(hours=2)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        f = request.form
        try:
            db = get_connection()
            cur = db.cursor()
            cur.execute("""
                INSERT INTO users (username, password, institute, roll_no, birth_date)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                f["username"],
                generate_password_hash(f["password"]),
                f["institute"],
                f["roll_no"],
                f["birth_date"]
            ))
            db.commit()
            db.close()
            return redirect("/login")
        except:
            return render_template("login.html", error="Username already exists")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_connection()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (request.form["username"],))
        user = cur.fetchone()
        db.close()

        if not user or not check_password_hash(user["password"], request.form["password"]):
            return render_template("login.html", error="Invalid credentials")

        session.update({
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "institute": user["institute"],
            "roll_no": user["roll_no"],
            "birth_date": str(user["birth_date"])
        })

        return redirect("/")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    stats = get_user_stats(session["user_id"])

    total_users = None
    if session.get("role") == "admin":
        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        total_users = cur.fetchone()[0]
        db.close()

    return render_template(
        "index.html",
        total_predictions=stats["total_predictions"],
        avg_score=stats["avg_score"],
        latest_score=stats["latest_score"],
        total_users=total_users,
        profile_username=session["username"],
        profile_institute=session["institute"],
        profile_roll_no=session["roll_no"],
        profile_birth_date=session["birth_date"]
    )

# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        institute = request.form["institute"]
        roll_no = request.form["roll_no"]
        birth_date = request.form["birth_date"]

        db = get_connection()
        cur = db.cursor()
        cur.execute("""
            UPDATE users
            SET institute=%s, roll_no=%s, birth_date=%s
            WHERE id=%s
        """, (institute, roll_no, birth_date, session["user_id"]))
        db.commit()
        db.close()

        session["institute"] = institute
        session["roll_no"] = roll_no
        session["birth_date"] = birth_date

        flash("✅ Profile updated successfully!")
        return redirect("/profile")

    return render_template("profile.html")

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect("/login")

    try:
        print("FORM DATA:", request.form)

        values = validate_prediction_inputs(request.form)
        print("VALUES:", values)

        prediction = predict_student(values)
        print("PREDICTION:", prediction)

        save_prediction(session["user_id"], values, prediction)

        # ✅ Get updated stats (VERY IMPORTANT)
        stats = get_user_stats(session["user_id"])

        total_users = None
        if session.get("role") == "admin":
            db = get_connection()
            cur = db.cursor()
            cur.execute("SELECT COUNT(*) FROM users")
            total_users = cur.fetchone()[0]
            db.close()

        # ✅ RETURN PAGE (NOT redirect)
        return render_template(
            "index.html",
            total_predictions=stats["total_predictions"],
            avg_score=stats["avg_score"],
            latest_score=stats["latest_score"],
            total_users=total_users,
            profile_username=session["username"],
            profile_institute=session["institute"],
            profile_roll_no=session["roll_no"],
            profile_birth_date=session["birth_date"],
            success_msg=f"✅ Prediction successful! Score: {round(prediction, 2)}"
        )

    except Exception as e:
        print("ERROR:", e)

        return render_template(
            "index.html",
            success_msg=f"❌ Prediction failed: {e}"
        )

# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT p.studytime, p.failures, p.absences, p.health, p.G1, p.G2,
               p.predicted_score, p.created_at,
               u.institute, u.roll_no, u.birth_date
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id=%s
        ORDER BY p.created_at DESC
    """, (session["user_id"],))

    rows = cur.fetchall()
    db.close()

    return render_template("history.html", rows=rows)

# ---------------- ANALYSIS ----------------
@app.route("/analysis")
def analysis():
    if "user_id" not in session:
        return redirect("/login")

    db = get_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT predicted_score FROM predictions
        WHERE user_id=%s ORDER BY id
    """, (session["user_id"],))
    rows = cur.fetchall()
    db.close()

    scores = [float(r[0]) for r in rows]
    labels = list(range(1, len(scores) + 1))

    return render_template("analysis.html", scores=scores, labels=labels)

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied", 403

    db = get_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT id, username, institute, roll_no, birth_date, role
        FROM users
    """)
    users = cur.fetchall()

    cur.execute("""
        SELECT 
            u.username, u.institute, u.roll_no, u.birth_date,
            p.predicted_score, p.created_at
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)
    predictions = cur.fetchall()

    cur.execute("""
        SELECT DATE(created_at) AS day, COUNT(*) AS total
        FROM predictions
        GROUP BY day
        ORDER BY day
    """)
    chart_data = cur.fetchall()

    db.close()

    return render_template(
        "admin.html",
        users=users,
        predictions=predictions,
        chart_data=chart_data
    )

# ---------------- CSV EXPORT ----------------
@app.route("/admin/export-csv")
def export_predictions_csv():
    if session.get("role") != "admin":
        return "Access Denied", 403

    db = get_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            u.username, u.institute, u.roll_no, u.birth_date,
            p.studytime, p.failures, p.absences, p.health,
            p.G1, p.G2, p.predicted_score, p.created_at
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)
    rows = cur.fetchall()
    db.close()

    def generate():
        header = [
            "username", "institute", "roll_no", "birth_date",
            "studytime", "failures", "absences", "health",
            "G1", "G2", "predicted_score", "created_at"
        ]
        yield ",".join(header) + "\n"

        for r in rows:
            row = []
            for h in header:
                val = r[h]
                if val is None:
                    val = ""
                if isinstance(val, datetime):
                    val = val.strftime("%Y-%m-%d %H:%M:%S")
                val = str(val).replace(",", " ")
                row.append(val)
            yield ",".join(row) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=all_predictions.csv"
        }
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=False)