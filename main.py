import subprocess

voice_python = r"C:\Users\thari\Personal Projects\Universal Macro Controller\.venv\Scripts\python.exe"
gesture_python = r"C:\Users\thari\Personal Projects\Universal Macro Controller\.venv310\Scripts\python.exe"

voice_script = r"C:\Users\thari\Personal Projects\Universal Macro Controller/voice_runner.py"
gesture_script = r"C:\Users\thari\Personal Projects\Universal Macro Controller/gesture_runner.py"

voice_subProcess = subprocess.Popen([voice_python,voice_script])
gesture_subProcess = subprocess.Popen([gesture_python,gesture_script])

try:
    voice_subProcess.wait()
    gesture_subProcess.wait()
except KeyboardInterrupt:
    print("Terminating")
    voice_subProcess.terminate()
    gesture_subProcess.terminate()