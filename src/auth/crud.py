from database import get_connection

def create_user(username: str, hashed_password: str, user_email: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, user_email)
        )
        conn.commit()
        user_id = cursor.lastrowid

    return {"user_id": user_id, "username": username, "user_email": user_email}

def delete_user(user_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        conn.commit()
    return True

def get_all_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users"
        )
        rows= cursor.fetchall()
    
    return [dict(row) for row in rows]

def get_user_by_username(username: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

    return dict(row) if row else None

def get_user_by_email(user_email: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (user_email,)
        )
        row = cursor.fetchone()
    
    return dict(row) if row else None

def get_user_by_id(user_id: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()

    return dict(row) if row else None

def deactivate_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET is_active = 0 WHERE id = ?",
            (user_id,)
        )
        conn.commit()

    return {"detail": "user deactivated"} 

def reactivate_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET is_active = 1 WHERE id = ?",
            (user_id,)
        )
        conn.commit()

    return {"detail": "user activated"}

def is_active(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_active FROM users WHERE id = ?", 
            (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        
    return bool(row["is_active"])
