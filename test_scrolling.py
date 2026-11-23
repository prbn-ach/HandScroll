
import cv2

from detection.hand_detector import HandDetector
from detection.gesture_recognition import GestureRecognizer
from detection.movement_tracker import MovementTracker
from controllers.scroll_controller import ScrollController


detector = HandDetector()

recognizer = GestureRecognizer(
    pinch_start=0.30,
    pinch_release=0.45
)

tracker = MovementTracker()

scroll_controller = ScrollController(
    sensitivity=0.025,
    smoothing=0.55,
    dead_zone=0.8,
    max_delta=35
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
            hand = hands[0]

            gesture = recognizer.recognize(hand)
            movement = tracker.update(gesture)

            if movement["active"]:
                delta = movement["delta_y"]

                scroll_controller.scroll(delta)

                status = "SCROLLING"
                color = (0, 255, 0)

            else:
                scroll_controller.reset()

                status = "NOT SCROLLING"
                color = (0, 0, 255)

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
                status,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.putText(
                annotated_frame,
                f"Movement: {movement['delta_y']:.2f}px",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

        else:
            tracker.reset()
            scroll_controller.reset()

        cv2.imshow("HandScroll - Scrolling Test", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    detector.close()
    cv2.destroyAllWindows()
