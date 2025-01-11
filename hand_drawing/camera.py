import cv2
from virtualpainter.hand_detection import HandDetector
import virtualpainter.tools as tools
import numpy as np
from virtualpainter.tools_manager import ToolsManager

cam_width, cam_height = 960, 1080

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

hand_detector = HandDetector(detection_confidence=0.8, tracking_confidence=0.9)
tool_manager = ToolsManager(
    [
        tools.Brush(position=(50, 120)),
        tools.Eraser(position=(50, 50)),
        tools.Save(position=(500, 50)),
    ]
)

canvas = np.zeros((cam_height // 2, cam_width, 3), np.uint8)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = hand_detector.find_hands(frame, draw_landmark=False)
    landmarks = hand_detector.get_hand_landmarks(frame, draw_landmark=True)
    tool_manager.add_to_screen(frame)

    if landmarks is not None:
        tool_manager.use(canvas, frame, landmarks)
        tool_manager.check_finger_position(landmarks["index"], landmarks["thumb"])
    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    cv2.imshow("Camera", combined)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
