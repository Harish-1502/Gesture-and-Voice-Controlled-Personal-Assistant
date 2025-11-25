import subprocess,sys,os

# NOTE: Do ctrl+shift+p => python interpreter => 3.10.. version
# Also run the code in the .310venv activated
# Do .310venv/Scripts/Activate in terminal first then run python main.py

# Creates variable to link files together
base_dir = os.path.dirname(__file__)
# print("Base_dir", base_dir)
voice_script = os.path.join(base_dir,"voice_runner.py")
gesture_script = os.path.join(base_dir,"gesture_runner.py")
# gui_script = os.path.join(base_dir,"gui/pystray_control.py")

# Creates subprocess variable
voice_subProcess = subprocess.Popen([sys.executable,voice_script])
gesture_subProcess = subprocess.Popen([sys.executable,gesture_script])
gui_process = subprocess.Popen([sys.executable, "-m" ,"Gui.gui_display"])


# Runs both the voice and the gesture scripts
try:
    voice_subProcess.wait()
    gesture_subProcess.wait()
    gui_process.wait()
except KeyboardInterrupt:
    print("Terminating")
    voice_subProcess.terminate()
    gesture_subProcess.terminate()
    gui_process.terminate()