from django.shortcuts import render


def main(request):
    return render(request, "game/main.html")


def lobby(request):
    return render(request, "game/lobby.html")


def game_in_session(request):
    return render(request, "game/game-in-session.html")
