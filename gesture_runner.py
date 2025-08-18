from input.gesture_service import gesture_service, check_gesture
import time
from agent.intent_router import rule_based_intent
from actions.action_executor import execute_action
import os
import threading
import sys
import time


stop_event = threading.Event()

def gesture_controller():
    print("Gesture is Called...")
    while not stop_event.is_set():
        gestured_action = check_gesture()
        # print("Gestured Action: ", gestured_action)
        if not gestured_action:
            continue
        gestured_macro = rule_based_intent(gestured_action)
        if gestured_macro:
            # print(gestured_macro)
            execute_action(gestured_macro["action"])
        # else:
            # print("No matching macro found.")
        time.sleep(0.5)
            
gesture_service_thread = threading.Thread(target = gesture_service, args=(stop_event,), daemon = True)
gesture_control_thread = threading.Thread(target = gesture_controller, daemon = True)

gesture_service_thread.start()
gesture_control_thread.start()

try:
    gesture_service_thread.join()
    gesture_control_thread.join()
except KeyboardInterrupt:
    print("Exiting gesture control")
    sys.exit()