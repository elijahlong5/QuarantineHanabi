from django.urls import path

from game.api import views


urlpatterns = [
    path(
        "games/<uuid:pk>/", views.GameDetailView.as_view(), name="game-detail"
    ),
    path("lobbies/", views.LobbyCreateView.as_view(), name="lobby-list"),
    path(
        "lobbies/<code>/", views.LobbyDetailView.as_view(), name="detail-view",
    ),
    path(
        "lobbies/<code>/members/",
        views.LobbyMemberListCreateView.as_view(),
        name="lobby-member-list",
    ),
    path(
        "lobbies/<code>/games/",
        views.GameListCreateView.as_view(),
        name="game-list",
    ),
]
