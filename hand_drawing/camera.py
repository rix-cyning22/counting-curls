import cv2
from hand_detection import HandDetector
from tools import Brush, Eraser
import numpy as np

cam_width, cam_height = 960, 1080

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

hand_detector = HandDetector(detection_confidence=0.8, tracking_confidence=0.9)
brush = Brush()
eraser = Eraser()

curr_tool = brush
canvas = np.zeros((cam_height // 2, cam_width, 3), np.uint8)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = hand_detector.find_hands(frame, draw_landmark=False)
    landmarks = hand_detector.get_hand_landmarks(frame, draw_landmark=True)
    brush.add_to_screen(frame, color=brush.colors[brush.curr_color_idx])
    eraser.add_to_screen(frame)

    if landmarks is not None:
        brush.change_color(landmarks["index"], landmarks["middle"])
        brush.paint(canvas, frame, landmarks["thumb"], landmarks["index"])
    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    cv2.imshow("Camera", combined)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
