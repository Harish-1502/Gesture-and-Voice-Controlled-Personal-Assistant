from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui
import webbrowser

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
    
def prev_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def volume_up():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    currentVolume = volume.GetMasterVolumeLevelScalar()
    newVolume = min(currentVolume+0.05,1.0)
    volume.SetMasterVolumeLevelScalar(newVolume, None)
    
    
dispatcher = {
    "mute": mute,
    "close tab": close_tab,
    "open brave": open_brave,
    "start downloading": download,
    "print": print_doc,
    "parry": parry,
    "open menu": open_menu,
    "next tab" : next_tab,
    "prev tab" :  prev_tab,
    "volume up" : volume_up
}

def execute_action(action):
    
    if action in dispatcher:
        print(action)
        return dispatcher[action]()
    else:
        return print("action not found")