from typing import Any

from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "EXCEPTIONS_HOG", None)

DEFAULTS: dict[str, Any] = {
    "ENABLE_IN_DEBUG": False,
    "NESTED_KEY_SEPARATOR": "__",
    "SUPPORT_MULTIPLE_EXCEPTIONS": False,
}

IMPORT_STRINGS = ("EXCEPTION_REPORTING",)

api_settings: APISettings = APISettings(
    USER_SETTINGS,
    DEFAULTS,  # type: ignore[reportArgumentType]
    IMPORT_STRINGS,
)
