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


class GameStateSerializer(serializers.ModelSerializer):
    active_player = serializers.CharField(
        read_only=True, source="active_player.name"
    )
    discards = GameStateCardSerializer(many=True, read_only=True)
    players = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "active_player",
            "discards",
            "id",
            "is_in_progress",
            "piles",
            "players",
            "remaining_bombs",
            "remaining_cards",
            "remaining_hints",
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


class HintActionSerializer(serializers.ModelSerializer):
    target_player_name = serializers.CharField(source="target_player.name")

    class Meta:
        fields = ("color", "number", "target_player_name")
        model = models.HintAction

    def validate(self, attrs):
        """
        Ensure that either a color or number has been provided, but not
        both.

        Args:
            attrs:
                The serializer data to validate.

        Returns:
            The validated data.
        """
        if "color" in attrs and "number" in attrs:
            raise serializers.ValidationError(
                gettext("A hint may not specify both a color and number.")
            )

        if "color" not in attrs and "number" not in attrs:
            raise serializers.ValidationError(
                gettext("A hint must specify a color or a number.")
            )

        return attrs


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
    hint_action = HintActionSerializer(required=False)
    play_action = PlayActionSerializer(required=False)
    player_name = serializers.CharField(source="player.name")

    class Meta:
        fields = (
            "action_type",
            "created_at",
            "hint_action",
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

        if action_type == models.Action.HINT:
            hint_action = validated_data.pop("hint_action", {})

            target_player = self.context["game"].players.get(
                lobby_member__name=hint_action["target_player"]["name"]
            )

            hint_info = {}
            if "color" in hint_action:
                hint_info["color"] = hint_action["color"]
            else:
                hint_info["number"] = hint_action["number"]

            models.HintAction.objects.create(
                action=action, target_player=target_player, **hint_info
            )

        elif action_type == models.Action.PLAY:
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

            if self.context["game"].remaining_cards > 0:
                self._player.give_card(
                    self.context["game"].draw_card(self._player)
                )

        return action

    def validate(self, attrs):
        action_type_name = attrs.get("action_type")
        action_type = self.ACTION_NAME_TO_INTERNAL_REP_MAP[action_type_name]
        if action_type in models.Action.TURN_ACTION_TYPES:
            if not self.context["game"].is_players_turn(self._player):
                raise serializers.ValidationError(
                    gettext("It is not your turn.")
                )

            if action_type == models.Action.HINT:
                if self.context["game"].remaining_hints <= 0:
                    raise serializers.ValidationError(
                        gettext("No hints remaining.")
                    )

                hint_action = attrs.get("hint_action", {})
                target_player_name = hint_action.get("target_player", {}).get(
                    "name"
                )

                if (
                    not self.context["game"]
                    .players.exclude(pk=self._player.pk)
                    .filter(lobby_member__name=target_player_name)
                    .exists()
                ):
                    raise serializers.ValidationError(
                        gettext("Invalid target player.")
                    )

            elif action_type == models.Action.PLAY:
                play_action = attrs.get("play_action", {})
                card = play_action.get("card_id")

                if card not in self._player.cards:
                    raise serializers.ValidationError(
                        gettext(
                            "The specified card does not exist in your hand."
                        )
                    )

        return attrs

    def validate_player_name(self, name):
        try:
            self._player = models.Player.objects.get(
                game=self.context["game"], lobby_member__name=name
            )
        except models.Player.DoesNotExist:
            raise serializers.ValidationError(gettext("Invalid player name."))

        return name
