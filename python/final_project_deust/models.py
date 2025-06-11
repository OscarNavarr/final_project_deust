import sqlite3
from uuid import uuid4

DB_NAME = "robots.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS robots (
        id TEXT PRIMARY KEY,
        addressMAC TEXT NOT NULL,
        name TEXT,
        created_at TEXT,
        mission TEXT DEFAULT 'None'
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS status (
        robot_id TEXT,
        timestamp TEXT,
        ligne INTEGER,
        instructionId INTEGER,
        status TEXT,
        FOREIGN KEY(robot_id) REFERENCES robots(id)     
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT,
        instruction TEXT,
        FOREIGN KEY(robot_id) REFERENCES robots(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS telemetry(
        vitesse FLOAT,
        distance_ultrasons FLOAT,
        status_deplacement TEXT,
        ligne INTEGER,
        pince_active BOOLEAN,
        robot_id TEXT,
        FOREIGN KEY(robot_id) REFERENCES robots(id)
              )
    """)
    conn.commit()
    conn.close()
