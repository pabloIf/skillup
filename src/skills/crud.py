from database import get_connection

def get_all_skills():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name FROM skills"
        )
        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def get_skill_by_id(skill_id: int, user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM skills WHERE id = ? AND user_id = ?",
            (skill_id, user_id)
        )
        row = cursor.fetchone()

    return dict(row) if row else None

def get_skills_by_user_id(user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM skills WHERE user_id = ?",
            (user_id,)
        )
        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def create_skill(name: str, user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO skills (user_id, name) VALUES (?, ?)",
            (user_id, name,)
        )
        conn.commit()
        skill_id = cursor.lastrowid

    return {"id": skill_id, "name": name}

def update_skill(skill_id: int, update_data: dict):
    with get_connection() as conn:
        cursor = conn.cursor()
        for key, value in update_data.items():
            query = f"UPDATE skills SET {key} = ? WHERE id = ?"
            cursor.execute(query, (value, skill_id))
        conn.commit()
    
    return True

def delete_skill(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM skills WHERE id = ?",
            (id,)
        )
        conn.commit()
    
    return True