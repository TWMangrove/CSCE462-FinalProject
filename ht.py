import cv2
import mediapipe as mp

def get_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

def detect_hand_from_image():
    # Initialize the Mediapipe hand detection and landmark detection models
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
    wrist_x = None
    wrist_y = None
    
    frame = get_frame()

    # Flip the image horizontally
    frame = cv2.flip(frame, 1)

    # Partition the image into 10 vertical zones
    num_zones = 10
    zone_width = frame.shape[1] // num_zones
    for i in range(num_zones):
        x = i * zone_width
        cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 0, 255), 2)

    # Detect the hand in the image
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        # Get the coordinates of the wrist landmark
        hand_landmarks = results.multi_hand_landmarks[0]
        wrist_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        wrist_x = int(wrist_landmark.x * frame.shape[1])
        wrist_y = int(wrist_landmark.y * frame.shape[0])

        # Draw a circle at the wrist landmark
        cv2.circle(frame, (wrist_x, wrist_y), 10, (0, 255, 0), -1)

        # Display the location of the hand
        cv2.putText(frame, f"Hand location: ({wrist_x}, {wrist_y})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #Display the flipped image
    cv2.imshow('Hand Detection', frame)

    # Wait for 1 millisecond and automatically close the window
    cv2.waitKey(100)

    #Destroy the window
    cv2.destroyAllWindows()

    return wrist_x, wrist_y
