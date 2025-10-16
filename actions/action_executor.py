import json, os, importlib, inspect

base_dir = os.path.dirname(__file__)
daily = os.path.join(base_dir,"./action_files/daily.py")
wuthering_waves = os.path.join(base_dir,"./action_files/wutering_waves.py")
files = []
mode_list = []
action_file = os.path.join(base_dir, "./action_files")  

# Dispatcher holds a copy all the commands to do their respective action
dispatcher = {}

with open("config/macros.json") as f:
    command_map = json.load(f)
                
for filename in os.listdir(action_file):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        file_path = os.path.join(action_file, filename)
        
        # load the file
        spec = importlib.util.spec_from_file_location(module_name, file_path)

        # Make space in memory for the code from the file
        module = importlib.util.module_from_spec(spec)

        # Fill the space with the code
        spec.loader.exec_module(module)
        
        # getmembers return a dict. the string has the name from the
        # method name and the function with the memory location 
        for name,func in inspect.getmembers(module, inspect.isfunction):

            # Change the underscore to a space
            dispatcher[name.replace("_", " ")] = func
            

# Used Lambda to link specific phrases to the set_mode in dispatcher
for mode_name in command_map.keys():  
    dispatcher[f"change to {mode_name}"] = (lambda m=mode_name: dispatcher["set mode"](m))
    dispatcher[f"change to {mode_name} mode"] = (lambda m=mode_name: dispatcher["set mode"](m))
    mode_list.append(mode_name)

def execute_action(action):
    print(dispatcher)
    print(action)
    # Finds the command in dispatcher array and executed the action
    if action in dispatcher:
        # print(action)
        return dispatcher[action]()
    else:
        return print("action not found")