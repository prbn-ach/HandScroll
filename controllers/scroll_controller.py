
import math
import pyautogui


class ScrollController:
    def __init__(
        self,
        sensitivity=0.025,
        smoothing=0.20,
        dead_zone=1.5,
        max_delta=35
    ):
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        self.dead_zone = dead_zone
        self.max_delta = max_delta

        self.smoothed_delta = 0.0
        self.scroll_accumulator = 0.0

    def scroll(self, delta_y):
        """
        Smooth hand movement and convert it into scroll events.

        Positive delta_y = hand moves down.
        Negative delta_y = hand moves up.
        """

        # Prevent unusually large tracking jumps.
        delta_y = max(
            -self.max_delta,
            min(self.max_delta, delta_y)
        )

        # Exponential moving average.
        self.smoothed_delta = (
            self.smoothing * delta_y
            + (1 - self.smoothing) * self.smoothed_delta
        )

        # Ignore small movements.
        if abs(self.smoothed_delta) < self.dead_zone:
            return

        # Accumulate fractional scroll movement.
        self.scroll_accumulator += (
            -self.smoothed_delta * self.sensitivity
        )

        # Only generate complete scroll steps.
        scroll_amount = math.trunc(self.scroll_accumulator)

        if scroll_amount != 0:
            pyautogui.scroll(scroll_amount)
            self.scroll_accumulator -= scroll_amount

    def reset(self):
        """Reset smoothing and accumulated movement."""
        self.smoothed_delta = 0.0
        self.scroll_accumulator = 0.0
