import sqlite3

DATABASE = "db/project.db"
GAME_LENGTH = 12
WIN_CONDITION = 10000000

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
    game = conn.execute("SELECT * FROM games WHERE user_id = ? AND status = 'ACTIVE'", (user_id,)).fetchone()
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

def generate_new_game(user_id, last_game=None):
    """Set up the basic settings for new game and create a row in tables"""
    conn = get_db_connection()
    if last_game is not None:
        conn.execute("UPDATE users SET last_game = ? WHERE id = ?", (last_game, user_id))
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
        log_action(game["id"], "PRODUCE", genre, 1, cost)
        return True
    else:
        conn.close()
        return False
    
def cancel(genre, user_id):
    conn = get_db_connection()
    game = conn.execute("SELECT id, cash, base_cancel_penalty FROM games WHERE user_id = ? AND status = 'ACTIVE'", (user_id,)).fetchone()
    if conn.execute("SELECT episodes_produced FROM portfolios WHERE game_id = ? AND genre = ?", (game["id"], genre)).fetchone()["episodes_produced"] > 0:
        cash_return = game["base_cancel_penalty"] / 100 * conn.execute("SELECT base_cost FROM genres WHERE name = ?", (genre,)).fetchone()["base_cost"]
        conn.execute("UPDATE portfolios SET episodes_produced = episodes_produced - 1 WHERE game_id = ? and genre = ?", (game["id"], genre))
        conn.execute("UPDATE games SET cash = cash + ? WHERE id = ?", (cash_return, game["id"]))
        conn.commit()
        conn.close()
        log_action(game["id"], "CANCEL", genre, 1, cash_return)
        return True
    else:
        conn.close()
        return False
    
def log_action(game_id, action, genre, episodes, cost):
    conn = get_db_connection()
    conn.execute("INSERT INTO history (game_id, action, genre, episodes, cost) VALUES (?, ?, ?, ?, ?)", (game_id, action, genre, episodes, cost))
    conn.commit()
    conn.close()

def get_random_event():
    conn = get_db_connection()
    event = conn.execute("SELECT * FROM random_events ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    return event

def log_month(game_id, event_title, subscribers, cash, month):
    conn = get_db_connection()
    conn.execute("INSERT INTO month_history (game_id, month, cash, subscribers, event) VALUES (?, ?, ?, ?, ?)", (game_id, month, cash, subscribers, event_title))
    if month == GAME_LENGTH:
        game = conn.execute("SELECT user_id, subscribers FROM games WHERE id = ?", (game_id,)).fetchone()
        if ( game["subscribers"] + subscribers ) >= WIN_CONDITION:
            status = 'WON'
        else:
            status = 'LOST'
        conn.execute("UPDATE games SET subscribers = subscribers + ?, cash = cash + ?, status = ? WHERE id = ?", (subscribers, cash, status, game_id))
        conn.commit()
        conn.close()
        generate_new_game(game["user_id"], game_id)
    else:
        conn.execute("UPDATE games SET subscribers = subscribers + ?, cash = cash + ?, current_month = current_month + 1 WHERE id = ?", (subscribers, cash, game_id))
        conn.commit()
        conn.close()

def get_last_month(game_id, month):
    conn = get_db_connection()
    last_month = conn.execute("SELECT * FROM month_history WHERE game_id = ? AND month = ? - 1", (game_id, month)).fetchone()
    conn.close()
    return last_month

def get_last_game(user_id):
    conn = get_db_connection()
    last_game_id = conn.execute("SELECT last_game FROM users WHERE id = ?", (user_id,)).fetchone()["last_game"]
    last_game = conn.execute("SELECT * FROM games WHERE id = ?", (last_game_id,)).fetchone()
    conn.close()
    return last_game