import cv2
from time import time
import utils


class Tool:

    def __init__(self, position, box_dim, curr_thickness):
        self.box_dim = box_dim
        self.max_thickness = 100
        self.position = position
        self.curr_thickness = curr_thickness
        self.prev_tool_pos = None

    def add_to_screen(self, frame, color=None):
        if color is None:
            color = (255, 255, 255)
        cv2.putText(
            frame,
            type(self).__name__,
            self.position,
            cv2.FONT_HERSHEY_PLAIN,
            2,
            color,
            2,
        )
        cv2.rectangle(
            frame,
            (self.position[0], self.position[1] - self.box_dim[0]),
            (self.position[0] + self.box_dim[1], self.position[1]),
            color,
            2,
        )


class Brush(Tool):

    def __init__(
        self,
        box_dim=(40, 120),
        position=(50, 80),
        colors=[
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (0, 255, 255),
            (255, 255, 0),
            (255, 0, 255),
            (255, 255, 255),
        ],
        curr_thickness=0.2,
    ):
        super().__init__(position, box_dim, curr_thickness)
        self.colors = colors
        self.curr_color_idx = 0
        self.click_start = None
        self.change_triggered = False

    def change_color(self, index, middle):
        if (
            middle[0] <= self.position[0] + self.box_dim[1]
            and middle[0] >= self.position[0]
            and middle[1] >= self.position[1] - self.box_dim[0]
            and middle[1] <= self.position[1]
            and index[0] >= self.position[0]
            and index[0] <= self.position[0] + self.box_dim[1]
            and index[1] <= self.position[1]
            and index[1] >= self.position[1] - self.box_dim[0]
        ):
            if self.click_start is None:
                self.click_start = time()
            elapsed = time() - self.click_start
            if elapsed >= 0.7 and not self.change_triggered:
                self.change_triggered = True
                self.curr_color_idx += 1
                self.curr_color_idx %= len(self.colors)
        else:
            self.click_start = None
            self.change_triggered = False

    def paint(self, canvas, frame, thumb, index, threshold=50, alpha=0.2):
        if utils.distance(thumb, index) < threshold:
            cv2.circle(frame, index, 80, self.colors[self.curr_color_idx], 2)
            if self.prev_tool_pos is None:
                self.prev_tool_pos = index
            else:
                cx = int((1 - alpha) * self.prev_tool_pos[0] + alpha * index[0])
                cy = int((1 - alpha) * self.prev_tool_pos[1] + alpha * index[1])
                cv2.line(
                    canvas,
                    self.prev_tool_pos,
                    (cx, cy),
                    self.colors[self.curr_color_idx],
                    int(self.max_thickness * self.curr_thickness),
                )
            self.prev_tool_pos = index
        else:
            self.prev_tool_pos = None


class Eraser(Tool):
    def __init__(self, position=(50, 30), box_dim=(40, 120), curr_thickness=0.2):
        super().__init__(position, box_dim, curr_thickness)

    def erase(self, canvas, thumb, index, threshold=50):
        if utils.distance(thumb, index) < threshold:
            if self.prev_tool_pos is None:
                self.prev_tool_pos = index
            else:
                cv2.line(
                    canvas,
                    self.prev_tool_pos,
                    utils.midpoint(thumb, index),
                    (0, 0, 0),
                    int(self.max_thickness * self.curr_thickness),
                )
            self.prev_tool_pos = index
        else:
            self.prev_tool_pos = None
