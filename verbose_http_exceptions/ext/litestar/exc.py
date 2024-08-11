from verbose_http_exceptions.exc import UnprocessableContentHTTPException


class ValidationHTTPException(UnprocessableContentHTTPException):
    """Override for UnprocessableContentHTTPException but with code = 'validation_error'."""

    code = "validation_error"
