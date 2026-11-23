
import cv2

from detection.hand_detector import HandDetector
from detection.gesture_recognition import GestureRecognizer


detector = HandDetector()
recognizer = GestureRecognizer(pinch_threshold=40)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    annotated_frame, hands = detector.detect(frame)

    for hand in hands:
        result = recognizer.recognize(hand)

        gesture = result["gesture"]
        distance = result["pinch_distance"]

        wrist_x = int(result["wrist_position"]["x"])
        wrist_y = int(result["wrist_position"]["y"])

        color = (0, 255, 0) if gesture == "pinch" else (0, 0, 255)

        cv2.putText(
            annotated_frame,
            f"{gesture} ({distance}px)",
            (wrist_x, wrist_y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("Gesture Recognition Test", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
