from rest_framework import generics

from game.api import serializers


class LobbyCreateView(generics.CreateAPIView):
    serializer_class = serializers.LobbySerializer
