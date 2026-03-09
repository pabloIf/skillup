from database import get_connection


def get_log_by_id(log_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, skill_id, date FROM logs WHERE id = ?",
            (log_id,)
        )
        row = cursor.fetchone()

    return dict(row) if row else None

def get_logs_by_skill_id(skill_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, skill_id, date FROM logs WHERE skill_id = ?",
            (skill_id,)
        )
        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def create_log(skill_id: int, log_date: str) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (skill_id, date) VALUES (?, ?)",
            (skill_id, log_date)
        )
        conn.commit()
        log_id = cursor.lastrowid

    return {"id": log_id, "skill_id": skill_id, "date": log_date}
    
def delete_log(log_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM logs WHERE id = ?",
            (log_id,)
        )
        conn.commit()

    return True

def delete_logs_by_skill_id(skill_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM logs WHERE skill_id = ?",
            (skill_id,)
        )
        conn.commit()
    
    return True