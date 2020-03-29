import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Game(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    is_in_progress = models.BooleanField(
        null=False, verbose_name=_("in progress")
    )
    lobby = models.ForeignKey(
        "Lobby",
        null=False,
        on_delete=models.CASCADE,
        related_name="games",
        related_query_name="game",
        verbose_name=_("lobby"),
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=False, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("game")
        verbose_name_plural = _("games")
