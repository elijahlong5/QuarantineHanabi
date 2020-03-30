from django.shortcuts import get_object_or_404
from rest_framework import generics

from game import models
from game.api import serializers


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
