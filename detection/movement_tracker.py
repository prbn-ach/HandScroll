
class MovementTracker:
    def __init__(self):
        self.previous_y = None
        self.total_movement = 0.0
        self.active = False

    def update(self, gesture_result):
        """
        Track vertical wrist movement while pinching.

        Positive delta_y = hand moves down.
        Negative delta_y = hand moves up.
        """

        if not gesture_result["is_pinching"]:
            self.reset()

            return {
                "active": False,
                "delta_y": 0.0,
                "total_movement": 0.0
            }

        current_y = gesture_result["wrist_position"]["y"]

        # First frame of a pinch: establish starting position.
        if not self.active:
            self.previous_y = current_y
            self.total_movement = 0.0
            self.active = True

            return {
                "active": True,
                "delta_y": 0.0,
                "total_movement": 0.0
            }

        delta_y = current_y - self.previous_y

        self.previous_y = current_y
        self.total_movement += delta_y

        return {
            "active": True,
            "delta_y": delta_y,
            "total_movement": self.total_movement
        }

    def reset(self):
        self.previous_y = None
        self.total_movement = 0.0
        self.active = False
