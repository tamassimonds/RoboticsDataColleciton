"""Video-specific exception types."""


class CameraOpenError(RuntimeError):
    """Raised when cv2 fails to open the requested camera device."""

    def __init__(self, device_index: int) -> None:
        super().__init__(f"Unable to open camera index {device_index}")
        self.device_index = device_index


class VideoFileOpenError(RuntimeError):
    """Raised when a video file cannot be opened for decoding."""

    def __init__(self, path, reason: str | None = None) -> None:
        message = f"Unable to open video file: {path}"
        if reason:
            message = f"{message} ({reason})"
        super().__init__(message)
        self.path = path
        self.reason = reason
