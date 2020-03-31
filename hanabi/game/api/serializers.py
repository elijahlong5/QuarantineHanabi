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


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "order")
        model = models.Player
        read_only_fields = fields


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "is_in_progress", "players")
        model = models.Game
        read_only_fields = fields

    def create(self, validated_data):
        return models.Game.create_from_lobby(**validated_data)
