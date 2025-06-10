import sqlite3
from uuid import uuid4

DB_NAME = "robots.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS robots (
        id TEXT PRIMARY KEY,
        name TEXT,
        created_at TEXT,
        mission TEXT DEFAULT 'None'
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS status (
        robot_id TEXT,
        timestamp TEXT,
        position TEXT,
        status TEXT,
        FOREIGN KEY(robot_id) REFERENCES robots(id)
    )
    """)
    conn.commit()
    conn.close()
