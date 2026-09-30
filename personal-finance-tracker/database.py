import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "finance.db")


def get_connection():
    """Return a connection to the SQLite database (creates the data folder if needed)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Income / expense transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK (type IN ('Income', 'Expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount > 0),
            date TEXT DEFAULT (date('now', 'localtime')),
            description TEXT DEFAULT ''
        )
    ''')

    # Migration: older databases have no description column
    columns = [row[1] for row in cursor.execute("PRAGMA table_info(transactions)")]
    if "description" not in columns:
        cursor.execute("ALTER TABLE transactions ADD COLUMN description TEXT DEFAULT ''")

    # Single-row savings goal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS savings_goal (
            id INTEGER PRIMARY KEY,
            goal_amount REAL NOT NULL CHECK (goal_amount > 0)
        )
    ''')

    conn.commit()
    conn.close()