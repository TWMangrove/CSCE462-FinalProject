from ht import detect_gesture_from_image
from ht import detect_hand_from_image

#detect_gesture_from_image()


while True:
    zone = detect_hand_from_image()
    if(zone is None):
        print("NO HAND DETECTED")
    else: 
        print(f"Hand location: ({zone})")
