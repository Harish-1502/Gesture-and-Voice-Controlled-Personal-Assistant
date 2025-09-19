from input.gesture_service import gesture_service, check_gesture
import time
from agent.intent_router import rule_based_intent
from actions.action_executor import execute_action
import os
import threading
import sys
import time

# TODO: Use the stop_event to kill the gesture controls
stop_event = threading.Event()

# Main gesture command operation(links all the gesture operations together)
def gesture_controller():
    print("Gesture is Called...")
    # Runs until the stop event is called
    while not stop_event.is_set():

        # Waits for gestured action to be detected in the txt file
        gestured_action = check_gesture()
        # DEBUG
        # print("Gestured Action: ", gestured_action)

        if not gestured_action:
            # skips the function when a gestured action isn't detected
            continue
        # Get the macro linked to the action
        gestured_macro = rule_based_intent(gestured_action)
        if gestured_macro:
            # DEBUG
            # print(gestured_macro)
            # Perform the macro found for the action
            execute_action(gestured_macro["action"])
        # else:
            # print("No matching macro found.")
        # Delay to prevent multiple commands sent right away
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