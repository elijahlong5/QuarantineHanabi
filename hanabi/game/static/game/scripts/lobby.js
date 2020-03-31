const PLAYER_LIST_UPDATE_INTERVAL_MILLIS  = 5000;
const GAME_STATE_UPDATE_MILLIS = 5000;

function fetchPlayerInfo(accessCode) {
    return fetch("/api/lobbies/"+accessCode+"/members/")
        .then(function (response) {
            return response.json();
        });
}

function updatePlayerList(playerListContainer, players) {
    const playerList = $("<ul />");
    for (const player of players) {
        const playerListItem = $("<li />");
        playerListItem.text(player["name"]);

        playerList.append(playerListItem);
    }

    playerListContainer.empty();
    playerListContainer.append(playerList);
}

function pollPlayerList(accessCode, playerListContainer) {
    fetchPlayerInfo(accessCode)
        .then(updatePlayerList.bind(this, playerListContainer))
        .then(function () {
            setTimeout(
                pollPlayerList.bind(this, accessCode, playerListContainer),
                PLAYER_LIST_UPDATE_INTERVAL_MILLIS
            );
        }.bind(this));
}

function startPollingPlayerList(accessCode, playerListSelector) {
    const playerListContainer = $(playerListSelector);
    pollPlayerList(accessCode, playerListContainer);
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
