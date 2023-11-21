from django.db import models
from django.contrib.auth import get_user_model

import uuid


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    name = models.CharField(max_length=30)


class Message(models.Model):
    isHuman = models.BooleanField(default=False)
    text = models.CharField(default="")
    context = models.CharField(default="")
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-createdAt"])]
