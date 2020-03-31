from django.http import JsonResponse
from django.shortcuts import render, redirect
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


def game_in_session(request):
    return render(request, "game/game-in-session.html")


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


def get_lobby_members(request, code):
    lobby = models.Lobby.objects.get(code=code)
    lobby_members = models.LobbyMember.objects.filter(lobby=lobby).values(
        "name"
    )
    return JsonResponse(list(lobby_members), safe=False)
