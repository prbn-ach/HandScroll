
import math


class GestureRecognizer:
    def __init__(self, pinch_threshold=40):
        self.pinch_threshold = pinch_threshold

    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two landmarks."""
        x1, y1 = point1[:2]
        x2, y2 = point2[:2]

        return math.hypot(x2 - x1, y2 - y1)

    def recognize(self, hand):
        """
        Recognize gestures from one detected hand.

        Returns:
            Dictionary containing gesture and hand position.
        """
        landmarks = hand["landmarks"]

        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        pinch_distance = self.calculate_distance(
            thumb_tip,
            index_tip
        )

        is_pinching = pinch_distance < self.pinch_threshold

        return {
            "gesture": "pinch" if is_pinching else "none",
            "is_pinching": is_pinching,
            "pinch_distance": round(pinch_distance, 2),
            "wrist_position": {
                "x": wrist[0],
                "y": wrist[1]
            }
        }
