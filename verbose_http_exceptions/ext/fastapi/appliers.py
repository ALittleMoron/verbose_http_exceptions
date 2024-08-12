from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from verbose_http_exceptions.exc import BaseVerboseHTTPException
from verbose_http_exceptions.ext.fastapi.handlers import (
    any_exception_handler,
    any_http_exception_handler,
    verbose_http_exception_handler,
    verbose_request_validation_error_handler,
)
from verbose_http_exceptions.ext.fastapi.openapi_override import override_422_error


def apply_verbose_http_exception_handler(app: FastAPI) -> FastAPI:
    """Apply verbose_http_exception_handler on given FastAPI instance."""
    app.add_exception_handler(
        BaseVerboseHTTPException,
        verbose_http_exception_handler,  # type: ignore[reportArgumentType]
    )
    return app


def apply_any_http_exception_handler(app: FastAPI) -> FastAPI:
    """Apply any_http_exception_handler on given FastAPI instance."""
    app.add_exception_handler(
        HTTPException,
        any_http_exception_handler,  # type: ignore[reportArgumentType]
    )
    return app


def apply_verbose_request_validation_error_handler(
    app: FastAPI,
    *,
    override_422_openapi: bool = True,
) -> FastAPI:
    """Apply verbose_request_validation_error_handler on given FastAPI instance."""
    app.add_exception_handler(
        RequestValidationError,
        verbose_request_validation_error_handler,  # type: ignore[reportArgumentType]
    )
    if override_422_openapi:  # pragma: no coverage
        override_422_error(app)
    return app


def apply_all_handlers(app: FastAPI, *, override_422_openapi: bool = True) -> FastAPI:
    """Apply all exception handlers on given FastAPI instance."""
    app.add_exception_handler(
        Exception,
        any_exception_handler,  # type: ignore[reportArgumentType]
    )
    if override_422_openapi:  # pragma: no coverage
        override_422_error(app)
    return app
