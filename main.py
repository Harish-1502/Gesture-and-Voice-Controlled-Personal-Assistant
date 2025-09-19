import subprocess

# Creates variable to link files together
voice_python_exe = r"C:\Users\thari\Personal Projects\Universal Macro Controller\.venv\Scripts\python.exe"
gesture_python_exe = r"C:\Users\thari\Personal Projects\Universal Macro Controller\.venv310\Scripts\python.exe"
voice_script = r"C:\Users\thari\Personal Projects\Universal Macro Controller/voice_runner.py"
gesture_script = r"C:\Users\thari\Personal Projects\Universal Macro Controller/gesture_runner.py"

# Creates subprocess variable
voice_subProcess = subprocess.Popen([voice_python_exe,voice_script])
gesture_subProcess = subprocess.Popen([gesture_python_exe,gesture_script])

# Runs both the voice and the gesture scripts
try:
    voice_subProcess.wait()
    gesture_subProcess.wait()
except KeyboardInterrupt:
    print("Terminating")
    voice_subProcess.terminate()
    gesture_subProcess.terminate()