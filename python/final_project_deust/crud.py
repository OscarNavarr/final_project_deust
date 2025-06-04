from database import get_db
from uuid import uuid4
import datetime

def create_robot(name):
    conn = get_db()
    cursor = conn.cursor()
    robot_id = str(uuid4())
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO robots (id, name, created_at) VALUES (?, ?, ?)", (robot_id, name, now))
    conn.commit()
    conn.close()
    return robot_id

def get_robots():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, created_at FROM robots")
    result = cursor.fetchall()
    conn.close()
    return result

def add_status(robot_id, position, status):
    conn = get_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO status (robot_id, timestamp, position, status) VALUES (?, ?, ?, ?)", (robot_id, timestamp, position, status))
    conn.commit()
    conn.close()

def get_last_status(robot_id: str):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT timestamp, position, status
        FROM status
        WHERE robot_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (robot_id,))
    
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "timestamp": row[0],
            "position": row[1],
            "status": row[2]
        }
    else:
        return {"message": "Aucun état trouvé pour ce robot"}