from database import get_connection


# ---------------- SAVE PREDICTION ----------------

def save_prediction(user_id, values, prediction):
    print("Saving prediction for user:", user_id)  # debug

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions
        (user_id, studytime, failures, absences, health, G1, G2, predicted_score)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (user_id, *values, prediction))

    conn.commit()
    conn.close()


# ---------------- USER DASHBOARD STATS ----------------

def get_user_stats(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # total predictions
    cur.execute("SELECT COUNT(*) AS total FROM predictions WHERE user_id=%s", (user_id,))
    total_predictions = cur.fetchone()["total"]

    # average score
    cur.execute("SELECT AVG(predicted_score) AS avg_score FROM predictions WHERE user_id=%s", (user_id,))
    avg_score = cur.fetchone()["avg_score"]

    # latest score
    cur.execute("""
        SELECT predicted_score
        FROM predictions
        WHERE user_id=%s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    latest = cur.fetchone()

    conn.close()

    return {
        "total_predictions": total_predictions,
        "avg_score": round(avg_score, 2) if avg_score else 0,
        "latest_score": latest["predicted_score"] if latest else None
    }


# ---------------- USER ROLE (ADMIN / USER) ----------------

def get_user_role(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()

    conn.close()

    return row["role"] if row else None
