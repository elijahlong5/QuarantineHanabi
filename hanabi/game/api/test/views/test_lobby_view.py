import pytest
import requests
from rest_framework import status


@pytest.mark.integration
def test_create_lobby(live_server):
    data = {"name": "John"}

    response = requests.post(f"{live_server}/api/lobbies/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    lobby = response.json()

    assert lobby["code"]
    assert lobby["id"]
