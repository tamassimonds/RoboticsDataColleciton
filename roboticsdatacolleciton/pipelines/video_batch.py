"""Offline video processing pipeline."""
from __future__ import annotations

from typing import Optional, Sequence

from roboticsdatacolleciton.detection import MediaPipeHandTracker
from roboticsdatacolleciton.loggers import HandLogWriter
from roboticsdatacolleciton.types import HandPosition
from roboticsdatacolleciton.video import VideoFileStream
from roboticsdatacolleciton.visualization import HandPreviewRenderer


class VideoProcessingPipeline:
    """Runs detection over a video file with optional preview/logging."""

    def __init__(
        self,
        video_stream: VideoFileStream,
        detector: MediaPipeHandTracker,
        logger: Optional[HandLogWriter] = None,
        visualizer: Optional[HandPreviewRenderer] = None,
    ) -> None:
        self.video_stream = video_stream
        self.detector = detector
        self.logger = logger
        self.visualizer = visualizer

    def run(self) -> None:
        try:
            with self.video_stream as stream:
                try:
                    for frame_index, frame in stream.frames():
                        positions = self.detector.detect(frame)
                        self._emit(frame_index, positions)
                        if self.visualizer:
                            keep_running = self.visualizer.render(frame, positions)
                            if not keep_running:
                                break
                except KeyboardInterrupt:
                    print("\nStopping video processing early...")
        finally:
            self.detector.close()
            if self.logger:
                self.logger.close()
            if self.visualizer:
                self.visualizer.close()

    def _emit(self, frame_index: int, positions: Sequence[HandPosition]) -> None:
        if self.logger:
            self.logger.record(frame_index, positions)
