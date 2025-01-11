import cv2
import utils
from abc import ABC, abstractmethod
from PIL import Image
import tkinter as tk
from tkinter import filedialog


class Tool(ABC):
    def __init__(self, position, gestures, box_dim=(40, 120)):
        self.box_dim = box_dim
        self.position = position
        self.gestures = utils.Gestures()

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

    @abstractmethod
    def use(self, *args, **kwargs):
        pass


class Adjustable(Tool):
    def __init__(self, position, box_dim=(40, 120), curr_thickness=0.2):
        super().__init__(position, box_dim)
        self.curr_thickness = curr_thickness
        self.max_thickness = 100
        self.prev_pos = None
        self.is_locked = False
        self.thickness_before_locked = self.curr_thickness

    def thicc(self, mode=None):
        if mode == "pinch":
            return int(self.max_thickness * self.thickness_before_locked)
        elif mode == "max":
            return self.max_thickness
        return int(self.max_thickness * self.curr_thickness)

    def change_thickness(self, frame, landmarks, color=(0, 0, 0)):
        thumb = landmarks["thumb"]
        middle = landmarks["middle"]
        ring = landmarks["ring"]

        if self.gestures.is_pinch(thumb, ring):
            if not self.is_locked:
                self.thickness_before_locked = self.curr_thickness
            self.is_locked = True
            distance = utils.distance(middle, thumb)
            self.curr_thickness = max(0.05, min(1.0, distance / 160))
            center = utils.midpoint(thumb, ring)
            cv2.circle(frame, center, self.thicc(), color, cv2.FILLED)
            cv2.circle(
                frame, center, self.thicc(mode="pinch"), (255, 255, 255), cv2.FILLED
            )
            cv2.circle(frame, center, self.thicc(mode="max") + 5, color, 2)
            cv2.putText(
                frame,
                f"{self.thicc()}",
                (
                    center[0] + self.thicc(mode="max") + 2,
                    center[1] + self.thicc(mode="max") + 2,
                ),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                color,
                2,
            )
        else:
            self.is_locked = False

    def paint(self, canvas, frame, thumb, index, alpha=0.2, color=(0, 0, 0)):
        if self.gestures.is_painting(thumb, index):
            cv2.circle(frame, index, self.thicc() + 5, color, 2)
            if self.prev_pos is None:
                self.prev_pos = index
            else:
                center = utils.midpoint(index, thumb)
                c = utils.smoothen(center, self.prev_pos, alpha=alpha)
                cv2.line(canvas, self.prev_pos, c, color, self.thicc())
            self.prev_pos = index
        else:
            self.prev_pos = None

    def on_free(self, *args, **kwargs):
        pass

    def use(self, *args, **kwargs):
        canvas = args[0]
        frame = args[1]
        landmarks = args[2]
        if not self.is_locked:
            alpha = kwargs.get("alpha", 0.4)
            self.paint(
                canvas,
                frame,
                landmarks["thumb"],
                landmarks["index"],
                alpha=alpha,
            )
            self.on_free(*args, **kwargs)
        self.change_thickness(frame, landmarks, **kwargs)


class ColorTool(Adjustable):
    def __init__(
        self,
        position,
        box_dim=(40, 120),
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
        super().__init__(position, box_dim, curr_thickness=curr_thickness)
        self.colors = colors
        self.curr_color_idx = 0

    def curr_color(self):
        return self.colors[self.curr_color_idx]

    def add_to_screen(self, frame):
        super().add_to_screen(frame, color=self.curr_color())

    def change_color(self, index, middle):
        if self.gestures.two_finger_hold(
            index,
            middle,
            self.position,
            (self.position[0] + self.box_dim[1], self.position[1]),
        ):
            self.curr_color_idx = (self.curr_color_idx + 1) % len(self.colors)

    def change_thickness(self, frame, landmarks):
        super().change_thickness(frame, landmarks, self.curr_color())

    def paint(self, canvas, frame, thumb, index, alpha=0.2):
        super().paint(canvas, frame, thumb, index, alpha, self.curr_color())

    def on_free(self, *args):
        landmarks = args[2]
        self.change_color(landmarks["index"], landmarks["middle"])


class Eraser(Adjustable):
    def __init__(self, position, box_dim=(40, 120), curr_thickness=0.2):
        super().__init__(position, box_dim, curr_thickness=curr_thickness)


class Save(Tool):
    def __init__(self, position, box_dim=(40, 120)):
        super().__init__(position, box_dim)

    def use(self, *args):
        canvas = args[0]
        landmarks = args[2]
        middle = landmarks["middle"]
        index = landmarks["index"]

        if self.gestures.two_finger_hold(
            index,
            middle,
            self.position,
            (self.position[0] + self.box_dim[1], self.position[1] + self.box_dim[0]),
        ):
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save Canvas",
            )
            root.destroy()
            if file_path:
                canvas = 255 - canvas
                img = Image.fromarray(canvas)
                img.save(file_path)
