from django.urls import include, path
from game import views

urlpatterns = [path("api/", include("game.api.urls")), path("", views.main)]
