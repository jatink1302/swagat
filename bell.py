import cv2
import mediapipe as mp
import pygame
import time
 
# Initialize mediapipe for person detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
 
# Initialize pygame for playing sound
pygame.mixer.init()
pygame.mixer.music.load(r'/Users/jatinkumar/Desktop/doorbell.mp3')  # Replace with the path to your sound file

 
# Initialize webcam
cap = cv2.VideoCapture(0)
 
# Variable to track whether the sound has been played
sound_played = False
 
def play_sound():
    """Plays a sound when a person is detected"""
    pygame.mixer.music.play()
 
# Start capturing frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
 
    # Convert the frame to RGB (mediapipe works with RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detect the pose/person
    result = pose.process(rgb_frame)
    # Check if any pose landmarks are detected (indicating a person is present)
    if result.pose_landmarks:
        if not sound_played:
            play_sound()
            sound_played = True  # Set flag to indicate sound has been played
 
        # Optional: Draw landmarks on the frame
        mp.solutions.drawing_utils.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )
    else:
        sound_played = False  # Reset flag if no person is detected
    # Show the frame
    cv2.imshow('Webcam', frame)
 
    # Press 'q' to quit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
 
# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
