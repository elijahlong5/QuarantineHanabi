from django.contrib import admin

from game import models


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    fields = ("lobby", "is_in_progress", "created_at", "updated_at")
    list_display = ("lobby", "is_in_progress", "created_at", "updated_at")
    list_filter = ("is_in_progress",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("lobby__code",)


@admin.register(models.Lobby)
class LobbyAdmin(admin.ModelAdmin):
    fields = ("code", "created_at", "updated_at")
    list_display = ("code", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("code",)


@admin.register(models.LobbyMember)
class LobbyMember(admin.ModelAdmin):
    autocomplete_fields = ("lobby",)
    fields = ("lobby", "name", "is_owner", "created_at", "updated_at")
    list_display = (
        "name",
        "lobby",
        "is_owner",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_owner",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("lobby__code", "name")


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("game", "lobby_member")
    fields = ("game", "lobby_member", "order", "created_at", "updated_at")
    list_display = (
        "lobby_member",
        "game",
        "order",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("game__lobby_member__lobby__code", "lobby_member__name")
