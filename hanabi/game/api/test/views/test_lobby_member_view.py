import pytest
import requests
from rest_framework import status

from game import models


@pytest.mark.integration
def test_create_lobby_member(live_server):
    lobby = models.Lobby.objects.create()
    data = {
        "name": "John",
    }

    response = requests.post(
        f"{live_server}/api/lobbies/{lobby.code}/members/", json=data
    )
    assert response.status_code == status.HTTP_201_CREATED

    member = response.json()

    assert member["name"] == data["name"]


@pytest.mark.integration
def test_list_lobby_members(live_server):
    lobby = models.Lobby.objects.create()
    john = lobby.members.create(name="John")
    jim = lobby.members.create(name="Jim")

    response = requests.get(f"{live_server}/api/lobbies/{lobby.code}/members/")
    assert response.status_code == status.HTTP_200_OK

    members = response.json()

    assert_lobby_member_in_list(john, members)
    assert_lobby_member_in_list(jim, members)


def assert_lobby_member_in_list(member, members):
    for found_member in members:
        if member.name == found_member["name"]:
            return

    assert False, f"Failed to find {member} in {members}"
