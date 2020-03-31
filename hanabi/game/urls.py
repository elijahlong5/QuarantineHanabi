from django.urls import include, path
from game import views


urlpatterns = [
  path("api/", include("game.api.urls")),  
  path("", views.main),
    path("lobby/<access_code>/<lobby_member>/", views.lobby),
    path("create-lobby/", views.create_lobby),
    path("join-lobby/", views.join_lobby),
]

