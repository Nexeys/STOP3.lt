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

def get_portfolio_data(game_id):
    conn = get_db_connection()
    portfolios = conn.execute("SELECT p.genre, p.episodes_produced, g.base_cost, g.base_subscriber_yield FROM portfolios p JOIN genres g ON p.genre = g.name WHERE p.game_id = ?", (game_id,)).fetchall()
    conn.close()
    return portfolios

def produce(genre, user_id):
    conn = get_db_connection()
    game = conn.execute("SELECT id, cash FROM games WHERE user_id = ? AND status = 'ACTIVE'", (user_id,)).fetchone()
    if game["cash"] >= (cost := conn.execute("SELECT base_cost FROM genres WHERE name = ?", (genre,)).fetchone()["base_cost"]):
        conn.execute("UPDATE portfolios SET episodes_produced = episodes_produced + 1 WHERE game_id = ? and genre = ?", (game["id"], genre))
        conn.execute("UPDATE games SET cash = cash - ? WHERE id = ?", (cost, game["id"]))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
    
def cancel(genre, user_id, penalty):
    conn = get_db_connection()
    game = conn.execute("SELECT id, cash FROM games WHERE user_id = ? AND status = 'ACTIVE'", (user_id,)).fetchone()
    if conn.execute("SELECT episodes_produced FROM portfolios WHERE game_id = ? AND genre = ?", (game["id"], genre)).fetchone()["episodes_produced"] > 0:
        cash_return = penalty * conn.execute("SELECT base_cost FROM genres WHERE name = ?", (genre,)).fetchone()["base_cost"]
        conn.execute("UPDATE portfolios SET episodes_produced = episodes_produced - 1 WHERE game_id = ? and genre = ?", (game["id"], genre))
        conn.execute("UPDATE games SET cash = cash + ? WHERE id = ?", (cash_return, game["id"]))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False