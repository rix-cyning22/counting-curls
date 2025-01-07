from dataclasses import dataclass


@dataclass
class Brush:
    thickness: int = 10
    colors: list = [
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 255, 0),
        (255, 0, 255),
        (255, 255, 255),
    ]


@dataclass
class Eraser:
    thickness: int = 50
