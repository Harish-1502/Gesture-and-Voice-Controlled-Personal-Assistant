import subprocess,sys,os

# NOTE: Do ctrl+shift+p => python interpreter => 3.10.. version
# Also run the code in the .310venv activated

# Creates variable to link files together
base_dir = os.path.dirname(__file__)
voice_script = os.path.join(base_dir,"voice_runner.py")
gesture_script = os.path.join(base_dir,"gesture_runner.py")

# Creates subprocess variable
voice_subProcess = subprocess.Popen([sys.executable,voice_script])
gesture_subProcess = subprocess.Popen([sys.executable,gesture_script])

# Runs both the voice and the gesture scripts
try:
    voice_subProcess.wait()
    gesture_subProcess.wait()
except KeyboardInterrupt:
    print("Terminating")
    voice_subProcess.terminate()
    gesture_subProcess.terminate()