from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from django.contrib.auth import get_user_model


class APIKey(AbstractAPIKey):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
