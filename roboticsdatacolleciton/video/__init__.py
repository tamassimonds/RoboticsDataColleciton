"""Video and camera utilities."""

from .capture import CameraStream
from .errors import CameraOpenError

__all__ = ["CameraStream", "CameraOpenError"]
