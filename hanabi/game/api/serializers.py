from django.utils.translation import gettext_lazy as _, gettext
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


class PlayActionSerializer(serializers.ModelSerializer):
    card = GameStateCardSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Card.objects.all(), write_only=True
    )

    class Meta:
        fields = ("card", "card_id", "was_successful")
        model = models.PlayAction
        read_only_fields = ("was_successful",)


class ActionSerializer(serializers.ModelSerializer):
    DISCARD = "DISCARD"
    DRAW = "DRAW"
    HINT = "HINT"
    ORDER_HAND = "ORDER_HAND"
    PLAY = "PLAY"

    ACTION_NAME_TO_INTERNAL_REP_MAP = {
        DISCARD: models.Action.DISCARD,
        DRAW: models.Action.DRAW,
        HINT: models.Action.HINT,
        ORDER_HAND: models.Action.ORDER_HAND,
        PLAY: models.Action.PLAY,
    }

    type_choices = (
        (DISCARD, _("Discard")),
        (DRAW, _("Draw")),
        (HINT, _("Hint")),
        (ORDER_HAND, _("ORDER_HAND")),
        (PLAY, _("Play")),
    )

    action_type = serializers.ChoiceField(choices=type_choices)
    play_action = PlayActionSerializer()
    player_name = serializers.CharField(source="player.name")

    class Meta:
        fields = (
            "action_type",
            "created_at",
            "id",
            "play_action",
            "player_name",
        )
        model = models.Action
        read_only_fields = ("created_at", "id")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._player = None

    def create(self, validated_data):
        action_type_name = validated_data.pop("action_type")
        action_type = self.ACTION_NAME_TO_INTERNAL_REP_MAP[action_type_name]

        action = models.Action.objects.create(
            action_type=action_type,
            game=self.context["game"],
            player=self._player,
        )

        if action_type == models.Action.PLAY:
            play_action = validated_data.pop("play_action", {})
            # card_id exposes itself as an ID but is represented in
            # Python as a full card object.
            card = play_action.pop("card_id")

            models.PlayAction.objects.create(
                action=action,
                card=card,
                was_successful=self.context["game"].is_playable(card),
            )
            action.player.remove_card(card, action)

        return action

    def validate_player_name(self, name):
        try:
            self._player = models.Player.objects.get(
                game=self.context["game"], lobby_member__name=name
            )
        except models.Player.DoesNotExist:
            raise serializers.ValidationError(gettext("Invalid player name."))

        return name
