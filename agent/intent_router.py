import json,os,sqlite3
from actions.action_files.database import get_mode
from .phi3_ai import ask_phi3
# from tts import speak
from .embedded_matching import match_command
from .shared_data import combined

# Used to link the macro_path variable to the macros json file
base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")
# global_macro_path = os.path.join(base_dir, "../config/global_macros.json")

# Saves the entire json file into the macros variable
with open(os.path.abspath(macro_path)) as f:
    macros = json.load(f)
    # DEBUG
    # print(macros)

# with open(os.path.abspath(global_macro_path)) as f:
#     global_macros = json.load(f)

# combined = {**macros, **global_macros}

def rule_based_intent(text):
    # Turn the command into lower case
    text = text.lower()

    action, score = match_command(text)
    if action:
        print(f"[Fast match] '{text}' → {action} (score={score:.2f})")
        return action

    action = ask_phi3(text, combined)

    if action in combined:
        return combined[action]
    else:
        manual_intent_mapping(text)

    # TODO: Create logic when the action was not found


def manual_intent_mapping(text):
    if text.startswith("change to"):
        print(text)
        return {"action": text}

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
    else:
        return None



# if __name__ == "__main__":
#     result = rule_based_intent("mute")
#     # print("Result:", result)