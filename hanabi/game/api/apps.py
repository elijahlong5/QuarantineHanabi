from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class APIConfig(AppConfig):
    name = "game.api"
    label = "game_api"
    verbose_name = _("Game API")
