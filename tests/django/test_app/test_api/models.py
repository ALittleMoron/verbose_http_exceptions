from django.db import models


class ForeignModel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:  # noqa: D105
        return self.name


class TestModel(models.Model):
    name = models.CharField(max_length=128)
    foreign = models.ForeignKey(
        ForeignModel,
        related_name="foreign",
        related_query_name="tests",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:  # noqa: D105
        return self.name
