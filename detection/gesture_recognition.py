
import math


class GestureRecognizer:
    def __init__(self, pinch_start=0.30, pinch_release=0.45):
        self.pinch_start = pinch_start
        self.pinch_release = pinch_release
        self.is_pinching = False

    def calculate_distance(self, point1, point2):
        x1, y1 = point1[:2]
        x2, y2 = point2[:2]

        return math.hypot(x2 - x1, y2 - y1)

    def recognize(self, hand):
        landmarks = hand["landmarks"]

        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        middle_mcp = landmarks[9]

        # Normalize distance using hand size.
        hand_scale = self.calculate_distance(
            wrist,
            middle_mcp
        )

        pinch_distance = self.calculate_distance(
            thumb_tip,
            index_tip
        )

        normalized_distance = (
            pinch_distance / hand_scale
            if hand_scale > 0
            else float("inf")
        )

        # Hysteresis prevents flickering.
        if not self.is_pinching:
            if normalized_distance < self.pinch_start:
                self.is_pinching = True
        else:
            if normalized_distance > self.pinch_release:
                self.is_pinching = False

        return {
            "gesture": "pinch" if self.is_pinching else "none",
            "is_pinching": self.is_pinching,
            "pinch_distance": round(normalized_distance, 3),
            "wrist_position": {
                "x": wrist[0],
                "y": wrist[1]
            }
        }
