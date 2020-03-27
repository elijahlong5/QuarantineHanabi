const GAME_UPDATE_INTERVAL_MILLIS = 5000;

function fetchGameState(accessToken, playerId) {
    console.log(playerId)
    return fetch("/api/game-in-session/" + accessToken + "/" + playerId + "/")
        .then(function(response) {
            return response.json();
        });
}


async function fetchPostPlayerMove(playCardDict, accessToken, playerId) {
    let data = playCardDict;
    url = "/api/player-response/" + accessToken + "/" + playerId + "/";
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrer: 'no-referrer',
        body: JSON.stringify(data)
    })

    return await response.json(); //todo:handle the response dict (should repopulate that players hand if the move was a discard
}



function initiateDisplay(accessToken, playerId) {
    fetchGameState(accessToken, playerId)
        .then( function (gameState) {
            console.log(gameState);
            let baseLink = "/static/hanabi_deck/";

            for (let curPId in gameState['players']) {
                // make player div
                let playerDiv = document.createElement("div");
                playerDiv.id = curPId;
                $("#hands").append(playerDiv);

                let playerHeader = document.createElement("h3");
                playerHeader.innerText = curPId;
                playerDiv.appendChild(playerHeader);

                let cardsDiv = document.createElement("div");
                cardsDiv.classList.add("cards-container");
                playerDiv.appendChild(cardsDiv);

                for (let card in gameState['players'][curPId]) {
                    let curImg = document.createElement("img");
                    let color = gameState['players'][curPId][card][0];
                    let rank = gameState['players'][curPId][card][1];
                    let cardId = gameState['players'][curPId][card][2];
                    let link = (curPId === playerId) ? (baseLink+"card_back.png") : (baseLink+color+"_"+rank+".png");
                    curImg.src = link;
                    cardsDiv.appendChild(curImg);
                    curImg.addEventListener("click", function() {
                        console.log("the "+color+" "+rank+" was clicked");
                        event.preventDefault();

                        // Todo: for now all own-hand card moves are "plays"
                        let move = (curPId === playerId) ? "play" : "hint";
                        let cardIndex = (curPId === playerId) ? card : cardId;
                        let hintType = (curPId === playerId) ? null : "rank";

                        let moveDict = {
                            "move": move,// = play discard or hint
                            "card-index": cardIndex, // REQUIRED: 0-3 index for what card is selected
                            "player-id": curPId, // REQUIRED: = key if play or discard. otherwise, who they are hinting to
                            "hint-type": hintType, // REQUIRED IF HINT: either rank or color.
                        };

                        console.log("move dict is:");
                        console.log(moveDict);

                        fetchPostPlayerMove(moveDict, accessToken, playerId).then(r => {
                            console.log(r);
                            // Todo: update display
                        })
                    });
                }
            }
        });
}

