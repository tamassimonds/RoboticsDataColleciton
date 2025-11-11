"""Shared dataclasses used across pipelines."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(slots=True)
class Landmark:
    """Single 3D landmark for a detected hand."""

    name: str
    x: float
    y: float
    z: float | None


@dataclass(slots=True)
class HandPosition:
    """Represents the inferred position of a single hand."""

    label: str
    confidence: float
    normalized_palm: tuple[float, float]
    pixel_palm: tuple[int, int]
    landmarks: Sequence[Landmark]
