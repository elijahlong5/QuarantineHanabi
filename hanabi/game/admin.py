from django.contrib import admin

from game import models


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
