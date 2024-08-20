from typing import Any

from rest_framework import serializers

from .models import ForeignModel, TestModel


class TestSerializer(serializers.ModelSerializer):  # noqa: D101
    class Meta:  # type: ignore[reportIncompatibleVariableOverride]  # noqa: D106
        model = TestModel
        fields = (
            "id",
            "name",
        )


class ForeignSerializer(serializers.ModelSerializer):  # noqa: D101
    tests = TestSerializer(many=True)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]  # noqa: D106
        model = ForeignModel
        fields = (
            "name",
            "tests",
        )

    def create(self, validated_data: dict[str, Any]) -> None:  # noqa: D102
        for hedgehog in validated_data["tests"]:
            nested_serializer = TestSerializer(data=hedgehog)
            nested_serializer.is_valid(raise_exception=True)
            nested_serializer.save()
