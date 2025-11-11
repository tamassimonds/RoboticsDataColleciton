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

## Project layout
- `main.py` – CLI entrypoint for realtime hand detection.
- `roboticsdatacolleciton/`
  - `config.py` – shared dataclasses for runtime configuration.
  - `types.py` – strongly-typed objects for detected landmarks.
  - `video/` – camera capture abstractions.
  - `detection/` – MediaPipe-backed detectors.
  - `pipelines/` – orchestration logic (currently realtime only).
  - `batch/` – placeholder for future batch import/processing modules.
  - `storage/` – placeholder for storage backends (S3, local disk, etc.).

## Future roadmap
The folder structure leaves room for:
- Batch ingestion of large video collections (local or remote).
- Export of detection results to persistent storage (S3, databases, etc.).
- Reusable processing pipelines that share detectors, IO, and analytics stages.
