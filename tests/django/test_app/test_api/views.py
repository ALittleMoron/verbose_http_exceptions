from typing import TYPE_CHECKING, Any

from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from .models import TestModel
from .permissions import NoPermission
from .serializers import ForeignSerializer, TestSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


ONE = 1
ZERO = 0


class TestView(ModelViewSet):
    serializer_class = TestSerializer
    queryset = TestModel.objects.all()


class NoPermissionView(ModelViewSet):
    serializer_class = TestSerializer
    queryset = TestModel.objects.all()
    permission_classes = (NoPermission,)


class ExceptionView(GenericAPIView):
    def post(self, request: "Request", *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401, ARG002
        """Sample view to raise unhandled exception."""
        exception_type: str = request.POST.get("type", "")

        if exception_type == "assertion_error":
            assert (
                ONE == ZERO
            ), "Set a custom message and make sure it isn't leaked in the response."
        elif exception_type == "arithmetic_error":
            return 1 / 0
        elif exception_type == "key_error":
            sample_dict = {"a": 1}
            sample_dict["b"]
        elif exception_type == "api_error":
            raise APIException
        elif exception_type == "nested_list_on_serializer":
            s = ForeignSerializer()
            s.create({"tests": [{"color": "red"}]})
        elif exception_type == "atomic_transaction":
            TestModel.objects.create(name="One")

            with transaction.atomic():
                TestModel.objects.create(name="Two")
                raise APIException

        msg = "Shouldn't be included in the response."
        raise Exception(msg)  # noqa: TRY002
