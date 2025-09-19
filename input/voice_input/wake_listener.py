import pvporcupine
import sounddevice as sd
import queue
import struct
import threading
# import stream_transcriber

# wake word is created to respond to jarvis
def wake_up_detection(stop_event):
    # Will activate when it detects the word Jarvis
    porcupine = pvporcupine.create(keywords=["jarvis"], access_key="3KesXGRlyX//DpicuvntBNfGUotCX4emjJXM9KKaVHbt9sIeUGXr8A==")

    # starts capturing audio from the microphone
    with sd.RawInputStream(
        samplerate=16000,       # Sample rate in Hz
        blocksize=512,          # How many frames per audio block
        dtype='int16',          # Data format (matches wake word/STT expectations)
        channels=1,             # Mono audio
        #callback=audio_callback # Function to call each time new audio is available
    ) as stream:
        
        print("Listening")
        
        while not stop_event.is_set():
            # gets the raw audio buffer
            audio_data,_ = stream.read(porcupine.frame_length)
            # converts raw audio into ints(to let porcupine to process it)
            pcm = struct.unpack_from("h" * porcupine.frame_length, audio_data)
            # wake word detection
            detected_word = porcupine.process(pcm)
            
            if detected_word >= 0:
                # Testing
                print("Word detected")
                break
    # housekeeping
    porcupine.delete()