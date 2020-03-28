const PLAYER_LIST_UPDATE_INTERVAL_MILLIS  = 5000;
const GAME_STATE_UPDATE_MILLIS = 5000;

function fetchPlayerInfo(accessToken) {
    let foo = "bar";
    return fetch("/api/lobby/" + accessToken + "/")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            return data.players;
        });
}

function updatePlayerList(playerListContainer, players) {
    const playerList = $("<ul />");
    for (const player in players) {
        const playerListItem = $("<li />");
        playerListItem.text(player);

        playerList.append(playerListItem);
    }

    playerListContainer.empty();
    playerListContainer.append(playerList);
}

function pollPlayerList(accessToken, playerListContainer) {
    fetchPlayerInfo(accessToken)
        .then(updatePlayerList.bind(this, playerListContainer))
        .then(function () {
            setTimeout(
                pollPlayerList.bind(this, accessToken, playerListContainer),
                PLAYER_LIST_UPDATE_INTERVAL_MILLIS
            );
        }.bind(this));
}

function startPollingPlayerList(accessToken, playerListSelector) {
    const playerListContainer = $(playerListSelector);

    pollPlayerList(accessToken, playerListContainer);
}

async function fetchIsGameOn(accessToken) {
    return fetch("/api/is-game-on/" + accessToken + "/")
        .then(function (response) {
            return response.json();
        });
}

function pollGameState(accessToken, playerId) {
    fetchIsGameOn(accessToken)
        .then(function (response) {
            if (response["status"] === true) {
               window.location.href = "/game-in-session/"+accessToken+"/player-id/"+playerId+"/";
            }
        }).then(function () {
            setTimeout(
                pollGameState.bind(this, accessToken, playerId),
                GAME_STATE_UPDATE_MILLIS
            );
        }.bind(this));
}
