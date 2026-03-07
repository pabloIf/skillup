from database import get_connection

def get_all_skills():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM skills")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_skill_by_id(skill_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills WHERE id = ? AND user_id = ?", (skill_id, user_id))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def get_skills_by_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def create_skill(name: str, user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO skills (user_id, name) VALUES (?, ?)", (user_id, name,))
    conn.commit()
    skill_id = cursor.lastrowid
    conn.close()

    return {"id": skill_id, "user_id": user_id, "name": name}

def delete_skill(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return True