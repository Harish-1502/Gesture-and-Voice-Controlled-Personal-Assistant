import sounddevice as sd
import numpy as np 
from vosk import Model, KaldiRecognizer
import json
import os
import noisereduce as nr
from scipy.signal import butter, lfilter
import difflib

known_phrases = []
# get all the global commands into the array
with open("config/global_macros.json") as f:
    command_map = json.load(f)
known_phrases.extend(command_map.keys())
print(known_phrases)

with open("config/macros.json") as f:
    command_map = json.load(f)
# Turn the change to phrase into complete sentences by combining the mode from the macros.json file
change_to_phrases = [f"change to {phrase} mode" for phrase in command_map.keys()]
known_phrases.extend(change_to_phrases)
# Put all the command from the macros.json file into the array 
for group in command_map.values(): #For each mode 
    if isinstance(group, dict): #If each mode has it's own dict
        known_phrases.extend(group.keys()) #Returns all the keys
del command_map

base_dir = os.path.dirname(__file__)  # e.g. .../input/voice_input
model_path = os.path.abspath(os.path.join(base_dir, "../../models/vosk-model-small-en-us-0.15"))
model = Model(model_path)
rec = KaldiRecognizer(model, 16000, json.dumps(known_phrases))

def highpass_filter(audio, cutoff = 100, fs = 16000, order = 5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    filtered_audio = lfilter(b,a,audio)
    return filtered_audio

def normalize_audio(audio):
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    else:
        return audio/peak

# Used to record commands and check in the array if they exist
# If the command exists then, it will return the word
def record_audio(duration = 2, fs=16000):
    print("Recording now")
    # Does the recording
    audio = sd.rec(int(duration * fs), samplerate = fs, channels = 1, dtype = 'int16')
    sd.wait()
    
    audio = np.squeeze(audio)  # flatten shape: (n,1) → (n,)
    audio = highpass_filter(audio,cutoff=100,fs=fs)
    audio = nr.reduce_noise(y = audio,sr = fs)
    audio = normalize_audio(audio)
    audio_int16 = (audio * 32767).astype(np.int16)
    # Manipulate the audio to make more comprehensible
    audio_bytes = audio_int16.tobytes()
    # print(f"DEBUG: Transcribed text = '{audio}'")

    # audio_bytes = audio.tobytes()
    rec.AcceptWaveform(audio_bytes)
    result = rec.FinalResult()
    print("Vosk result:", result)

    text = json.loads(result).get("text", "").strip()

    if text:
        # print("📝 Transcript:", text)
        if text in known_phrases:
            print("Exact match found")
            return text
        else:
            best_match = find_match(text,known_phrases)
            if best_match:
                print(f"Using find_match to eliminate fuzzy words: {best_match}")
                return best_match
            else:
                return ""
    else:
        # print("⚠️ Still no recognizable speech.")
        return ""
    
def find_match(text, known_phrases, cutoff=0.75):
    matches = difflib.get_close_matches(text, known_phrases, n=1, cutoff=cutoff)
    return matches[0] if matches else None