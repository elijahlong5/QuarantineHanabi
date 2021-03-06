# Generated by Django 3.0.4 on 2020-03-29 21:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0002_lobbymember"),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                    "is_in_progress",
                    models.BooleanField(verbose_name="in progress"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="updated at"
                    ),
                ),
                (
                    "lobby",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games",
                        related_query_name="game",
                        to="game.Lobby",
                        verbose_name="lobby",
                    ),
                ),
            ],
            options={
                "verbose_name": "game",
                "verbose_name_plural": "games",
                "ordering": ("created_at",),
            },
        ),
    ]
