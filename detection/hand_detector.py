
import cv2
import numpy as np
from ultralytics import YOLO


class HandDetector:
    """
    Detects hands and extracts their pose landmarks using YOLO.
    """

    # Standard 21-point hand skeleton connections
    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),       # Index
        (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
        (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
        (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
        (5, 9), (9, 13), (13, 17)             # Palm
    ]

    def __init__(
        self,
        model_path="models/yolo26s-pose-hands.pt",
        confidence=0.5,
        image_size=640
    ):
        print("[HandDetector] Loading YOLO model...")

        self.model = YOLO(model_path)
        print("\n========== MODEL INFORMATION ==========")
        print("Model names:", self.model.names)
        print(
            "Keypoint shape:",
            getattr(self.model.model, "kpt_shape", "Not available")
        )
        print(
            "Model task:",
            self.model.task
        )
        print("Model YAML:")
        print(self.model.model.yaml)
        self.confidence = confidence
        self.image_size = image_size

        print("[HandDetector] Model loaded successfully!")

    def detect(self, frame):
        """
        Detect hands using YOLO and use Ultralytics
        built-in annotation.
        """

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        result = results[0]

        # Use the original Ultralytics visualization
        annotated_frame = result.plot()

        hands = []

        if result.keypoints is not None:

            keypoint_data = result.keypoints.data.cpu().numpy()

            for hand_index, points in enumerate(keypoint_data):

                hands.append({
                    "landmarks": points[:, :2].tolist(),
                    "confidence": (
                        float(result.boxes.conf[hand_index].item())
                        if result.boxes is not None
                        else 0.0
                    ),
                    "keypoint_confidence": points[:, 2].tolist()
                })

        return annotated_frame, hands

    def draw_landmarks(self, frame, points, confidence=None):
        """
        Draw hand skeleton while filtering unreliable landmarks.
        """

        points = points.astype(int)

        # Confidence threshold for visualization
        threshold = 0.35

        if confidence is None:
            confidence = np.ones(len(points))

        valid = confidence >= threshold

        # Draw connections only when both landmarks are reliable
        for start, end in self.HAND_CONNECTIONS:

            if not valid[start] or not valid[end]:
                continue

            x1, y1 = points[start]
            x2, y2 = points[end]

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # Draw landmarks
        for index, (x, y) in enumerate(points):

            if not valid[index]:
                continue

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 0, 255),
                -1
            )

            if index in [0, 4, 8, 12, 16, 20]:

                cv2.putText(
                    frame,
                    str(index),
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
