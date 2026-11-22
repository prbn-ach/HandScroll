
import cv2

from detection.hand_detector import HandDetector


def main():

    # Initialize detector
    detector = HandDetector(
        model_path="models/yolo26s-pose-hands.pt",
        confidence=0.5
    )

    # Initialize webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Webcam started.")
    print("[INFO] Press Q to quit.")

    try:
        while True:

            success, frame = camera.read()

            if not success:
                print("[ERROR] Could not read webcam frame.")
                break

            # Mirror the webcam
            frame = cv2.flip(frame, 1)

            # Detect hands
            annotated_frame, hands = detector.detect(frame)

            # Display detection count
            cv2.putText(
                annotated_frame,
                f"Hands detected: {len(hands)}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # Display webcam
            cv2.imshow(
                "HandScroll - Hand Detection",
                annotated_frame
            )
            annotated_frame, hands = detector.detect(frame)

            print(f"Detected hands: {len(hands)}")
            # Exit when Q is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
