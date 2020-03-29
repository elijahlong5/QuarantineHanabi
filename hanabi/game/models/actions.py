import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Action(models.Model):
    DISCARD = 1
    DRAW = 2
    HINT = 3
    ORDER_HAND = 4
    PLAY = 5

    TYPE_CHOICES = (
        (DISCARD, _("Discard")),
        (DRAW, _("Draw")),
        (HINT, _("Hint")),
        (ORDER_HAND, _("Order Hand")),
        (PLAY, _("Play")),
    )

    action_type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES, null=False, verbose_name=_("action type")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    game = models.ForeignKey(
        "Game",
        null=False,
        on_delete=models.CASCADE,
        related_name="actions",
        related_query_name="action",
        verbose_name=_("game"),
    )
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="actions",
        related_query_name="action",
        verbose_name=_("player"),
    )

    class Meta:
        ordering = ("game", "created_at")
        unique_together = ("created_at", "game")
        verbose_name = _("action")
        verbose_name_plural = _("actions")
