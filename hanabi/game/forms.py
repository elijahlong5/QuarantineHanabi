from django import forms
from game import models


class CreateLobbyForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)

    def save(self):
        name = self.cleaned_data["name"]
        lobby = models.Lobby.objects.create()
        lobby_member = models.LobbyMember.objects.create(
            lobby=lobby, name=name
        )
        return lobby_member


class JoinLobbyForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    access_code = forms.CharField(label="Access Code", max_length=5)

    def clean_access_code(self):
        access_code = self.cleaned_data["access_code"]
        if not models.Lobby.objects.filter(code=access_code).exists():
            raise forms.ValidationError("Invalid access code.")
        return access_code

    def clean(self):
        cleaned_data = super().clean()
        access_code = cleaned_data.get("access_code")
        if not access_code:
            raise forms.ValidationError("Invalid access code.")
        name = cleaned_data.get("name")
        lobby = models.Lobby.objects.get(code=access_code)
        if models.LobbyMember.objects.filter(lobby=lobby, name=name).exists():
            raise forms.ValidationError("Name already taken.")

    def save(self):
        access_code = self.cleaned_data["access_code"]
        lobby = models.Lobby.objects.get(code=access_code)
        name = self.cleaned_data["name"]
        lobby_member = models.LobbyMember.objects.create(
            lobby=lobby, name=name
        )
        return lobby_member
