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

base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")

mode = "daily"
with open(os.path.abspath(macro_path)) as f:
    macros = json.load(f)
    # print(macros)

def rule_based_intent(text):
    text = text.lower()
    action = macros.get(mode,{}).get(text)
    # print(action)
    if action:
        # print(action)
        return action

# Used to link the macro_path variable to the macros json file
base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")

# Hard-coded the mode
#TODO: change this hard-coded mode into a state and have it change
mode = "daily"

# Saves the entire json sile into the macros variable
with open(os.path.abspath(macro_path)) as f:
    macros = json.load(f)
    # DEBUG
    # print(macros)

def rule_based_intent(text):
    # Turn the command into lower case
    text = text.lower()
    # Get action linked to the specified command
    action = macros.get(mode,{}).get(text)
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