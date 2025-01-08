import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize MediaPipe Hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

def classify_gesture(landmarks, hand_label):
    def is_finger_extended(tip_id, pip_id, vertical=True):
        if vertical:
            return landmarks[tip_id][1] < landmarks[pip_id][1]
        else:
            # Horizontal check for thumb
            if hand_label == "Right":
                return landmarks[tip_id][0] < landmarks[pip_id][0]
            else:
                return landmarks[tip_id][0] > landmarks[pip_id][0]

    thumb_extended = is_finger_extended(4, 2, vertical=False)
    index_extended = is_finger_extended(8, 6, vertical=True)
    middle_extended = is_finger_extended(12, 10, vertical=True)
    ring_extended = is_finger_extended(16, 14, vertical=True)
    pinky_extended = is_finger_extended(20, 18, vertical=True)

    extended_count = sum([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended])

    # Classification rules:
    if extended_count == 0:
        return "Rock"
    elif extended_count == 5:
        return "Paper"
    elif index_extended and middle_extended and not ring_extended and not pinky_extended and not thumb_extended:
        return "Scissors"
    else:
        return "Unknown"

def determine_winner(left_hand, right_hand):
    if "Unknown" in [left_hand, right_hand]:
        return "Unknown"
    win_map = {
        ("Rock", "Scissors"): "Left win!",
        ("Scissors", "Paper"): "Left win!",
        ("Paper", "Rock"): "Left win!",
        ("Scissors", "Rock"): "Right win!",
        ("Paper", "Scissors"): "Right win!",
        ("Rock", "Paper"): "Right win!",
    }
    if left_hand == right_hand:
        return "Tie"
    return win_map.get((left_hand, right_hand), "Unknown")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    left_gesture = "No Hand"
    right_gesture = "No Hand"
    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            label = handedness.classification[0].label  # "Left" or "Right"

            # Extract landmarks
            landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

            # Classify gesture
            gesture = classify_gesture(landmarks, label)
            if label == "Left":
                left_gesture = gesture
            else:
                right_gesture = gesture

    # Determine winner
    result_text = determine_winner(left_gesture, right_gesture)

    # Display left and right hand gestures
    cv2.putText(frame, f"Left: {left_gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Right: {right_gesture}", (frame.shape[1] - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display winner
    cv2.putText(frame, result_text, (frame.shape[1] // 2 - 100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imshow("Rock-Paper-Scissors Battle", frame)
    if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
