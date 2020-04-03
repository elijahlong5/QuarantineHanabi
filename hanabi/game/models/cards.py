import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Card(models.Model):
    BLUE = "BLUE"
    GREEN = "GREEN"
    RAINBOW = "RAINBOW"
    RED = "RED"
    WHITE = "WHITE"
    YELLOW = "YELLOW"

    COLOR_CHOICES = (
        (BLUE, _("Blue")),
        (GREEN, _("Green")),
        (RAINBOW, _("Rainbow")),
        (RED, _("Red")),
        (WHITE, _("White")),
        (YELLOW, _("Yellow")),
    )

    color = models.CharField(
        choices=COLOR_CHOICES, max_length=7, verbose_name=_("color"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    deck_order = models.PositiveSmallIntegerField(
        null=False, verbose_name=_("deck order")
    )
    game = models.ForeignKey(
        "Game",
        null=False,
        on_delete=models.CASCADE,
        related_name="cards",
        related_query_name="card",
        verbose_name=_("game"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    number = models.PositiveSmallIntegerField(
        null=False, verbose_name=_("number")
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=False, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("game", "deck_order")
        unique_together = ("deck_order", "game")
        verbose_name = _("card")
        verbose_name_plural = _("cards")
