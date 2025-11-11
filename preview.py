"""Quick video preview with hand landmark overlays."""
from __future__ import annotations

import argparse

from roboticsdatacolleciton.detection import MediaPipeHandTracker
from roboticsdatacolleciton.pipelines import VideoProcessingPipeline
from roboticsdatacolleciton.video import VideoFileOpenError, VideoFileStream
from roboticsdatacolleciton.visualization import HandPreviewRenderer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview hand tracking on a recorded video")
    parser.add_argument(
        "--video-path",
        type=str,
        default="data/videos/sample.mp4",
        help="Path to the video to preview",
    )
    parser.add_argument("--max-num-hands", type=int, default=2, help="Maximum hands to track")
    parser.add_argument("--min-detection-confidence", type=float, default=0.5)
    parser.add_argument("--min-tracking-confidence", type=float, default=0.5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detector = MediaPipeHandTracker(
        max_num_hands=args.max_num_hands,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )
    preview = HandPreviewRenderer(window_name="Video Preview")
    stream = VideoFileStream(args.video_path)
    pipeline = VideoProcessingPipeline(
        video_stream=stream,
        detector=detector,
        logger=None,
        visualizer=preview,
    )
    try:
        pipeline.run()
    except VideoFileOpenError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
