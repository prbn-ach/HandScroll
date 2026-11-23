
import cv2

from detection.hand_detector import HandDetector
from detection.gesture_recognition import GestureRecognizer
from detection.movement_tracker import MovementTracker


detector = HandDetector()
recognizer = GestureRecognizer(
    pinch_start=0.30,
    pinch_release=0.45
)
tracker = MovementTracker()

cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        annotated_frame, hands = detector.detect(frame)

        if hands:
            hand = hands[0]

            gesture = recognizer.recognize(hand)
            movement = tracker.update(gesture)

            if movement["active"]:
                status = "TRACKING"
                delta = movement["delta_y"]
                total = movement["total_movement"]
            else:
                status = "NOT TRACKING"
                delta = 0
                total = 0

            color = (
                (0, 255, 0)
                if movement["active"]
                else (0, 0, 255)
            )

            cv2.putText(
                annotated_frame,
                f"Gesture: {gesture['gesture']}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.putText(
                annotated_frame,
                f"Status: {status}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.putText(
                annotated_frame,
                f"Delta Y: {delta:.2f}px",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"Total movement: {total:.2f}px",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

        else:
            tracker.reset()

        cv2.imshow("Hand Movement Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    detector.close()
    cv2.destroyAllWindows()
