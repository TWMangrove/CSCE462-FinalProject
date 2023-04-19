import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def get_frame():
    cap = cv2.VideoCapture(2)
    ret, frame = cap.read()
    cap.release()
    return frame

def detect_hand_from_image():
    # Initialize the Mediapipe hand detection and landmark detection models
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.55)
    hand_center_x = None
    hand_center_y = None
    zone_num = None
    
    frame = get_frame()

    # Flip the image horizontally
    frame = cv2.flip(frame, 1)

    # Partition the image into 10 vertical zones
    num_zones = 3
    zone_width = frame.shape[1] // num_zones
    for i in range(num_zones):
        x = i * zone_width
        cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 0, 255), 2)

    # Detect the hand in the image
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        # Get the coordinates of all the landmark points of the hand
        hand_landmarks = results.multi_hand_landmarks[0]
        landmark_coords = np.zeros((21, 2), dtype=np.int32)
        for i, landmark in enumerate(hand_landmarks.landmark):
            landmark_coords[i] = (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))

        # Calculate the center point of the hand
        hand_center_x, hand_center_y = np.mean(landmark_coords, axis=0).astype(np.int32)

        # Determine which zone the hand is in based on its x-coordinate
        zone_num = int(hand_center_x // zone_width)

        # Draw a circle at the center of the hand
        cv2.circle(frame, (hand_center_x, hand_center_y), 10, (0, 255, 0), -1)

        # Display the location of the hand and the zone number
        cv2.putText(frame, f"Hand location: ({hand_center_x}, {hand_center_y})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Zone: {zone_num}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the flipped image
    #cv2.imshow('Hand Detection', frame)

    # Wait for 1 millisecond and automatically close the window
    cv2.waitKey(1)

    # Destroy the window
    cv2.destroyAllWindows()

    return zone_num

def detect_gesture_from_image():
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    images = get_frame()
    results = None
    # STEP 3: Load the input image.
    # Load the input image from a numpy array.
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=images)

   
    # STEP 4: Recognize gestures in the input image.
    recognition_result = recognizer.recognize(image)
   
    # STEP 5: Process the result. In this case, visualize it.
    top_gesture = recognition_result.gestures
    hand_landmarks = recognition_result.hand_landmarks
    results = (top_gesture, hand_landmarks)
    
    cv2.imshow('Hand Detection', images)
    # Wait for 1 millisecond and automatically close the window
    cv2.waitKey(1000)
    print(recognition_result)
    # Destroy the window
    cv2.destroyAllWindows()
    
