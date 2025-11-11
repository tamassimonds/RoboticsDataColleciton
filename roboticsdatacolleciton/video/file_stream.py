"""Utilities for reading frames from a video file."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Tuple

import cv2
import numpy as np

from .errors import VideoFileOpenError


@dataclass
class VideoFileStream:
    """Context-managed reader over a video file."""

    path: str | Path

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self._capture: Optional[cv2.VideoCapture] = None

    def __enter__(self) -> "VideoFileStream":
        if not self.path.exists():
            raise VideoFileOpenError(self.path, reason="file-not-found")

        self._capture = cv2.VideoCapture(str(self.path))
        if not self._capture.isOpened():
            raise VideoFileOpenError(self.path, reason="open-failed")
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:  # noqa: ANN001
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def frames(self) -> Iterator[Tuple[int, np.ndarray]]:
        if self._capture is None:
            raise RuntimeError("VideoFileStream must be entered before reading frames")

        frame_idx = 0
        while True:
            success, frame = self._capture.read()
            if not success:
                break
            yield frame_idx, frame
            frame_idx += 1
