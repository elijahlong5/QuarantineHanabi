import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class Player(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    game = models.ForeignKey(
        "Game",
        null=False,
        on_delete=models.CASCADE,
        related_name="players",
        related_query_name="player",
        verbose_name=_("game"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    lobby_member = models.ForeignKey(
        "LobbyMember",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("lobby member"),
    )
    order = models.PositiveSmallIntegerField(
        null=False, verbose_name=_("order")
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=False, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("created_at",)
        unique_together = ("game", "order")
        verbose_name = _("player")
        verbose_name_plural = _("players")

    @property
    def name(self):
        if self.lobby_member:
            return self.lobby_member.name

        return ugettext("Player %d") % (self.order + 1)


class PlayerHand(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="hands",
        related_query_name="hand",
        verbose_name=_("player"),
    )
    source_action = models.OneToOneField(
        "Action",
        on_delete=models.CASCADE,
        related_name="resulting_hand",
        verbose_name=_("source action"),
    )

    class Meta:
        verbose_name = _("player hand")
        verbose_name_plural = _("player hands")


class PlayerHandCard(models.Model):

    card = models.ForeignKey(
        "Card",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("card"),
    )
    hand = models.ForeignKey(
        "PlayerHand",
        on_delete=models.CASCADE,
        related_name="cards",
        related_query_name="card",
        verbose_name=_("hand"),
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )

    class Meta:
        order_with_respect_to = "hand"
        verbose_name = _("player hand card")
        verbose_name_plural = _("player hand cards")
