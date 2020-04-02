from django.shortcuts import render, redirect, get_object_or_404
from game.forms import CreateLobbyForm, JoinLobbyForm
from game import models


def main(request):
    forms = {
        "create_lobby_form": CreateLobbyForm(),
        "join_lobby_form": JoinLobbyForm(),
    }
    return render(request, "game/main.html", forms)


def lobby(request, access_code, lobby_member):
    return render(
        request,
        "game/lobby.html",
        {"access_code": access_code, "lobby_member": lobby_member},
    )


def game_in_session(request, access_code, player_name):
    lobby = get_object_or_404(models.Lobby, code=access_code)
    game = models.Game.objects.get(lobby=lobby)
    return render(
        request,
        "game/game-in-session.html",
        {
            "access_code": access_code,
            "player_name": player_name,
            "game_code": game.id,
        },
    )


def create_lobby(request):
    if request.method == "POST":
        form = CreateLobbyForm(request.POST)
        if form.is_valid():
            lobby_member = form.save()
            url = f"/lobby/{lobby_member.lobby.code}/{lobby_member.name}/"
            return redirect(url)
    return redirect("/")


def join_lobby(request):
    if request.method == "POST":
        form = JoinLobbyForm(request.POST)
        if form.is_valid():
            lobby_member = form.save()
            url = f"/lobby/{lobby_member.lobby.code}/{lobby_member.name}/"
            return redirect(url)
    return redirect("/")


def start_game(request):
    if request.method == "POST":
        code = request.POST.get("access_code")
        player_name = request.POST.get("lobby_member_name")
        lobby = get_object_or_404(models.Lobby, code=code)
        if not models.Game.objects.filter(lobby=lobby).exists():
            models.Game.create_from_lobby(lobby)
        return redirect(f"/game-in-session/{lobby.code}/{player_name}/")
