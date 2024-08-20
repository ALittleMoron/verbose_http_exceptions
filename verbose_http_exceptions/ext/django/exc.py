from verbose_http_exceptions.exc import ConflictHTTPException


class ProtectedObjectException(ConflictHTTPException):
    """Django DB ProtectedException verbose HTTP exception class."""

    type_: str = "protected_error"
    message = "Requested operation cannot be completed because a related object is protected."
