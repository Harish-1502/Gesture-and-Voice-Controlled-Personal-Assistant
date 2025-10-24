import sqlite3,os
from actions.action_executor import mode_list 

base_dir = os.path.dirname(__file__)
macro_manager_path = os.path.join(base_dir,"../../config/macro_manager.db")

def set_mode(new_mode):
    if new_mode in mode_list:
        with sqlite3.connect(macro_manager_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO state (key,value) VALUES (?,?) """, ("mode",new_mode))
            conn.commit() 
        return print("Mode change successful")
    else:
        return print("Mode change failed")

def get_mode():
    with sqlite3.connect(macro_manager_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM state WHERE key = 'mode'")
        row = cursor.fetchone()
        return row[0] if row else "daily"
    
def db_init():
    with sqlite3.connect(macro_manager_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()