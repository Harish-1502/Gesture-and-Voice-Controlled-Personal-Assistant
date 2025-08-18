from input.voice_input.wake_listener import wake_up_detection
from input.voice_input.stream_transcriber import record_audio
from agent.intent_router import rule_based_intent
from actions.action_executor import execute_action
import os
import threading
import time

def voice_thread():
    print("Voice is Called...")
    wake_up_detection()
    transcribed_text = record_audio()
    print("Transcription: ",transcribed_text)
    macro = rule_based_intent(transcribed_text)
    print(macro)
    if macro:
        print(macro)
        execute_action(macro["action"])
    else:
        print("No matching macro found.")
        
def check_gesture():
    if os.path.exists("gesture.txt"):
        with open("gesture.txt", "r") as f:
            gesture = f.read().strip()
        os.remove("gesture.txt") 
        return gesture
    return None

def gesture_thread():
    print("Gesture is Called...")
    while True:
        gestured_action = check_gesture()
        print("Gestured Action: ", gestured_action)
        if not gestured_action:
            continue
        gestured_macro = rule_based_intent(gestured_action)
        if gestured_macro:
            print(gestured_macro)
            execute_action(gestured_macro["action"])
        else:
            print("No matching macro found.")

print("Assistant is running...")
# gesture_thread()
# voice_thread()

t1 = threading.Thread(target = gesture_thread, daemon=True)
t1.start()

while True:
    t2 = threading.Thread(target = voice_thread)
    
    
    t2.start()
    
    # t1.join()
    t2.join()
    
    time.sleep(3)
# break

