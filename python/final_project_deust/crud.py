from database import get_db
from uuid import uuid4
import datetime

def create_robot(name: str, addressMac: str, mission: str = "None"):
    conn = get_db()
    cursor = conn.cursor()
    robot_id = str(uuid4())
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO robots (id, name, addressMAC, created_at, mission) VALUES (?, ?, ?, ?, ?)", (robot_id, name, addressMac,now, mission))
    conn.commit()
    conn.close()
    return robot_id

def delete_robot(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM robots WHERE id = ?", (robot_id,))
    conn.commit()
    conn.close()

def get_robots():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM robots")
    result = cursor.fetchall()
    conn.close()
    return result

def get_status():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT robots.name, robot_id, timestamp, ligne, status FROM status JOIN robots ON status.robot_id = robots.id ORDER BY timestamp DESC")
    result = cursor.fetchall()
    conn.close()
    return result

def add_status(robot_id, position, status):
    conn = get_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO status (robot_id, timestamp, ligne, status) VALUES (?, ?, ?, ?)", (robot_id, timestamp, position, status))
    conn.commit()
    conn.close()

def get_last_status(robot_id: str):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT timestamp, ligne, status
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
            "ligne": row[1],
            "status": row[2]
        }
    else:
        return {"message": "Aucun état trouvé pour ce robot"}
    
def get_instructions(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT instructions
        FROM robots
        WHERE id = ?
    """, (robot_id,))
    
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"instructions": row[0]}
    else:
        return {"message": "Aucun robot trouvé avec cet ID"}
    
def create_instruction(robot_id: str, instruction: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO instructions (robot_id, instruction)
        VALUES (?, ?)
    """, (robot_id, instruction))
    
    conn.commit()
    conn.close()
    
    return {"message": "Instruction créée avec succès"}

def delete_instruction(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM instructions
        WHERE robot_id = ?
    """, (robot_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Instruction supprimée avec succès"}