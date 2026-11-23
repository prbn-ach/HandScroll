import cv2

from detection.hand_detector import HandDetector


detector = HandDetector()

cap = cv2.VideoCapture(0)

try:
    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        annotated_frame, hands = detector.detect(frame)

        for hand in hands:
            wrist = hand["landmarks"][0]

            cv2.putText(
                annotated_frame,
                f"{hand['handedness']} "
                f"({hand['confidence']:.2f})",
                (int(wrist[0]), int(wrist[1]) - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

        cv2.imshow("MediaPipe Hand Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    detector.close()
    cv2.destroyAllWindows()
