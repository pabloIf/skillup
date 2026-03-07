from database import get_connection

def create_user(username: str, hashed_password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return {"user_id": user_id, "username": username}

def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None