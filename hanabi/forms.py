import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from hanabi.validators import (
    ValidAccessToken,
    ValidAsciiValues,
    ValidUnclaimedUsername,
)


class CreateLobbyForm(FlaskForm):
    """
    Form for creating a new lobby.
    """

    name = wtforms.StringField(
        "Name", validators=[DataRequired(), ValidAsciiValues()]
    )


class JoinLobbyForm(FlaskForm):
    access_token = wtforms.StringField(
        "Access Token", validators=[DataRequired(), ValidAccessToken()]
    )
    name = wtforms.StringField(
        "Name",
        validators=[
            DataRequired(),
            ValidAsciiValues(),
            ValidUnclaimedUsername(),
        ],
    )
