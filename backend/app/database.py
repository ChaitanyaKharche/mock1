import sqlite3
from .models import ConversationState

DB_PATH = "chat_sessions.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Using TEXT for state for flexibility, could also be an ENUM/INTEGER
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            session_id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            name TEXT,
            email TEXT,
            phone TEXT,
            move_in_date TEXT,
            beds INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_session(session_id: str) -> ConversationState | None:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM conversations WHERE session_id = ?", (session_id,)).fetchone()
    conn.close()
    if row:
        return ConversationState(**dict(row))
    return None

def save_session(session: ConversationState):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Using INSERT OR REPLACE for simplicity in this context
    cursor.execute('''
        INSERT OR REPLACE INTO conversations (session_id, state, name, email, phone, move_in_date, beds)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        session.session_id, session.state, session.name, session.email,
        session.phone, session.move_in_date, session.beds
    ))
    conn.commit()
    conn.close()