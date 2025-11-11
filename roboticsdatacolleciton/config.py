"""Configuration objects shared across the app."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RealtimeTrackingConfig:
    """Holds runtime settings for the realtime hand tracking pipeline."""

    device_index: int = 0
    frame_width: int | None = None
    frame_height: int | None = None
    max_num_hands: int = 2
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5


@dataclass(slots=True)
class BatchProcessingConfig:
    """Placeholder for future batch processing configuration."""

    input_path: str | None = None
    output_path: str | None = None
