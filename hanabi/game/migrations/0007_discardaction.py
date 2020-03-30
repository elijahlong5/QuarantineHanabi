# Generated by Django 3.0.4 on 2020-03-29 22:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0006_action"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscardAction",
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
                        related_name="discard_action",
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
                "verbose_name": "discard action",
                "verbose_name_plural": "discard actions",
                "order_with_respect_to": "action",
            },
        ),
    ]