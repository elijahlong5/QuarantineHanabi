import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .cards import Card


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


class DiscardAction(models.Model):

    action = models.OneToOneField(
        "Action",
        on_delete=models.CASCADE,
        related_name="discard_action",
        verbose_name=_("action"),
    )
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("card"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )

    class Meta:
        order_with_respect_to = "action"
        verbose_name = _("discard action")
        verbose_name_plural = _("discard actions")


class DrawAction(models.Model):

    action = models.OneToOneField(
        "Action",
        on_delete=models.CASCADE,
        related_name="draw_action",
        verbose_name=_("action"),
    )
    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("card"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )

    class Meta:
        order_with_respect_to = "action"
        verbose_name = _("draw action")
        verbose_name_plural = _("draw actions")


class HintAction(models.Model):

    COLOR_CHOICES = (
        (Card.BLUE, _("Blue")),
        (Card.GREEN, _("Green")),
        (Card.RAINBOW, _("Rainbow")),
        (Card.RED, _("Red")),
        (Card.WHITE, _("White")),
        (Card.YELLOW, _("Yellow")),
    )

    action = models.OneToOneField(
        "Action",
        on_delete=models.CASCADE,
        related_name="hint_action",
        verbose_name=_("action"),
    )
    color = models.PositiveSmallIntegerField(
        choices=COLOR_CHOICES, null=True, verbose_name=_("color")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    number = models.PositiveSmallIntegerField(
        null=True, verbose_name=_("number")
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=Q(
                    (Q(color__isnull=False) & Q(number__isnull=True))
                    | (Q(color__isnull=True) & Q(number__isnull=False))
                ),
                name="cix_color_xor_number",
            ),
        )
        order_with_respect_to = "action"
        verbose_name = _("hint action")
        verbose_name_plural = _("hint actions")


class HintCard(models.Model):

    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="hint_cards",
        related_query_name="hint_card",
        verbose_name=_("card"),
    )
    hint = models.ForeignKey(
        "HintAction",
        on_delete=models.CASCADE,
        related_name="cards",
        related_query_name="card",
        verbose_name=_("hint"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )

    class Meta:
        unique_together = ("card", "hint")
        verbose_name = _("hint card")
        verbose_name_plural = _("hint cards")


class PlayAction(models.Model):

    action = models.OneToOneField(
        "Action",
        on_delete=models.CASCADE,
        related_name="play_action",
        verbose_name=_("action"),
    )
    card = models.OneToOneField(
        "Card",
        on_delete=models.CASCADE,
        related_name="play_action",
        verbose_name=_("card"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    was_successful = models.BooleanField(verbose_name=_("was successful"))

    class Meta:
        order_with_respect_to = "action"
        verbose_name = _("play action")
        verbose_name_plural = _("play actions")
