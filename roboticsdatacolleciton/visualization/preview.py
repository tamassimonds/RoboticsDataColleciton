"""Utilities for visualizing detected hands on a live preview window."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Tuple

import cv2
import mediapipe as mp

from roboticsdatacolleciton.types import HandPosition


@dataclass(slots=True)
class HandPreviewRenderer:
    """Render video frames with MediaPipe-style hand overlays."""

    window_name: str = "Hand Tracking"
    circle_radius: int = 4
    line_thickness: int = 2
    _connections: List[Tuple[str, str]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._connections = [
            (self._landmark_name(start), self._landmark_name(end))
            for start, end in mp.solutions.hands.HAND_CONNECTIONS
        ]

    def render(self, frame, positions: Iterable[HandPosition]) -> bool:
        display_frame = frame.copy()
        height, width = display_frame.shape[:2]
        hands = list(positions)

        for idx, hand in enumerate(hands):
            color = self._color_for_hand(hand.label, idx)
            points = self._landmark_points(hand, width, height)
            self._draw_connections(display_frame, points, color)
            self._draw_landmarks(display_frame, points, color)
            self._draw_label(display_frame, hand, color)

        cv2.imshow(self.window_name, display_frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q")):
            return False
        return True

    def close(self) -> None:
        """Destroy the OpenCV window."""

        cv2.destroyWindow(self.window_name)

    def _landmark_points(
        self, hand: HandPosition, width: int, height: int
    ) -> Dict[str, Tuple[int, int]]:
        points: Dict[str, Tuple[int, int]] = {}
        for landmark in hand.landmarks:
            px = int(landmark.x * width)
            py = int(landmark.y * height)
            points[landmark.name] = (px, py)
        return points

    def _draw_connections(
        self, frame, points: Dict[str, Tuple[int, int]], color: Tuple[int, int, int]
    ) -> None:
        for start_name, end_name in self._connections:
            start = points.get(start_name)
            end = points.get(end_name)
            if start and end:
                cv2.line(frame, start, end, color, self.line_thickness)

    def _draw_landmarks(
        self, frame, points: Dict[str, Tuple[int, int]], color: Tuple[int, int, int]
    ) -> None:
        for point in points.values():
            cv2.circle(frame, point, self.circle_radius, color, -1)

    def _draw_label(self, frame, hand: HandPosition, color: Tuple[int, int, int]) -> None:
        px, py = hand.pixel_palm
        label = f"{hand.label} ({hand.confidence:.2f})"
        cv2.putText(
            frame,
            label,
            (px + 10, max(py - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )

    def _color_for_hand(self, label: str, idx: int) -> Tuple[int, int, int]:
        mapping = {
            "Left": (255, 128, 0),
            "Right": (0, 200, 255),
        }
        return mapping.get(label, ((50 + idx * 70) % 255, 255, (150 + idx * 40) % 255))

    def _landmark_name(self, landmark: Any) -> str:
        if hasattr(landmark, "name"):
            return landmark.name  # type: ignore[return-value]
        return mp.solutions.hands.HandLandmark(int(landmark)).name
