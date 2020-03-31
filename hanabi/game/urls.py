from django.urls import path
from game import views

urlpatterns = [
    path("", views.main),
    path("lobby/<access_code>/<lobby_member>/", views.lobby),
    path("create-lobby/", views.create_lobby),
    path("join-lobby/", views.join_lobby),
]
