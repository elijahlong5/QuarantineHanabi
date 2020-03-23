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
@app.route("/lobby/<access_code>/player_id/<player_id>/")
def lobby(access_code, player_id=None):
    return render_template('lobby.html',
                           access_code=access_code,
                           player_id=player_id)


@app.route('/create-lobby/', methods=['post'])
def create_lobby():
    access_code = "hanab"
    hanabi_lobbies[access_code] = HanabiGame()
    return redirect(url_for("lobby", access_code=access_code))


@app.route("/join-lobby/", methods=['post'])
def join_lobby():
    access_code = request.form["access_code"]
    player_id = request.form["player_name_field"]
    return redirect(url_for("lobby",
                            access_code=access_code,
                            player_id=player_id))


if __name__ == "__main__":
    app.run()
