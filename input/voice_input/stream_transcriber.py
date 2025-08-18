import sounddevice as sd
import numpy as np 
from vosk import Model, KaldiRecognizer
import json
import os
import noisereduce as nr
from scipy.signal import butter, lfilter

known_phrases = ["mute", "open brave", "close tab", "start download", "print","parry","open menu", "next tab", "prev tab", "volume up"]
base_dir = os.path.dirname(__file__)  # e.g. .../input/voice_input
model_path = os.path.abspath(os.path.join(base_dir, "../../models/vosk-model-small-en-us-0.15"))
model = Model(model_path)
rec = KaldiRecognizer(model, 16000, json.dumps(known_phrases))

# def highpass_filter(audio, cutoff = 100, fs = 16000, order = 5):
#     nyquist = 0.5 * fs
#     normal_cutoff = cutoff / nyquist
#     b, a = butter(order, normal_cutoff, btype='high', analog=False)
#     filtered_audio = lfilter(b,a,audio)
#     return filtered_audio

# def normalize_audio(audio):
#     peak = np.max(np.abs(audio))
#     if peak == 0:
#         return audio
#     else:
#         return audio/peak

def record_audio(duration = 2, fs=16000):
    print("Recording now")
    audio = sd.rec(int(duration * fs), samplerate = fs, channels = 1, dtype = 'int16')
    sd.wait()
    
    audio = np.squeeze(audio)  # flatten shape: (n,1) → (n,)
    
    # audio = highpass_filter(audio,cutoff=100,fs=fs)
    # audio = nr.reduce_noise(y = audio,sr = fs)
    # audio = normalize_audio(audio)
    # audio_int16 = (audio * 32767).astype(np.int16)
    # print(f"DEBUG: Transcribed text = '{audio}'")

    # audio_bytes = audio_int16.tobytes()
    audio_bytes = audio.tobytes()
    rec.AcceptWaveform(audio_bytes)
    result = rec.FinalResult()
    print("Vosk result:", result)
 
    text = json.loads(result).get("text", "").strip()
    
    
    if text:
        # print("📝 Transcript:", text)
        return text
    else:
        # print("⚠️ Still no recognizable speech.")
        return ""