import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "project.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

with sqlite3.connect(DB_PATH) as conn:
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
        
    conn.executescript(schema_sql)
    print(f"Database project.db initialized successfully at {DB_PATH}!")