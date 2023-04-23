import cv2

# Load the hand cascade classifier
hand_cascade = cv2.CascadeClassifier('fist.xml')


def get_frame():
    cap = cv2.VideoCapture(2)
    ret, frame = cap.read()
    cap.release()
    return frame

def detect_hand_from_image():
    zone_num = None
    frame = get_frame()

    # Flip the image horizontally
    frame = cv2.flip(frame, 1)

    # Split the frame into three vertical zones
    height, width, _ = frame.shape
    zone_width = width // 3
    zone1 = (0, 0, zone_width, height)
    zone2 = (zone_width, 0, zone_width, height)
    zone3 = (zone_width*2, 0, zone_width, height)
    
    # Extract the zones from the frame
    zone1_frame = frame[zone1[1]:zone1[1]+zone1[3], zone1[0]:zone1[0]+zone1[2]]
    zone2_frame = frame[zone2[1]:zone2[1]+zone2[3], zone2[0]:zone2[0]+zone2[2]]
    zone3_frame = frame[zone3[1]:zone3[1]+zone3[3], zone3[0]:zone3[0]+zone3[2]]
    
    # Convert the frames to grayscale
    zone1_gray = cv2.cvtColor(zone1_frame, cv2.COLOR_BGR2GRAY)
    zone2_gray = cv2.cvtColor(zone2_frame, cv2.COLOR_BGR2GRAY)
    zone3_gray = cv2.cvtColor(zone3_frame, cv2.COLOR_BGR2GRAY)
    
    # Detect hands in each zone
    zone1_hands = hand_cascade.detectMultiScale(zone1_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    zone2_hands = hand_cascade.detectMultiScale(zone2_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    zone3_hands = hand_cascade.detectMultiScale(zone3_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Label each zone with the number of hands detected
    cv2.putText(zone1_frame, f'Zone 1: {len(zone1_hands)} hand(s)', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(zone2_frame, f'Zone 2: {len(zone2_hands)} hand(s)', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(zone3_frame, f'Zone 3: {len(zone3_hands)} hand(s)', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Combine the frames
    output_frame = cv2.hconcat([zone1_frame, zone2_frame, zone3_frame])
    
    
    
    # Show the output
    #cv2.imshow('Hand Tracking', output_frame)
    
    # Break the loop if 'q' is pressed
    #cv2.waitKey(1000)
        
        
    # Determine the zone with the most hands detected
    if len(zone1_hands) >= len(zone2_hands) and len(zone1_hands) >= len(zone3_hands) and len(zone1_hands) > 0:
        zone_num = 0
    elif len(zone2_hands) >= len(zone1_hands) and len(zone2_hands) >= len(zone3_hands) and len(zone2_hands) > 0:
        zone_num = 1
    elif len(zone3_hands) > 0:
        zone_num = 2
    
    # Destroy the window
    cv2.destroyAllWindows()

    return zone_num
