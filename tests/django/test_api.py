from typing import TYPE_CHECKING, Any

import pytest
from django.db import connection

from verbose_http_exceptions import status

if TYPE_CHECKING:
    from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


class TestAPI:
    @pytest.fixture(autouse=True)
    def before_start(
        self,
        test_client: "APIClient",
        auth_header: str,
    ) -> None:
        self.test_client = test_client
        self.auth_header = auth_header

    def test_api_not_found(
        self,
    ) -> None:
        response = self.test_client.get('/test/152126216')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "code": "client_error",
            "type": "not_found",
            "message": "Entity not found.",
            "location": None,
            "attr": None,
        }

    def test_api_permission_denied(
        self,
    ) -> None:
        response = self.test_client.get("/denied", HTTP_AUTHORIZATION=self.auth_header)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "code": "client_error",
            "type": "forbidden",
            "message": "Permission denied.",
            "location": None,
            "attr": None,
        }
