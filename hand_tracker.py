import cv2
import mediapipe as mp
import math


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        return self.hands.process(rgb)

    @staticmethod
    def get_landmark_position(hand_landmarks, index):
        landmark = hand_landmarks.landmark[index]

        return (
            landmark.x,
            landmark.y
        )

    @staticmethod
    def distance(point1, point2):
        return math.sqrt(
            (point1[0] - point2[0]) ** 2
            + (point1[1] - point2[1]) ** 2
        )

    def is_pinching(self, hand_landmarks):
        thumb = self.get_landmark_position(
            hand_landmarks,
            4
        )

        index = self.get_landmark_position(
            hand_landmarks,
            8
        )

        distance = self.distance(
            thumb,
            index
        )

        return distance < 0.055

    def get_pinch_point(self, hand_landmarks):
        thumb = self.get_landmark_position(
            hand_landmarks,
            4
        )

        index = self.get_landmark_position(
            hand_landmarks,
            8
        )

        return (
            (thumb[0] + index[0]) / 2,
            (thumb[1] + index[1]) / 2
        )