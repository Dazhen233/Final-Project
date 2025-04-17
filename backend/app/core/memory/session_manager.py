import sqlite3
from datetime import datetime

DATABASE = "storybot.db"

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            character_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS story_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            current_state TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            audio_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, character_name=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, character_name) VALUES (?, ?)", (user_id, character_name))
    conn.commit()
    conn.close()

def update_user_character(user_id, character_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET character_name = ? WHERE user_id = ?", (character_name, user_id))
    conn.commit()
    conn.close()

def get_user_character(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT character_name FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_conversation_memory(user_id, message, response):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversation_memory (user_id, message, response) VALUES (?, ?, ?)", (user_id, message, response))
    conn.commit()
    conn.close()

def get_conversation_memory(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT message, response FROM conversation_memory WHERE user_id = ? ORDER BY created_at", (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def add_story_state(user_id, current_state):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO story_state (user_id, current_state) VALUES (?, ?)", (user_id, current_state))
    conn.commit()
    conn.close()

def get_story_state(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT current_state FROM story_state WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_image(user_id, image_url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (user_id, image_url) VALUES (?, ?)", (user_id, image_url))
    conn.commit()
    conn.close()

def add_audio_response(user_id, audio_url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO audio_responses (user_id, audio_url) VALUES (?, ?)", (user_id, audio_url))
    conn.commit()
    conn.close()

def get_all_conversation_memory():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversation_memory ORDER BY created_at")
    result = cursor.fetchall()
    conn.close()
    return result
