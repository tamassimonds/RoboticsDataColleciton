"""MediaPipe-based hand detection module."""
from __future__ import annotations

from typing import List

import cv2
import mediapipe as mp

from roboticsdatacolleciton.types import HandPosition, Landmark


class MediaPipeHandTracker:
    """Thin wrapper around MediaPipe Hands that returns HandPosition items."""

    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self._mp_hands = mp.solutions.hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1,
        )
        self._mp_landmarks = mp.solutions.hands.HandLandmark

    def detect(self, frame) -> List[HandPosition]:  # type: ignore[override]
        """Run detection on a BGR frame and return structured hand positions."""

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self._mp_hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.multi_hand_landmarks:
            return []

        image_height, image_width = frame.shape[:2]
        positions: List[HandPosition] = []

        hand_labels: List[str] = []
        confidences: List[float] = []
        if results.multi_handedness:
            hand_labels = [classification.classification[0].label for classification in results.multi_handedness]
            confidences = [classification.classification[0].score for classification in results.multi_handedness]
        else:
            hand_labels = ["UNKNOWN"] * len(results.multi_hand_landmarks)
            confidences = [0.0] * len(results.multi_hand_landmarks)

        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            label = hand_labels[idx] if idx < len(hand_labels) else "UNKNOWN"
            score = confidences[idx] if idx < len(confidences) else 0.0

            landmark_list: List[Landmark] = []
            xs, ys = [], []
            for landmark_enum in self._mp_landmarks:
                landmark = hand_landmarks.landmark[landmark_enum.value]
                xs.append(landmark.x)
                ys.append(landmark.y)
                landmark_list.append(
                    Landmark(
                        name=landmark_enum.name,
                        x=landmark.x,
                        y=landmark.y,
                        z=landmark.z,
                    )
                )

            palm_x = sum(xs) / len(xs)
            palm_y = sum(ys) / len(ys)
            pixel_x = int(palm_x * image_width)
            pixel_y = int(palm_y * image_height)

            positions.append(
                HandPosition(
                    label=label,
                    confidence=score,
                    normalized_palm=(palm_x, palm_y),
                    pixel_palm=(pixel_x, pixel_y),
                    landmarks=landmark_list,
                )
            )

        return positions

    def close(self) -> None:
        """Release MediaPipe resources."""

        self._mp_hands.close()
