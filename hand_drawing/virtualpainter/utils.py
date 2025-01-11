from time import time


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def midpoint(p1, p2):
    return (p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2


def smoothen(p1, p2, alpha=0.6):
    return (
        int((1 - alpha) * p2[0] + alpha * p1[0]),
        int((1 - alpha) * p2[1] + alpha * p1[1]),
    )


class Gestures:
    def __init__(self, threshold=50, hold_time=0.7):
        self.threshold = threshold
        self.hold_time = hold_time
        self.click_start = None
        self.triggered = False

    def is_pinch(self, thumb, ring):
        return distance(thumb, ring) < self.threshold

    def is_adjusting_thickness(self, thumb, middle):
        return distance(thumb, middle) < 160

    def is_painting(self, thumb, index):
        return distance(thumb, index) < self.threshold

    def is_hovering(self, finger, top_left, bottom_right):
        return (
            top_left[0] <= finger[0] <= bottom_right[0]
            and top_left[1] <= finger[1] <= bottom_right[1]
        )

    def two_finger_hold(self, index, middle, top_left, bottom_right):
        if self.is_hovering(index, top_left, bottom_right) and self.is_hovering(
            middle, top_left, bottom_right
        ):
            if self.click_start is None:
                self.click_start = time()
            elapsed = time() - self.click_start
            if elapsed >= self.hold_time and not self.triggered:
                self.triggered = True
                return True
        else:
            self.triggered = False
            self.click_start = None
        return False

    def reset_click_start(self):
        self.click_start = None
        self.triggered = False
