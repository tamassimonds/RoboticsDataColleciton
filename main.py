"""Entrypoint for running realtime hand tracking."""
from __future__ import annotations

import argparse
from typing import Iterable

from roboticsdatacolleciton.config import RealtimeTrackingConfig
from roboticsdatacolleciton.detection import MediaPipeHandTracker
from roboticsdatacolleciton.pipelines import RealTimeHandTrackingPipeline
from roboticsdatacolleciton.types import HandPosition
from roboticsdatacolleciton.video import CameraOpenError, CameraStream
from roboticsdatacolleciton.visualization import HandPreviewRenderer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Realtime hand tracking demo")
    parser.add_argument("--device-index", type=int, default=0, help="Camera index to open")
    parser.add_argument("--frame-width", type=int, default=None, help="Optional capture width")
    parser.add_argument("--frame-height", type=int, default=None, help="Optional capture height")
    parser.add_argument("--min-detection-confidence", type=float, default=0.5, help="MediaPipe detection score threshold")
    parser.add_argument("--min-tracking-confidence", type=float, default=0.5, help="MediaPipe tracking score threshold")
    parser.add_argument("--max-num-hands", type=int, default=2, help="Maximum hands to track")
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable the OpenCV window that shows the live preview with overlays.",
    )
    return parser.parse_args()


def console_output(positions: Iterable[HandPosition]) -> None:
    formatted = []
    for idx, position in enumerate(positions, start=1):
        px, py = position.pixel_palm
        formatted.append(
            f"Hand {idx} ({position.label}) @ ({px:4d}, {py:4d}) conf={position.confidence:.2f}"
        )
    if not formatted:
        message = "No hands detected"
    else:
        message = " | ".join(formatted)
    print(f"\r{message}", end="", flush=True)


def main() -> None:
    args = parse_args()
    config = RealtimeTrackingConfig(
        device_index=args.device_index,
        frame_width=args.frame_width,
        frame_height=args.frame_height,
        max_num_hands=args.max_num_hands,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )

    camera = CameraStream(
        device_index=config.device_index,
        frame_width=config.frame_width,
        frame_height=config.frame_height,
    )
    detector = MediaPipeHandTracker(
        max_num_hands=config.max_num_hands,
        min_detection_confidence=config.min_detection_confidence,
        min_tracking_confidence=config.min_tracking_confidence,
    )

    visualizer = None if args.no_preview else HandPreviewRenderer(window_name="Hand Tracking Preview")

    pipeline = RealTimeHandTrackingPipeline(
        camera=camera,
        detector=detector,
        config=config,
        output_fn=console_output,
        visualizer=visualizer,
    )

    try:
        pipeline.run()
    except CameraOpenError as exc:
        print(
            "\nCould not access the camera. Verify permissions (System Settings → Privacy & Security → Camera) "
            "and confirm the device index is correct."
        )
        raise SystemExit(str(exc)) from exc
    finally:
        print()


if __name__ == "__main__":
    main()
