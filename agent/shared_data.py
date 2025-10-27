import json,os

# Used to link the macro_path variable to the macros json file
base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")
global_macro_path = os.path.join(base_dir, "../config/global_macros.json")

# Saves the entire json file into the macros variable
with open(os.path.abspath(macro_path)) as f:
    macros = json.load(f)
    # DEBUG
    # print(macros)

with open(os.path.abspath(global_macro_path)) as f:
    global_macros = json.load(f)

combined = {**macros, **global_macros}