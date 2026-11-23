
import pyautogui


class ScrollController:
    def __init__(self, sensitivity=1.0, dead_zone=2):
        self.sensitivity = sensitivity
        self.dead_zone = dead_zone

    def scroll(self, delta_y):
        """
        Convert hand movement into mouse scrolling.

        Moving hand up   -> scroll up
        Moving hand down -> scroll down
        """

        if abs(delta_y) < self.dead_zone:
            return

        scroll_amount = int(delta_y * self.sensitivity)

        if scroll_amount == 0:
            return

        # Invert direction:
        # Hand moves up (negative delta) -> positive scroll.
        pyautogui.scroll(-scroll_amount)
