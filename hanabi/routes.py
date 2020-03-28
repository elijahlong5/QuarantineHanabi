from flask import (
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from hanabi import app, forms
from hanabi.game import HanabiGame


hanabi_lobbies = {}

# Views
@app.route("/")
@app.route("/home/")
def main(create_form=None, join_form=None):
    create_form = create_form or forms.CreateLobbyForm(prefix="create-lobby-")
    join_form = join_form or forms.JoinLobbyForm(prefix="join-lobby-")

    return render_template(
        "main.html", create_form=create_form, join_form=join_form
    )


@app.route("/api/get-game-state/<access_code>/<player_id>/")
def get_game_state_api(access_code, player_id):
    if access_code not in hanabi_lobbies:
        abort(404)
    game_state = hanabi_lobbies[access_code].get_game_state(player_id)
    return jsonify(game_state)


@app.route("/api/lobby/<access_code>/")
def lobby_api(access_code):
    if access_code not in hanabi_lobbies:
        abort(404)

    game = hanabi_lobbies[access_code]
    players = {}
    for player in game.players:
        players[player] = {
            "name": game.players[player].name,
            "order": game.players[player].turn_order,
        }

    return jsonify({"players": players})


@app.route("/lobby/<access_code>/")
@app.route("/lobby/<access_code>/player-id/<player_id>/")
def lobby(access_code, player_id=None):
    return render_template(
        "lobby.html", access_code=access_code, player_id=player_id
    )


@app.route("/game-in-session/<access_code>/player-id/<player_id>/")
def game_in_session(access_code, player_id):
    game_state = hanabi_lobbies[access_code].get_game_state(player_id)
    return render_template(
        "game-in-session.html",
        access_code=access_code,
        player_id=player_id,
        game_state=game_state,
    )


@app.route("/create-lobby/", methods=["post"])
def create_lobby():
    form = forms.CreateLobbyForm(prefix="create-lobby-")
    if not form.validate_on_submit():
        return main(create_form=form)

    game = HanabiGame()
    game.add_player(form.name.data)

    access_code = "hanab"
    hanabi_lobbies[access_code] = game

    return redirect(
        url_for("lobby", access_code=access_code, player_id=form.name.data)
    )


@app.route("/join-lobby/", methods=["post"])
def join_lobby():
    form = forms.JoinLobbyForm(prefix="join-lobby-")

    if form.validate(hanabi_lobbies):
        access_token = form.access_token.data
        name = form.name.data

        game = hanabi_lobbies[access_token]
        game.add_player(name)

        return redirect(
            url_for("lobby", access_code=access_token, player_id=name)
        )

    # Important to pass the current form instance so we can keep data
    # and display errors.
    return main(join_form=form)


@app.route("/start-game/", methods=["post"])
def start_game():
    access_code = request.form["access_code"]
    game_instance = hanabi_lobbies[access_code]

    player_id = request.form["player_id"]

    game_instance.add_player("Ahna")
    game_instance.add_player("Bill")
    game_instance.add_player("Sam")

    game_instance.start_game()

    return redirect(
        url_for(
            "game_in_session",
            access_code=access_code,
            player_id=player_id,
            game_state=game_instance.get_game_state(player_id),
        )
    )


@app.route("/api/is-game-on/<access_code>/")
def is_game_on(access_code):
    return jsonify({"status": hanabi_lobbies[access_code].game_in_session})


@app.route("/api/player-response/<access_code>/<player_id>/", methods=["post"])
def handle_player_move(access_code, player_id):
    hanabi_lobbies[access_code].handle_move_request(request.json, player_id)
    return get_game_state_api(access_code, player_id)
