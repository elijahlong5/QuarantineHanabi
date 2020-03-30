from django.urls import path

from game.api import views


urlpatterns = [
    path("lobbies/", views.LobbyCreateView.as_view(), name="lobby-list"),
    path(
        "lobbies/<code>/members/",
        views.LobbyMemberListCreateView.as_view(),
        name="lobby-member-list",
    ),
]
