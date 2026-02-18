import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONNECTION ----------------

def get_connection():
    """
    Returns a new MySQL database connection using environment variables.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        autocommit=False
    )

# ---------------- OPTIONAL: AUTO CREATE TABLES ----------------

def init_db():
    db = get_connection()
    cur = db.cursor()

    # USERS TABLE (with role)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        institute VARCHAR(255),
        roll_no VARCHAR(100),
        birth_date DATE,
        role ENUM('user','admin') DEFAULT 'user',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # PREDICTIONS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        studytime INT NOT NULL,
        failures INT NOT NULL,
        absences INT NOT NULL,
        health INT NOT NULL,
        G1 INT NOT NULL,
        G2 INT NOT NULL,
        predicted_score FLOAT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # PASSWORD RESET OTP TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS password_otp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        otp VARCHAR(10) NOT NULL,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    db.commit()
    db.close()
    print("✅ Database tables ready.")

# Run manually if needed
if __name__ == "__main__":
    init_db()
