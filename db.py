import sqlite3

DATABASE = "db/project.db"

def get_db_connection():
    """Opens a secure, structured connection to the SQLite database."""
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

def get_user_data(user_id):
    """Return username from database, based on cookies"""
    conn = get_db_connection()
    user = conn.execute("SELECT username FROM users WHERE id = ?",(user_id,)).fetchone()
    conn.close()
    return user

def get_game_data(user_id):
    """Return game row from database, based on cookies"""
    conn = get_db_connection()
    game = conn.execute("SELECT id, cash, subscribers, current_month FROM games WHERE user_id = ? AND status = 'ACTIVE'", (user_id,)).fetchone()
    conn.close()
    return game

def check_username(username):
    """Return id based on username"""
    conn = get_db_connection()
    user = conn.execute("SELECT id, hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def register_user(username, hashed_password):
    conn = get_db_connection()
    conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def generate_new_game(user_id):
    """Set up the basic settings for new game and create a row in tables"""
    conn = get_db_connection()
    cursor = conn.execute("INSERT INTO games (user_id) VALUES (?)", (user_id,))
    game_id = cursor.lastrowid
    conn.execute("INSERT INTO portfolios (game_id, genre) SELECT ?, name FROM genres", (game_id,))
    conn.commit()
    conn.close()
