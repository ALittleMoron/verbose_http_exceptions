from typing import TYPE_CHECKING, Any

from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from verbose_http_exceptions import error_by_status_mapping, status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException

if TYPE_CHECKING:
    from rest_framework.request import Request


def get_status_from_exception(exc: Exception) -> int:
    if isinstance(exc, APIException | BaseVerboseHTTPException):
        return exc.status_code
    if isinstance(exc, Http404):
        return status.HTTP_404_NOT_FOUND
    if isinstance(exc, ProtectedError):
        return status.HTTP_409_CONFLICT
    if isinstance(exc, PermissionDenied):
        return status.HTTP_403_FORBIDDEN
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int):
        return status_code
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def exception_handler(exc: Exception, context: dict[str, Any] | None = None) -> Response | None:
    request: Request | None = context["request"] if context and "request" in context else None
    status_code = get_status_from_exception(exc)
    error = error_by_status_mapping.get(status_code)
    if error is None:
        return Response(status=status_code)
    response = error().as_dict()
    return Response(response, status=status_code)
