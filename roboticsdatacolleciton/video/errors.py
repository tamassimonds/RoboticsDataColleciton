"""Video-specific exception types."""


class CameraOpenError(RuntimeError):
    """Raised when cv2 fails to open the requested camera device."""

    def __init__(self, device_index: int) -> None:
        super().__init__(f"Unable to open camera index {device_index}")
        self.device_index = device_index
