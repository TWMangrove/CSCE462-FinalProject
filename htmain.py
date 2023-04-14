from ht import detect_hand_from_image


while True:
    hand_x, hand_y, zone = detect_hand_from_image()
    if(hand_x is None and hand_y is None and zone is None):
        print("NO HAND DETECTED")
    else: 
        print(f"Hand location: ({hand_x}, {hand_y}, {zone})")
