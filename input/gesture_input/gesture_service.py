import cv2
import mediapipe as mp
import time
import threading
import os

# Creating variables to be used in functions
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
prev_position=[]
lock = threading.Lock()

# For webcam input:
cap = cv2.VideoCapture(0)

# Opens the gesture.txt file to get the action written into the file by the gesture_service function
def check_gesture():
    if os.path.exists("gesture.txt"):
        with lock:
            with open("gesture.txt", "r") as f:
                gesture = f.read().strip()
            os.remove("gesture.txt") 
            return gesture
    return None

# Runs the camera recognition function. Writes down the action caught by the camera into a text file 
def gesture_service(stop_event): 

# Setup for variance (This is the default)  
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:

    # Will the camera is on
    while cap.isOpened():
      
      # Used for checking if it works
      success, image = cap.read()
      
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
          
          # Saves the different the finger markers (The API works by identifying different 
          # of the hand to link together for it to recognize a human hand)
          index_tip = hand_landmarks.landmark[8]        
          x = index_tip.x
          
          thumb_tip = hand_landmarks.landmark[4]
          thumb_ip = hand_landmarks.landmark[3]

          index_pip = hand_landmarks.landmark[6]

          middle_tip = hand_landmarks.landmark[12]
          middle_pip = hand_landmarks.landmark[10]

          ring_tip = hand_landmarks.landmark[16]
          ring_pip = hand_landmarks.landmark[14]

          pinky_tip = hand_landmarks.landmark[20]
          pinky_pip = hand_landmarks.landmark[18]

          # All fingers folded except thumb
          is_thumb_up = thumb_tip.y < thumb_ip.y
          is_index_folded = index_tip.x < index_pip.x
          is_middle_folded = middle_tip.x < middle_pip.x
          is_ring_folded = ring_tip.x < ring_pip.x
          is_pinky_folded = pinky_tip.x < pinky_pip.x
          
          # Once the thumbs up is detected, volume goes up
          if is_thumb_up and is_index_folded and is_middle_folded and is_ring_folded and is_pinky_folded:
            print("Thumb up detected")
            with lock:
              with open("gesture.txt","w") as f:
                f.write("volume up")
              time.sleep(1)
          
          # Saves the position of the index finger in an array
          # Needed for swiping motion
          prev_position.append(x)

          # When the array is full, the oldest value is discarded
          if len(prev_position) > 5:
            prev_position.pop(0)

          # When enough data is collected (array is filled),
          # then it calculated the oldest position with the newest position 
          if len(prev_position) == 5:
            motion = prev_position[-1] - prev_position[0] 
             
            if(motion > 0.4):
              print("Swipe right detected")
              with lock:
                with open("gesture.txt","w") as f:
                  f.write("next tab")
                time.sleep(1)
            elif(motion < -0.4):
              print("Swipe left detected")
              with lock:
                with open("gesture.txt","w") as f:
                  f.write("prev tab")
                time.sleep(1)
      
      height, width, _ = image.shape
      # Draw vertical grid lines (every 20%)
      for i in range(1, 5):
        x = int(width * i * 0.2)
        cv2.line(image, (x, 0), (x, height), (200, 200, 200), 1)

      # Draw horizontal grid lines (every 20%)
      for i in range(1, 5):
        y = int(height * i * 0.2)
        cv2.line(image, (0, y), (width, y), (200, 200, 200), 1)
                      
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == ord('q'):
        stop_event.set()
        with open("gesture.txt", "w") as f:
          f.write("")
        break

  # Clean up when closing  
  cap.release()
  cv2.destroyAllWindows()

# t=threading.Thread(target=gesture_service)
# t.start()