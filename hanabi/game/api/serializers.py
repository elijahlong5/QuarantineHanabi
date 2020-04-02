from rest_framework import serializers

from game import models


class LobbyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = models.LobbyMember


class LobbySerializer(serializers.ModelSerializer):
    members = LobbyMemberSerializer(many=True, read_only=True)

    class Meta:
        fields = ("code", "id", "members", "has_active_game")
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


class GameStateSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "is_in_progress",
            "players",
            "remaining_bombs",
            "remaining_cards",
        )
        model = models.Game
        read_only_fields = fields

    def get_players(self, game):
        for_player = self.context["for_player"]

        player_reps = []
        for player in game.players.order_by("order"):
            if player == for_player:
                serializer = GameStateOwnPlayerSerializer(instance=player)
            else:
                serializer = GameStatePlayerSerializer(instance=player)

            rep = serializer.data
            player_reps.append(rep)

        return player_reps


class GameStateCardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("color", "id", "number")
        model = models.Card
        read_only_fields = fields


class GameStatePlayerSerializer(serializers.ModelSerializer):
    cards = GameStateCardSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "cards", "name", "order")
        model = models.Player
        read_only_fields = fields


class GameStateOwnCardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id",)
        model = models.Card
        read_only_fields = fields


class GameStateOwnPlayerSerializer(serializers.ModelSerializer):
    cards = GameStateOwnCardSerializer(many=True, read_only=True)

    class Meta:
        fields = ("id", "cards", "name", "order")
        model = models.Player
        read_only_fields = fields
