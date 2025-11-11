"""Process a recorded video, logging detections to disk."""
from __future__ import annotations

import argparse
from pathlib import Path

from roboticsdatacolleciton.detection import MediaPipeHandTracker
from roboticsdatacolleciton.loggers import HandLogWriter
from roboticsdatacolleciton.pipelines import VideoProcessingPipeline
from roboticsdatacolleciton.video import VideoFileOpenError, VideoFileStream
from roboticsdatacolleciton.visualization import HandPreviewRenderer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect hands in a video and log the results")
    parser.add_argument(
        "--video-path",
        type=str,
        default="data/videos/sample.mp4",
        help="Path to the input video",
    )
    parser.add_argument(
        "--log-path",
        type=str,
        default="logs/hand_positions.parquet",
        help="Where to store the Parquet log",
    )
    parser.add_argument(
        "--summary-path",
        type=str,
        default=None,
        help="Optional explicit path for the frame summary JSON",
    )
    parser.add_argument("--max-num-hands", type=int, default=2, help="Maximum hands to track")
    parser.add_argument("--min-detection-confidence", type=float, default=0.5)
    parser.add_argument("--min-tracking-confidence", type=float, default=0.5)
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show the OpenCV preview window while processing",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detector = MediaPipeHandTracker(
        max_num_hands=args.max_num_hands,
        min_detection_confidence=args.min_detection_confidence,
        min_tracking_confidence=args.min_tracking_confidence,
    )
    logger = HandLogWriter(
        output_path=Path(args.log_path),
        summary_path=Path(args.summary_path) if args.summary_path else None,
    )
    visualizer = HandPreviewRenderer(window_name="Video Processing Preview") if args.preview else None
    stream = VideoFileStream(args.video_path)

    pipeline = VideoProcessingPipeline(
        video_stream=stream,
        detector=detector,
        logger=logger,
        visualizer=visualizer,
    )
    try:
        pipeline.run()
    except VideoFileOpenError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
