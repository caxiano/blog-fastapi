
from http import HTTPStatus


class NotFoundPostError(Exception):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found", status_code: int = HTTPStatus.NOT_FOUND) -> None:
        self.message = message
        self.status_code = status_code