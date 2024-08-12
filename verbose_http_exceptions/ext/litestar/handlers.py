from typing import Any

from dev_utils.guards import all_dict_keys_are_str
from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException, ValidationException

from verbose_http_exceptions import error_by_status_mapping, status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException, VerboseHTTPExceptionDict
from verbose_http_exceptions.exc.server_error import InternalServerErrorHTTPException
from verbose_http_exceptions.ext.litestar.exc import (
    RequestValidationHTTPExceptionWithNestedErrors,
    ValidationHTTPException,
)


async def verbose_http_exception_handler(
    _: "Request[Any, Any, Any]",
    exc: "BaseVerboseHTTPException",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle verbose HTTP exception output.

    Handle only BaseVerboseHTTPException inherited instances. For handling all exceptions use
    ``any_http_exception_handler``.
    """
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=exc.status_code,
        content=exc.as_dict(),
        headers=exc.headers,
    )


async def verbose_request_validation_error_handler(
    _: "Request[Any, Any, Any]",
    exc: "ValidationException",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle ValidationException to override 400 error."""
    nested_errors: list[ValidationHTTPException] = []
    errors = exc.extra
    if errors is None:
        return Response["VerboseHTTPExceptionDict"](
            media_type=MediaType.JSON,
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ValidationHTTPException(message=exc.detail).as_dict(),
            headers=exc.headers,
        )
    if isinstance(errors, dict):
        errors = [errors]
    if len(errors) == 1:  # pragma: no coverage
        error = errors[0]
        return Response(
            media_type=MediaType.JSON,
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ValidationHTTPException().as_dict(),
            headers=exc.headers,
        )
    for error in errors:
        if not isinstance(error, dict):  # pragma: no cover
            continue
        if not all_dict_keys_are_str(error):  # type: ignore[reportUnknownArgumentType] # pragma: no cover
            continue
        error_instance = ValidationHTTPException(
            type_=error.get("type") or "not_known_type",
            message=error.get("message") or "not_known_message",
            location=error.get("source"),
            attr_name=error.get("key"),
        )
        nested_errors.append(error_instance)
    main_error = RequestValidationHTTPExceptionWithNestedErrors(*nested_errors)
    return Response(
        media_type=MediaType.JSON,
        status_code=main_error.status_code,
        content=main_error.as_dict(),
        headers=exc.headers,
    )


async def any_http_exception_handler(
    _: "Request[Any, Any, Any]",
    exc: "HTTPException",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle any HTTPException errors (BaseVerboseHTTPException too).

    Doesn't handle 422 request error well. Use ``verbose_request_validation_error_handler`` for it.
    """
    class_ = error_by_status_mapping.get(exc.status_code)
    if class_ is None:
        raise exc
    content = class_(message=exc.detail).as_dict()
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


async def any_exception_handler(
    request: "Request[Any, Any, Any]",
    exc: "Exception",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle any exception."""
    if isinstance(exc, BaseVerboseHTTPException):
        return await verbose_http_exception_handler(request, exc)
    if isinstance(exc, ValidationException):
        return await verbose_request_validation_error_handler(request, exc)
    if isinstance(exc, HTTPException):
        return await any_http_exception_handler(request, exc)
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=InternalServerErrorHTTPException(message=str(exc)).as_dict(),
    )
