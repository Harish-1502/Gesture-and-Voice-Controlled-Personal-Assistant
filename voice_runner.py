from input.voice_input.wake_listener import wake_up_detection
from input.voice_input.stream_transcriber import record_audio
from agent.intent_router import rule_based_intent
from actions.action_executor import execute_action
import threading
import sys
import comtypes
import keyboard

# Used to kill the voice_thread loop when it's time to end
stop_event = threading.Event()

def voice_thread():
    comtypes.CoInitialize()
    print("Voice is Called...")

    while not stop_event.is_set():
        # Used to active the voice detection
        wake_up_detection(stop_event)
        if stop_event.is_set():
            break
        # Transcribes the recorded audio for recording commands
        transcribed_text = record_audio()
        print("Transcription: ",transcribed_text)
        # Checks the transcribed audio with the json file to get the proper
        # command in its current mode
        macro = rule_based_intent(transcribed_text)
        print("Macro: ", macro)
        
        if macro:
            # print(macro)
            # Preforms action linked to the command
            execute_action(macro["action"])
        else:
            print("No matching macro found.")
        
def killMainThread():
    keyboard.wait('q')
    stop_event.set()
    print("Killing main thread")

print("Assistant is running...")
# voice_thread()

t1 = threading.Thread(target = voice_thread)
t2 = threading.Thread(target = killMainThread)
t1.start()
t2.start()

try:
    t1.join()
    t2.join()
except KeyboardInterrupt:
    print("Exiting gesture control")
    sys.exit()