from django.contrib import admin
from django.urls import path
from game import views

from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("", include("game.urls"))]
