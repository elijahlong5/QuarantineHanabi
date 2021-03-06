# Generated by Django 3.0.4 on 2020-03-29 21:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0003_game"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created at"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(verbose_name="order"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="players",
                        related_query_name="player",
                        to="game.Game",
                        verbose_name="game",
                    ),
                ),
                (
                    "lobby_member",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="game.LobbyMember",
                        verbose_name="lobby member",
                    ),
                ),
            ],
            options={
                "verbose_name": "player",
                "verbose_name_plural": "players",
                "ordering": ("created_at",),
            },
        ),
    ]
