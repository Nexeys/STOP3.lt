import sqlite3

DATABASE = "db/project.db"

def get_db_connection():
    """Opens a secure, structured connection to the SQLite database."""
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn