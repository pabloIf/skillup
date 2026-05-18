from database import get_connection

class SkillRepository:
    def __init__(self, cursor):
        self.cursor = cursor

    def update(self, skill_id: int, update_data: dict):
        self.cursor.execute(
            """
            UPDATE skills
            SET current_streak = ?,
                max_streak = ?,
                last_log_date = ?,
                xp = ?
            WHERE id = ?
            """,
            (
                update_data["current_streak"],
                update_data["max_streak"],
                update_data["last_log_date"],
                update_data["xp"],
                skill_id
            )
        )
    
    def get_by_id(self, skill_id: int, user_id: int):
        self.cursor.execute(
            "SELECT * FROM skills WHERE id = ? AND user_id = ?",
            (skill_id, user_id)
        )
        row = self.cursor.fetchone()

        return dict(row) if row else None


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
    if not update_data:
        return False
    
    with get_connection() as conn:
        cursor = conn.cursor()

        fields = ", ".join(f"{key} = ?" for key in update_data)

        values = list(update_data.values())
        values.append(skill_id)

        query = f"UPDATE skills SET {fields} WHERE id = ?"

        cursor.execute(query, (values))
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