
import cv2
import mediapipe as mp
import time
from pathlib import Path


HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


class HandDetector:
    def __init__(self, max_hands=2, detection_confidence=0.5,
                 tracking_confidence=0.5):

        model_path = (
            Path(__file__).resolve().parents[1]
            / "models"
            / "hand_landmarker.task"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"MediaPipe model not found: {model_path}"
            )

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=str(model_path)
            ),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.landmarker = (
            mp.tasks.vision.HandLandmarker.create_from_options(options)
        )

        self.last_timestamp = -1

    def detect(self, frame):
        height, width, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp = time.monotonic_ns() // 1_000_000

        # Video timestamps must increase strictly.
        timestamp = max(timestamp, self.last_timestamp + 1)
        self.last_timestamp = timestamp

        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp
        )

        annotated_frame = frame.copy()
        hands = []

        for index, hand_landmarks in enumerate(result.hand_landmarks):
            landmarks = []

            for point in hand_landmarks:
                x = point.x * width
                y = point.y * height
                z = point.z

                landmarks.append([x, y, z])

            # Draw connections.
            for start, end in HAND_CONNECTIONS:
                p1 = (int(landmarks[start][0]),
                      int(landmarks[start][1]))
                p2 = (int(landmarks[end][0]),
                      int(landmarks[end][1]))

                cv2.line(
                    annotated_frame, p1, p2,
                    (0, 255, 0), 2
                )

            # Draw landmarks.
            for point in landmarks:
                cv2.circle(
                    annotated_frame,
                    (int(point[0]), int(point[1])),
                    4,
                    (0, 0, 255),
                    -1
                )

            handedness = "Unknown"
            score = 0.0

            if index < len(result.handedness):
                category = result.handedness[index][0]
                handedness = category.category_name
                score = category.score

            hands.append({
                "landmarks": landmarks,
                "handedness": handedness,
                "confidence": score
            })

        return annotated_frame, hands

    def close(self):
        self.landmarker.close()
