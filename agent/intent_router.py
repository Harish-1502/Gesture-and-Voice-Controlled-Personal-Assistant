# import requests

# prompt = f"""
# You are a helpful assistant that turns voice commands into system actions.

# Examples:
# User: "open browser"
# Output: {{ "action": "open_app", "target": "browser" }}

# User: "mute volume"
# Output: {{ "action": "volume_control", "value": "mute" }}

# User: "close the game"
# Output: {{ "action": "close_app", "target": "game" }}

# Now interpret this:
# User: user_command
# Output:
# """

# def ask_llm(prompt_text):
#     try:
#         response = requests.post("http://localhost:11434/api/generate", json={
#             "model": "gemma:2b",
#             "prompt": prompt_text,
#             "stream": False
#         }, timeout=60)

#         # print("Raw response:", response.status_code)
#         # print(response.json())  # Debug print

#         return response.json()["response"]

#     except Exception as e:
#         return f"Exception: {str(e)}"
    
    
# if __name__ == "__main__":
#     prompt = "Parry."
#     reply = ask_llm(prompt)
#     print("LLM says:", reply)

import json
import os
import sqlite3
from actions.action_executor import get_mode

# Used to link the macro_path variable to the macros json file
base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")
global_macro_path = os.path.join(base_dir, "../config/global_macros.json")
macro_manager_path = os.path.join(base_dir,"../config/macro_manager.db")

mode_list = []
with open(os.path.abspath(macro_path)) as f:
    command_map = json.load(f)
for group in command_map.keys():
    mode_list.append(group)

current_mode = ""

# def set_mode(new_mode):
#     if new_mode in mode_list:
#         with sqlite3.connect(macro_manager_path) as conn:
#             conn.execute("""
#                 INSERT OR REPLACE INTO state (key,value) VALUES (?,?) """, ("mode",new_mode))
#             conn.commit() 
#         return True
#     else:
#         return False
    

# def get_mode():
#     with sqlite3.connect(macro_manager_path) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT value FROM state WHERE key = 'mode'")
#         row = cursor.fetchone()
#         return row[0] if row else "daily"
    
# def db_init():
#     with sqlite3.connect(macro_manager_path) as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS state (
#                 key TEXT PRIMARY KEY,
#                 value TEXT
#             )
#         """)
#         conn.commit()

# Saves the entire json file into the macros variable
with open(os.path.abspath(macro_path)) as f:
    macros = json.load(f)
    # DEBUG
    # print(macros)

with open(os.path.abspath(global_macro_path)) as f:
    global_macros = json.load(f)

def rule_based_intent(text):
    # Turn the command into lower case
    text = text.lower()
    if text in ["change to"]:
        mode_name = text.split(phrase, 1)[1].strip()
        if mode_name.endswith(" mode"):
            mode_name = mode_name[:-5].strip()
        return mode_name

    current_mode = get_mode()
    # Get action linked to the specified command
    action = macros.get(current_mode,{}).get(text)
    # DEBUG
    # print(action)
    if action:
        # DEBUG
        # print(action)
        # If action was found, then return it
        return action
    
    # TODO: Create logic when the action was not found
         
# if __name__ == "__main__":
#     result = rule_based_intent("mute")
#     # print("Result:", result)