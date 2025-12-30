# Gesture and Voice Controlled Personal Assistant

This is a personal assistant controlled using voice and gestures. The personal assistant is able to perform desktop automation tasks based on what voice controls or gesture actions it detects.

- Demo coming soon — currently polishing gesture and voice recognition accuracy.

# Why This Was Made

The goal of this project was to be a small, multi-functional assistant that uses both voice and gestures to do automation tasks instead of relying on one input method.

# Tech Stack:

- Language: Python 
- Gesture Recognition: MediaPipe (hand tracking), OpenCV (camera capture)
- Voice Commands: Porcupine (wake word), Vosk (speech-to-text)

# How It Was Made

- The system works by running both voice recognition and gesture recognition at the same time.
- The voice and gesture recognition processes detect user input, check a JSON file to determine which function to call, and then execute the corresponding function.

# Architecture Overview:

**Input Layer**
  - Voice Commands
      System listens for wake word and converts spoken commands into text.
  - Gesture Recognition
      System recognizes specific gestures using a webcam.

**Processing Layer**
- Both voice and gesture commands are translated to standard actions.

**Command Layer**
- Maps standardized actions to automation functions.

**Execution Layer**
- The automation function is executed and after execution the system waits for the next command.

# Design Decisions

- Cloud-based APIs were avoided to allow the system to work offline.
- Lightweight libraries were used to prioritize speed while maintaining acceptable tolerance levels.
- Voice and gesture commands are in separate threads to prevent modifications in one to block or affect the other. 

# Limitations

- Lighting affects accuracy of gesture recognition.
- Voice recognition struggles with background noise and low speaking volume.
- New commands can only be added by adding them directly into the code.
- Limited gesture and voice vocabulary and accuracy.

# Future Improvements

- Create a GUI to allow users to modify voice commands and gesture commands.
- Increase the number of automation functions and create a caching system to decrease processing overhead.
