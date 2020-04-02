from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import generics, serializers as drf_serializers

from game import models
from game.api import serializers


class GameDetailView(generics.RetrieveAPIView):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameStateSerializer

    def get_serializer_context(self):
        """
        Associate the requesting player with the serializer.

        Returns:
            A dictionary containing the context passed to the view's
            serializer.
        """
        context = super().get_serializer_context()
        print("requesting game state")

        player_name = self.request.query_params.get("as_player")
        if player_name is None:
            raise drf_serializers.ValidationError(
                {"as_player": _("This field is required.")}
            )

        game = self.get_object()
        try:
            player = game.players.get(lobby_member__name=player_name)
        except models.Player.DoesNotExist:
            raise drf_serializers.ValidationError(
                {"as_player": _("Invalid player name.")}
            )

        context["for_player"] = player

        return context


class GameListCreateView(generics.CreateAPIView):
    serializer_class = serializers.GameSerializer

    def perform_create(self, serializer):
        lobby = get_object_or_404(models.Lobby, code=self.kwargs.get("code"))
        serializer.save(lobby=lobby)


class LobbyCreateView(generics.CreateAPIView):
    serializer_class = serializers.LobbySerializer


class LobbyMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.LobbyMemberSerializer

    def get_object(self):
        """
        Returns:
            The lobby whose code is provided in the URL.
        """
        return get_object_or_404(models.Lobby, code=self.kwargs.get("code"))

    def get_queryset(self):
        """
        Get the members of the lobby specified in the URL.

        Returns:
            A queryset containing the lobby members of the lobby whose
            code is given in the URL.
        """
        return self.get_object().members

    def perform_create(self, serializer):
        """
        Associate the lobby whose code is provided in the URL with the
        new lobby member.

        Args:
            serializer:
                The serializer containing the new member's information.
        """
        lobby = self.get_object()
        serializer.save(lobby=lobby)
