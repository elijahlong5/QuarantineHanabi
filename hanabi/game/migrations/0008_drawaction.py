# Generated by Django 3.0.4 on 2020-03-29 22:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0007_discardaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="DrawAction",
            fields=[
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
                    "action",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draw_action",
                        to="game.Action",
                        verbose_name="action",
                    ),
                ),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="game.Card",
                        verbose_name="card",
                    ),
                ),
            ],
            options={
                "verbose_name": "draw action",
                "verbose_name_plural": "draw actions",
                "order_with_respect_to": "action",
            },
        ),
    ]