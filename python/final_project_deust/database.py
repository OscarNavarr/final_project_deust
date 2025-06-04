import sqlite3

DB_NAME = "robots.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn
