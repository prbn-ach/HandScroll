
import cv2

from detection.hand_detector import HandDetector
from detection.gesture_recognition import GestureRecognizer


detector = HandDetector()
recognizer = GestureRecognizer(
    pinch_start=0.30,
    pinch_release=0.45
)

cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        annotated_frame, hands = detector.detect(frame)

        if hands:
            # Test with the first detected hand.
            hand = hands[0]

            result = recognizer.recognize(hand)

            gesture = result["gesture"]
            distance = result["pinch_distance"]

            wrist = result["wrist_position"]

            color = (
                (0, 255, 0)
                if result["is_pinching"]
                else (0, 0, 255)
            )

            cv2.putText(
                annotated_frame,
                f"{gesture} | distance: {distance}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        cv2.imshow("Pinch Gesture Test", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    detector.close()
    cv2.destroyAllWindows()
