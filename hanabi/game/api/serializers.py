from rest_framework import serializers

from game import models


class LobbyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = models.LobbyMember


class LobbySerializer(serializers.ModelSerializer):
    members = LobbyMemberSerializer(many=True, read_only=True)

    class Meta:
        fields = ("code", "id", "members")
        model = models.Lobby
        read_only_fields = ("code", "id")
