import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'veerai.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_message TEXT,
        bot_response TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        category TEXT,
        score INTEGER,
        total INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS current_affairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        category TEXT,
        date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ssb_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        stage TEXT,
        questions_asked TEXT,
        answers TEXT,
        score INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS olq_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        scores TEXT,
        report TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Seed current affairs
    c.execute("SELECT COUNT(*) FROM current_affairs")
    if c.fetchone()[0] == 0:
        seed_current_affairs(c)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def seed_current_affairs(c):
    affairs = [
        ("Operation Sindoor 2025", "India launched Operation Sindoor in May 2025, striking 9 terrorist camps in Pakistan and POK following the Pahalgam terror attack. The operation demonstrated India's precision strike capability and zero-tolerance policy against cross-border terrorism.", "Operations", "May 2025"),
        ("Rafale Marine Deal", "India signed a deal for 26 Rafale Marine jets for the Indian Navy at a cost of approximately Rs 63,000 crore. These carrier-based fighters will operate from INS Vikrant.", "Procurement", "2025"),
        ("DRDO AMCA Programme", "India's Advanced Medium Combat Aircraft (AMCA) programme achieved key milestones. This 5th generation stealth fighter is being developed by DRDO and HAL for the Indian Air Force.", "Technology", "2025"),
        ("SCO Military Summit", "India participated in the Shanghai Cooperation Organisation (SCO) Defence Ministers' meeting, reaffirming commitment to regional security and counter-terrorism cooperation.", "International", "2025"),
        ("Exercise Tasman Saber", "India participated in Tasman Saber 2025 multilateral military exercise with Australia and USA, focusing on maritime security and joint operations.", "Exercises", "2025"),
        ("Agniveer Scheme Update", "The government announced enhanced benefits and revised retention policy for Agniveers, with provisions for priority in central government jobs after 4-year service period.", "Policy", "2025"),
        ("INS Nilgiri Commissioned", "INS Nilgiri, the lead ship of Project 17A frigates (Nilgiri-class), was commissioned into Indian Navy. These are advanced stealth frigates with superior sensors and weapons.", "Navy", "2025"),
        ("India Defence Budget 2025", "India's Defence Budget for 2025-26 was set at approximately Rs 6.81 lakh crore, reflecting 9.5% increase with focus on indigenisation and modernisation.", "Policy", "2025"),
        ("Malabar Exercise 2025", "Exercise Malabar 2025 was conducted between navies of India, USA and Japan focusing on anti-submarine warfare, air defence and maritime domain awareness.", "Exercises", "2025"),
        ("LCA Tejas Mk2 Progress", "HAL's LCA Tejas Mk2 programme achieved significant design milestones. The more capable variant with AESA radar and enhanced weapons capability is expected to fly by 2026.", "Technology", "2025"),
    ]
    for a in affairs:
        c.execute("INSERT INTO current_affairs (title, content, category, date) VALUES (?,?,?,?)", a)

def save_chat(session_id, user_msg, bot_resp):
    conn = get_connection()
    conn.execute("INSERT INTO chat_history (session_id, user_message, bot_response) VALUES (?,?,?)",
                 (session_id, user_msg, bot_resp))
    conn.commit()
    conn.close()

def save_quiz_score(session_id, category, score, total):
    conn = get_connection()
    conn.execute("INSERT INTO quiz_scores (session_id, category, score, total) VALUES (?,?,?,?)",
                 (session_id, category, score, total))
    conn.commit()
    conn.close()

def get_current_affairs(category=None, limit=10):
    conn = get_connection()
    if category:
        rows = conn.execute("SELECT * FROM current_affairs WHERE category=? ORDER BY id DESC LIMIT ?",
                           (category, limit)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM current_affairs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_quiz_scores(session_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM quiz_scores WHERE session_id=? ORDER BY timestamp DESC",
                       (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
