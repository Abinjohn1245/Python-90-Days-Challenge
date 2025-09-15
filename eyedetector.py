# This program uses the OpenCV and Mediapipe libraries to detect eye closure
# from a webcam feed and plays a sound when eyes are closed for too long.

# --- Required Libraries and Installation ---
# Before running this script, you must install the necessary libraries.
# Open your terminal or command prompt and run the following commands:
# pip install opencv-python mediapipe playsound

import cv2
import mediapipe as mp
from playsound import playsound
import math

# --- Configuration ---
# You must place a sound file (e.g., 'alarm.mp3') in the same directory as this script.
# You can easily find free alarm sounds online.
SOUND_FILE = 'alarm.mp3'

# The Eye Aspect Ratio (EAR) threshold. A lower value indicates eyes are more closed.
# You might need to adjust this value depending on your webcam and lighting conditions.
EYE_AR_THRESHOLD = 0.25

# The number of consecutive frames the EAR must be below the threshold before triggering the alarm.
# This prevents false positives from blinking.
EYE_AR_CONSEC_FRAMES = 20

# --- Mediapipe Setup ---
# Initialize Mediapipe's face mesh solution.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# These are the specific indices for the landmarks around the left and right eyes
# for calculating the Eye Aspect Ratio (EAR).
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Counter for consecutive eye closure frames
closed_frames_counter = 0

# --- Functions ---
def euclidean_distance(point1, point2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def get_ear(eye_landmarks):
    """Calculates the Eye Aspect Ratio (EAR) for a given set of eye landmarks."""
    # Vertical distances
    v1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])
    v2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])

    # Horizontal distance
    h = euclidean_distance(eye_landmarks[0], eye_landmarks[3])

    # The EAR formula
    ear = (v1 + v2) / (2.0 * h)
    return ear

def draw_landmarks(image, landmarks, connection_set, color):
    """Draws face landmarks on the image."""
    mp_drawing.draw_landmarks(
        image,
        landmarks,
        connection_set,
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=color, thickness=1)
    )

# --- Main Program Loop ---
def run_detection():
    global closed_frames_counter

    # Initialize webcam capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a more intuitive view
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to find face landmarks
        results = face_mesh.process(rgb_frame)

        # Draw the face mesh and detect eye closure
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get the landmark points for the eyes
                left_eye_points = [face_landmarks.landmark[i] for i in LEFT_EYE]
                right_eye_points = [face_landmarks.landmark[i] for i in RIGHT_EYE]

                # Calculate the EAR for both eyes
                left_ear = get_ear(left_eye_points)
                right_ear = get_ear(right_eye_points)

                # Average the EAR for both eyes
                avg_ear = (left_ear + right_ear) / 2.0

                # Check if eyes are closed
                if avg_ear < EYE_AR_THRESHOLD:
                    closed_frames_counter += 1
                    cv2.putText(frame, "STATUS: EYES CLOSED!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    if closed_frames_counter >= EYE_AR_CONSEC_FRAMES:
                        cv2.putText(frame, "ALERT! ALERT!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        print("Alert! Eyes closed for too long.")
                        try:
                            # Play the sound in a separate thread to avoid blocking the video feed
                            playsound(SOUND_FILE, block=False)
                        except Exception as e:
                            print(f"Error playing sound: {e}")
                else:
                    closed_frames_counter = 0
                    cv2.putText(frame, "STATUS: EYES OPEN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Draw the mesh on the frame for visualization
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)
                )

        # Display the output frame
        cv2.imshow("Eye Closure Detector", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection()
