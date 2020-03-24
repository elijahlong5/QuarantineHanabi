from flask import Flask, render_template, redirect, url_for, request
from Game import HanabiGame
app = Flask(__name__)

hanabi_lobbies = {}

# Views
@app.route('/')
@app.route('/home/')
def main():
    return render_template('main.html')


@app.route("/lobby/<access_code>/")
@app.route("/lobby/<access_code>/player-id/<player_id>/")
def lobby(access_code, player_id=None):
    return render_template('lobby.html',
                           access_code=access_code,
                           player_id=player_id)


@app.route('/game-in-session/<access_code>/player-id/<player_id>/')
def game_in_session(access_code, player_id):
    game_state = hanabi_lobbies[access_code].get_game_state(player_id)
    return render_template("game-in-session.html",
                           access_code=access_code,
                           player_id=player_id,
                           game_state=game_state)


@app.route('/create-lobby/', methods=['post'])
def create_lobby():
    access_code = "hanab"
    hanabi_lobbies[access_code] = HanabiGame()
    return redirect(url_for("lobby", access_code=access_code))


@app.route("/join-lobby/", methods=['post'])
def join_lobby():
    access_code = request.form["access_code"]
    if access_code not in hanabi_lobbies.keys():
        return redirect(url_for("main"))
    player_id = request.form["player_name_field"]
    game_instance = hanabi_lobbies[access_code]
    game_instance.add_player(player_id)
    return redirect(url_for("lobby",
                            access_code=access_code,
                            player_id=player_id))


@app.route("/start-game/", methods=['post'])
def start_game():
    access_code = request.form['access_code']
    game_instance = hanabi_lobbies[access_code]
    game_instance.start_game()
    player_id = request.form['player_id']
    return redirect(url_for("game_in_session",
                            access_code=access_code,
                            player_id=player_id,
                            game_state=game_instance.get_game_state(player_id)))


@app.route("/api/lobbies/<access_code>/game-in-session")
def is_game_on(access_code):
    return hanabi_lobbies[access_code].game_in_session


if __name__ == "__main__":
    app.run()
