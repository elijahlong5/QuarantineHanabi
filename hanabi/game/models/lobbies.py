import random
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from game.models import Game


LOBBY_CODE_LENGTH = 5


def generate_lobby_code():
    # ASCII letters and digits with ambiguous characters removed.
    characters = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

    return "".join(random.choices(characters, k=LOBBY_CODE_LENGTH))


class Lobby(models.Model):
    """
    A lobby is a collection of a group of members who will participate
    in games together. Lobbies are gated behind randomly generated
    access codes.
    """

    code = models.CharField(
        default=generate_lobby_code,
        max_length=LOBBY_CODE_LENGTH,
        unique=True,
        verbose_name=_("access code"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("lobby")
        verbose_name_plural = _("lobbies")

    @property
    def has_active_game(self):
        return Game.objects.filter(lobby=self).exists()


class LobbyMember(models.Model):
    """
    A lobby member has either created the lobby or joined the lobby
    using its access code. All members of the lobby become players in a
    game started from the lobby.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, null=False, verbose_name=_("created at")
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name=_("ID")
    )
    is_owner = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the member is the owner of the lobby. "
            "The lobby owner has additional permissions such as being able to "
            "delete the lobby."
        ),
        null=False,
        verbose_name=_("is owner"),
    )
    lobby = models.ForeignKey(
        "Lobby",
        null=False,
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="member",
        verbose_name=_("lobby"),
    )
    name = models.SlugField(blank=False, null=False, verbose_name=_("name"))
    updated_at = models.DateTimeField(
        auto_now=True, null=False, verbose_name=_("updated at")
    )

    class Meta:
        ordering = ("created_at",)
        unique_together = ("lobby", "name")
        verbose_name = _("lobby member")
        verbose_name_plural = _("lobby members")
