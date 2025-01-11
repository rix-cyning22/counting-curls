import cv2
from virtualpainter.utils import Gestures
from tools import ToolLike

gestures = Gestures()


class ToolsManager:
    def __init__(self, toolbox):
        tool_types = [type(tool).__name__ for tool in toolbox]
        assert len(tool_types) == len(set(tool_types)), "Duplicate tools found!"
        self.toolbox = toolbox
        self.curr_tool_idx = 0
        self.position = (500, 30)

    def add_tool(self, tool):
        assert isinstance(
            tool, ToolLike
        ), f"tool to be appended must be of type {ToolLike}"
        self.toolbox.append(tool)

    def add_to_screen(self, frame):
        for tool in self.toolbox:
            tool.add_to_screen(frame)
        cv2.putText(
            frame,
            f"Current Tool: {type(self.current_tool()).__name__}",
            self.position,
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 255, 0),
            2,
        )

    def current_tool(self):
        return self.toolbox[self.curr_tool_idx]

    def check_finger_position(self, index, thumb):
        for idx, tool in enumerate(self.toolbox):
            is_index_in_tool = gestures.is_hovering(
                index,
                tool.position,
                (
                    tool.position[0] + tool.box_dim[1],
                    tool.position[1] + tool.box_dim[0],
                ),
            )
            is_thumb_outside_tool = not gestures.is_hovering(
                thumb,
                tool.position,
                (
                    tool.position[0] + tool.box_dim[1],
                    tool.position[1] + tool.box_dim[0],
                ),
            )

            if is_index_in_tool and is_thumb_outside_tool:
                self.curr_tool_idx = idx
                break

    def use(self, *args, **kwargs):
        self.current_tool().use(*args, **kwargs)
