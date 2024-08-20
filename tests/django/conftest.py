import base64
import uuid

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def test_client(db: None) -> APIClient:
    return APIClient()


@pytest.fixture
def auth_header(db: None) -> str:
    username = uuid.uuid4().hex
    password = "password"  # noqa: S105
    get_user_model().objects._create_user(  # type: ignore[reportUnknownMemberType]  # noqa: SLF001
        username=f"user_{username}",
        email=f"{username}@example.com",
        password=password,
    )
    return f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}'
