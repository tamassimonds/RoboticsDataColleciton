"""Columnar logging of detected hand positions."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Sequence

import json

import pyarrow as pa
import pyarrow.parquet as pq

from roboticsdatacolleciton.types import HandPosition


@dataclass
class HandLogWriter:
    """Streams detections to a Parquet file and frame counts to JSON."""

    output_path: str | Path
    summary_path: str | Path | None = None

    _schema: pa.Schema = field(init=False, repr=False)
    _writer: pq.ParquetWriter | None = field(init=False, default=None, repr=False)
    _frame_counts: List[dict] = field(init=False, default_factory=list, repr=False)

    def __post_init__(self) -> None:
        self.output_path = Path(self.output_path)
        if self.summary_path is None:
            self.summary_path = self.output_path.with_suffix(".summary.json")
        self.summary_path = Path(self.summary_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.summary_path.parent.mkdir(parents=True, exist_ok=True)

        landmark_struct = pa.struct(
            [
                ("name", pa.string()),
                ("x", pa.float32()),
                ("y", pa.float32()),
                ("z", pa.float32()),
            ]
        )
        self._schema = pa.schema(
            [
                ("frame_index", pa.int32()),
                ("hand_index", pa.int16()),
                ("label", pa.string()),
                ("confidence", pa.float32()),
                ("palm_normalized", pa.list_(pa.float32(), 2)),
                ("palm_pixel", pa.list_(pa.float32(), 2)),
                ("landmarks", pa.list_(landmark_struct)),
            ]
        )

    def record(self, frame_index: int, positions: Sequence[HandPosition]) -> None:
        self._frame_counts.append({"frame_index": frame_index, "hand_count": len(positions)})
        if not positions:
            return

        rows = []
        for hand_idx, position in enumerate(positions):
            rows.append(
                {
                    "frame_index": frame_index,
                    "hand_index": hand_idx,
                    "label": position.label,
                    "confidence": float(position.confidence),
                    "palm_normalized": [float(position.normalized_palm[0]), float(position.normalized_palm[1])],
                    "palm_pixel": [float(position.pixel_palm[0]), float(position.pixel_palm[1])],
                    "landmarks": [
                        {
                            "name": lm.name,
                            "x": float(lm.x),
                            "y": float(lm.y),
                            "z": float(lm.z) if lm.z is not None else float("nan"),
                        }
                        for lm in position.landmarks
                    ],
                }
            )

        self._write_rows(rows)

    def close(self) -> None:
        if self._writer:
            self._writer.close()
            self._writer = None
        with self.summary_path.open("w", encoding="utf-8") as fp:
            json.dump({"frames": self._frame_counts}, fp, indent=2)

    def _write_rows(self, rows: List[dict]) -> None:
        table = pa.Table.from_pylist(rows, schema=self._schema)
        if self._writer is None:
            self._writer = pq.ParquetWriter(str(self.output_path), self._schema)
        self._writer.write_table(table)
