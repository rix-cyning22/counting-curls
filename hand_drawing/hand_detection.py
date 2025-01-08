from mediapipe.python.solutions import hands, drawing_utils
import cv2
from dataclasses import dataclass


class HandDetector:
    def __init__(
        self,
        static=False,
        max_hands=2,
        detection_confidence=0.5,
        tracking_confidence=0.5,
    ):
        self.static = static
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.hands = hands.Hands(
            static_image_mode=self.static,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        self.fingertip_idx = {
            4: "thumb",
            8: "index",
            12: "middle",
            16: "ring",
            20: "pinky",
        }

    def find_hands(self, frame, draw_landmark=False):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw_landmark:
                    drawing_utils.draw_landmarks(frame, handlms, hands.HAND_CONNECTIONS)
        return frame

    def __gethand__(self, frame, hand, draw_landmark=False):
        for idx, lm in enumerate(hand.landmark):
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            if draw_landmark and idx in self.fingertip_idx.keys():
                self.hand_landmarks[self.fingertip_idx[idx]] = (cx, cy)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 0), cv2.FILLED)

    def get_hand_landmarks(self, frame, hand_idx=0, draw_landmark=False):
        self.hand_landmarks = None
        if self.results.multi_hand_landmarks:
            self.hand_landmarks = {}
            hand = self.results.multi_hand_landmarks[hand_idx]
            self.__gethand__(frame, hand, draw_landmark=draw_landmark)

        return self.hand_landmarks
