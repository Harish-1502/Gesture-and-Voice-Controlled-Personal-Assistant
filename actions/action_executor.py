from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui
import webbrowser
import json

# ------------------------------------------------------
# All these functions are represent each action


def mute():
    # print("Mute the system")
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1,None)
    
def close_tab():
    # print("close tab")
    pyautogui.hotkey('ctrl', 'w')

def open_brave():
    webbrowser.open("https://www.brave.com")
    
def download():
    url = pyperclip.paste()
    if not url.startswith("http"):
        return print("Not a valid URL")
    
    filename = url.split("/")[-1]
    print("Filename is ",filename)
    
    try:
        response.get(url)
        with open(filename, wb) as f:
            f.write(response.content)
        return print("Download was a success")
    except Exception as e:
        return print("Error: ",e)

def print_doc():
    pyautogui.hotkey('ctrl', 'p')

def parry():
    pyautogui.click()

def open_menu():
    pyautogui.hotKey('Esc')
    
def next_tab():
    pyautogui.hotkey('ctrl', 'tab')
    
def previous_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def volume_up():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolume = volume.GetMasterVolumeLevelScalar()
    newVolume = min(currentVolume+0.05,1.0)
    volume.SetMasterVolumeLevelScalar(newVolume, None)
    
    
# ---------------------------------------------------------------------------------------------------    

# Dispatcher holds a copy all the commands to do their respective action
dispatcher = {}

with open("config/macros.json") as f:
    command_map = json.load(f)
for group in command_map.values(): #For each mode 
    if isinstance(group, dict): #If each mode has it's own dict
        for command,action in group.items():
            action_detail = action.get("action")
            global_function = globals().get(action_detail.replace(" ","_"))
            if global_function:
                dispatcher[command] = global_function

def execute_action(action):
    print(dispatcher)
    # Finds the command in dispatcher array and executed the action
    if action in dispatcher:
        print(action)
        return dispatcher[action]()
    else:
        return print("action not found")