import mediapipe as mp
from mediapipe.python import hands, drawing_utils
import cv2


class HandDetector:
    def __init__(
        self,
        static=False,
        maxhands=2,
        detection_confidence=0.5,
        tracking_confidence=0.5,
    ):
        self.static = static
        self.maxhands = maxhands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.hands = hands.Hands(
            self.static,
            self.maxhands,
            self.detection_confidence,
            self.tracking_confidence,
        )
        self.finger_idx = [4, 8, 12, 16, 20]

    def findhands(self, frame, draw_landmark=False):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw_landmark:
                    drawing_utils.draw_landmarks(
                        frame, handlms, self.mphands.HAND_CONNECTIONS
                    )
