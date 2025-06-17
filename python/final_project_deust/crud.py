from database import get_db
from uuid import uuid4
import datetime

def create_robot(name: str, uuid: str, mission: str = "None"):
    conn = get_db()
    cursor = conn.cursor()
    robot_id = str(uuid4())
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO robots (id, name, uuid, created_at, mission) VALUES (?, ?, ?, ?, ?)", (robot_id, name, uuid,now, mission))
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


def get_robot_by_uuid(uuid: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT robots.id, robots.uuid, robots.name, robots.created_at, robots.mission,
               instructions.id AS inst_id, instructions.blocks
        FROM robots
        JOIN instructions ON robots.id = instructions.robot_id
        WHERE robots.uuid = ?
        ORDER BY instructions.id DESC
        LIMIT 1
    """, (uuid,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "mac_address": result[1],
            "name": result[2],
            "created_at": result[3],
            "mission": result[4],
            "inst_id": result[5],
            "instruction": result[6]
        }
    else:
        return {"message": "Aucun état trouvé pour ce robot"}


def get_status():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT robots.name, robot_id, timestamp, ligne, status FROM status JOIN robots ON status.robot_id = robots.id ORDER BY timestamp DESC")
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_status_by_uuid(uuid: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status.timestamp, status.ligne, status.status, status.instructionId, robots.id
        FROM status 
        JOIN robots ON status.robot_id = robots.id
        WHERE robots.uuid = ?
        ORDER BY timestamp DESC
    """, (uuid,))
    
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return [
            {
                "robot_id": row[4],
                "timestamp": row[0],
                "ligne": row[1],
                "status": row[2],
                "instructionId": row[3]
            } for row in rows
        ]
    else:
        return {"message": "Aucun état trouvé pour ce robot"}

def add_status(robot_id, instructionID, position, status):
    conn = get_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO status (robot_id, instructionID, timestamp, ligne, status) VALUES (?, ?, ?, ?, ?)", (robot_id, instructionID, timestamp, position, status))
    conn.commit()
    conn.close()

def get_last_status(uuid: str):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT status.timestamp, status.ligne, status.status, status.instructionId, robots.id
        FROM status 
        JOIN robots ON status.robot_id = robots.id
        WHERE robots.uuid = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (uuid,))
    
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "robot_id": row[4],
            "timestamp": row[0],
            "ligne": row[1],
            "status": row[2],
            "instructionId": row[3]
        }
    else:
        return {"message": "Aucun état trouvé pour ce robot"}
    
def get_instructions(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT mission
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
        INSERT INTO instructions (robot_id, blocks)
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

def add_telemetry(robot_id: str, vitesse: float, distance_ultrasons: float, status_deplacement: str, ligne: str, status_pince: str):
    conn = get_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO telemetry (robot_id, timestamp, vitesse, distance_ultrasons, status_deplacement, ligne, status_pince)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (robot_id, timestamp, vitesse, distance_ultrasons, status_deplacement, ligne, status_pince))
    
    conn.commit()
    conn.close()
    
    return {"message": "Telemetry data added successfully"}