from TTS.api import TTS
import tempfile, os
import simpleaudio as sa

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_path = tmp.name

    tts.tts_to_file(text=text, file_path=temp_path)
    wave_obj = sa.WaveObject.from_wave_file(temp_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove(temp_path)

# if __name__ == "__main__":
#     speak("Hello, world! I am your offline assistant.")