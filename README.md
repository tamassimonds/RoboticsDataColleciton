# RoboticsDataColleciton

Realtime, modular hand-tracking utilities intended to grow into a richer robotics data collection toolkit.

## Getting started
1. Create a virtual environment (Python >= 3.12) and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. Run the realtime tracker (press `Ctrl+C` to stop):
   ```bash
   python main.py --device-index 0 --max-num-hands 2
   ```
   Optional arguments let you control resolution and MediaPipe confidence thresholds.
   The app opens a preview window with landmark overlays—press `q`/`Esc` to close it or pass `--no-preview` to disable the window.
   > On macOS you must grant the terminal camera access under **System Settings → Privacy & Security → Camera** the first time you run the app.
3. Preview detections on a recorded video (no logging):
   ```bash
   python preview.py --video-path data/videos/sample.mp4
   ```
4. Process a video and log detections to columnar storage:
   ```bash
   python process_video.py --video-path data/videos/sample.mp4 --log-path logs/sample.parquet
   ```
   Add `--preview` to watch the overlay while the log is produced. The pipeline writes the detailed detections to the Parquet file and saves per-frame hand counts to `<log-path>.summary.json`.

## Project layout
- `main.py` – CLI entrypoint for realtime hand detection.
- `roboticsdatacolleciton/`
  - `config.py` – shared dataclasses for runtime configuration.
  - `types.py` – strongly-typed objects for detected landmarks.
  - `video/` – camera capture plus file-based video readers.
  - `detection/` – MediaPipe-backed detectors.
  - `visualization/` – OpenCV overlay rendering utilities.
  - `loggers/` – scalable writers for detection logs (Parquet + JSON summary).
  - `pipelines/` – orchestration logic for realtime and offline video workflows.
  - `batch/` – placeholder for future batch import/processing modules.
  - `storage/` – placeholder for storage backends (S3, local disk, etc.).
- `preview.py` – lightweight CLI to inspect detections on a video file.
- `process_video.py` – offline processor that logs every detected hand per frame.

Place raw footage under `data/videos/` (ignored by git) and direct logs to `logs/` or any other folder.

## Detection logs

`process_video.py` emits two artifacts:

1. **Parquet log** – each row represents a detected hand for a specific frame, including palm positions and 21 landmarks as a nested struct, making it efficient to query or load into Pandas/Arrow for downstream processing.
2. **Frame summary JSON** – stores the frame index and hand count for every frame, ensuring frames with zero detections are still represented.

The format is designed to stay compatible with future batch importers (e.g., multi-video ingestion or S3-backed workflows).

## Future roadmap
The folder structure leaves room for:
- Batch ingestion of large video collections (local or remote).
- Export of detection results to persistent storage (S3, databases, etc.).
- Reusable processing pipelines that share detectors, IO, and analytics stages.
