from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class NoPermission(permissions.BasePermission):
    message = "You are not allowed to do this!"

    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        return False
