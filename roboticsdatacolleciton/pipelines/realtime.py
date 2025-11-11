"""Realtime hand tracking pipeline."""
from __future__ import annotations

import time
from typing import Callable, Iterable, Optional

from roboticsdatacolleciton.config import RealtimeTrackingConfig
from roboticsdatacolleciton.detection import MediaPipeHandTracker
from roboticsdatacolleciton.types import HandPosition
from roboticsdatacolleciton.video import CameraStream
from roboticsdatacolleciton.visualization import HandPreviewRenderer


class RealTimeHandTrackingPipeline:
    """Coordinates camera ingestion and detection, emitting console output."""

    def __init__(
        self,
        camera: CameraStream,
        detector: MediaPipeHandTracker,
        config: RealtimeTrackingConfig,
        output_fn: Callable[[Iterable[HandPosition]], None],
        visualizer: Optional[HandPreviewRenderer] = None,
    ) -> None:
        self.camera = camera
        self.detector = detector
        self.config = config
        self.output_fn = output_fn
        self.visualizer = visualizer

    def run(self) -> None:
        """Continuously read frames, detect hands, and stream results."""

        with self.camera as camera:
            try:
                for frame in camera.frames():
                    positions = self.detector.detect(frame)
                    self.output_fn(positions)
                    if self.visualizer:
                        keep_running = self.visualizer.render(frame, positions)
                        if not keep_running:
                            break
                    time.sleep(0.01)
            except KeyboardInterrupt:
                print("\nStopping realtime hand tracking...")
            finally:
                self.detector.close()
                if self.visualizer:
                    self.visualizer.close()
