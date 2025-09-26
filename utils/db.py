import sqlite3
import pandas as pd

DB_PATH = "data/resume_db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT
    )
    """)
    # --- Migration: ensure predicted_score column exists ---
    try:
        cur.execute("ALTER TABLE resumes ADD COLUMN predicted_score REAL;")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    conn.commit()
    conn.close()

def insert_resume(row: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resumes 
        (filename, name, email, phone, skills, education, experience, predicted_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row.get("filename"),
        row.get("name"),
        row.get("email"),
        row.get("phone"),
        row.get("skills"),
        row.get("education"),
        row.get("experience"),
        row.get("predicted_score")
    ))
    conn.commit()
    conn.close()

def fetch_resumes():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM resumes", conn)
    conn.close()
    return df

def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM resumes")
    conn.commit()
    conn.close()
