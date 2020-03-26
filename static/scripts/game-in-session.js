const GAME_UPDATE_INTERVAL_MILLIS = 5000;

// todo: fetch players and game state

function fetchGameState(accessToken, playerId) {
    return fetch("/api/game-in-session/" + accessToken + "/" + playerId + "/")
        .then(function(response) {
            return response.json();
        });
}

function initiateDisplay(accessToken, playerId) {
    fetchGameState(accessToken, playerId)
        .then( function (gameState) {
            console.log(gameState);

            for (let key in gameState['players']) {
                // make player div
                let playerDiv = document.createElement("div");
                playerDiv.id = key;
                $("#hands").append(playerDiv);

                for (let card in gameState['players'][key]) {
                    let curImg = document.createElement("img");
                    let color = gameState['players'][key][card][0];
                    let rank = gameState['players'][key][card][1];
                    let link = "/static/hanabi_deck/"+color+"_"+rank+".png";
                    curImg.src = link;
                    playerDiv.appendChild(curImg);
                    curImg.addEventListener("click", function() {
                        console.log("the "+color+" "+rank+" was clicked");
                    });
                }
            }
        });
}

// todo: print hands in console- test
// todo: display stacked hands

document.addEventListener("DOMContentLoader", function() {

});
