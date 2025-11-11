"""Camera capture utilities to abstract OpenCV specifics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional

import cv2

from .errors import CameraOpenError


@dataclass
class CameraStream:
    """Context manager around cv2.VideoCapture."""

    device_index: int = 0
    frame_width: Optional[int] = None
    frame_height: Optional[int] = None

    def __post_init__(self) -> None:
        self._capture: Optional[cv2.VideoCapture] = None

    def __enter__(self) -> "CameraStream":
        self._capture = cv2.VideoCapture(self.device_index)
        if not self._capture.isOpened():
            raise CameraOpenError(self.device_index)

        if self.frame_width:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        if self.frame_height:
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:  # noqa: ANN001
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def frames(self) -> Iterator:
        if self._capture is None:
            raise RuntimeError("CameraStream must be entered before reading frames")

        while True:
            success, frame = self._capture.read()
            if not success:
                raise RuntimeError("Failed to read from camera stream")
            yield frame
