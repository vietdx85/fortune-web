import sqlite3
from datetime import datetime

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Bảng users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Bảng lịch sử xem bói
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            birthdate TEXT,
            zodiac TEXT,
            prediction TEXT,
            tarot TEXT,
            lucky_number INTEGER,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_record(record, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (user_id, name, birthdate, zodiac, prediction, tarot, lucky_number, type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, record['name'], record['birthdate'], record['zodiac'],
          record['prediction'], ",".join(record['tarot']), record['lucky_number'], record['type']))
    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM history WHERE user_id=? ORDER BY created_at DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def search_records(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM history WHERE name LIKE ? ORDER BY created_at DESC', ('%'+name+'%',))
    rows = c.fetchall()
    conn.close()
    return rows
