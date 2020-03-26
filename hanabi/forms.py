import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from hanabi.validators import ValidAccessToken


class CreateLobbyForm(FlaskForm):
    """
    Form for creating a new lobby.
    """

    name = wtforms.StringField("Name", validators=[DataRequired()])


class JoinLobbyForm(FlaskForm):
    access_token = wtforms.StringField(
        "Access Token", validators=[DataRequired(), ValidAccessToken()]
    )
    name = wtforms.StringField("Name", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lobbies = None

    def validate(self, lobbies):
        # Cache the lobbies on the form so that the access token
        # validator can get them.
        self.lobbies = lobbies

        return super().validate()
