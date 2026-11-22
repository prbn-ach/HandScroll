
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
        self.confidence = confidence
        self.image_size = image_size

        print("[HandDetector] Model loaded successfully!")

    def detect(self, frame):
        """
        Process one webcam frame.

        Returns:
            annotated_frame: Frame with detected landmarks.
            hands: List of detected hand information.
        """

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        annotated_frame = frame.copy()
        hands = []

        if not results:
            return annotated_frame, hands

        result = results[0]

        if result.keypoints is None:
            return annotated_frame, hands

        # Extract keypoints
        keypoints = result.keypoints.xy.cpu().numpy()

        # Extract keypoint confidence if available
        keypoint_conf = None

        if result.keypoints.conf is not None:
            keypoint_conf = result.keypoints.conf.cpu().numpy()

        # Extract bounding boxes
        boxes = []

        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()

        for hand_index, points in enumerate(keypoints):

            if len(points) != 21:
                continue

            hand_confidence = (
                float(result.boxes.conf[hand_index].item())
                if result.boxes is not None
                else 0.0
            )

            # Convert coordinates into Python lists
            landmarks = points.tolist()

            hand = {
                "landmarks": landmarks,
                "confidence": hand_confidence,
                "bbox": (
                    boxes[hand_index].tolist()
                    if hand_index < len(boxes)
                    else None
                ),
                "keypoint_confidence": (
                    keypoint_conf[hand_index].tolist()
                    if keypoint_conf is not None
                    else None
                )
            }

            hands.append(hand)

            self.draw_landmarks(
                annotated_frame,
                points
            )

        return annotated_frame, hands

    def draw_landmarks(self, frame, points):
        """
        Draw hand skeleton and landmarks.
        """

        points = points.astype(int)

        # Draw connections
        for start, end in self.HAND_CONNECTIONS:

            x1, y1 = points[start]
            x2, y2 = points[end]

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # Draw individual landmarks
        for index, (x, y) in enumerate(points):

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 0, 255),
                -1
            )

            # Label important landmarks
            if index in [0, 4, 8, 12]:

                cv2.putText(
                    frame,
                    str(index),
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255, 255, 255),
                    1
                )
