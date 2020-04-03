const GAME_UPDATE_INTERVAL_MILLIS = 5000;

async function fetchGameState(gameCode, playerName) {
    return fetch("/api/games/" + gameCode + "/?as_player=" + playerName)
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
    });

    return await response.json();
}

function numberToColor(num) {
    let color = "";
    switch (num) {
        case 1:
            color = "Blue";
            break;
        case 2:
            color = "Green";
            break;
        case 3:
            color = "Rainbow";
            break;
        case 4:
            color = "Red";
            break;
        case 5:
            color = "White";
            break;
        case 6:
            color = "Yellow";
            break;
        default:
            color = "Yellow";
    }
    return color
}

function initiateDisplay(gameCode, playerName) {
    pollGameState(gameCode, playerName);
}

function pollGameState(gameCode, playerName) {
    fetchGameState(gameCode, playerName)
        .then(populateDisplay.bind(this))
        .then( function() {
           setTimeout(
             pollGameState.bind(this, gameCode, playerName),
               GAME_UPDATE_INTERVAL_MILLIS
           );
        });
}


function populateDisplay( gameState ) {
    document.getElementById("hands").innerHTML = "";
    document.getElementById("deck").innerHTML = "";
    document.getElementById("bombs").innerHTML = "";
    document.getElementById("piles").innerHTML = "";

    let remainingBombs = gameState["remaining_bombs"];
    let remainingCards = gameState["remaining_cards"];
    let players = gameState["players"];

    let baseLink = "/static/hanabi_deck/";
    let cardBackLink = baseLink + "card_back.png";

    // Display players' hands
    for (let p in players) {
        let curPlayerName = players[p]["name"];
        let playerCards = players[p]["cards"];
        let playerOrder = players[p]["order"];

        // make player div
        let playerDiv = document.createElement("div");
        playerDiv.id = curPlayerName;
        $("#hands").append(playerDiv);

        let playerHeader = document.createElement("h3");
        playerHeader.innerText = curPlayerName;
        playerDiv.appendChild(playerHeader);

        let cardsDiv = document.createElement("div");
        cardsDiv.classList.add("cards-container");
        playerDiv.appendChild(cardsDiv);


        for (let card in playerCards) {
            let link = cardBackLink;
            let cardOrder = card;
            if ("color" in playerCards[card]) {
                let color = numberToColor(playerCards[card]["color"]);
                let rank = playerCards[card]["number"];
                link = baseLink+color+"_"+rank+".png";
            }

            let curImg = document.createElement("img");
            curImg.src = link;
            cardsDiv.appendChild(curImg);
            curImg.addEventListener("click", function() {
                event.preventDefault();
                console.log("Card " + cardOrder + " was clicked!");
            });
        }
    }

    // Display deck.
    let deckImg = document.createElement("img");
    deckImg.classList.add("card");
    deckImg.src = cardBackLink;
    $("#deck").append(deckImg);
    let deckCount = document.createElement("h3");
    deckCount.innerHTML = "Remaining:</br>" + remainingCards;
    deckCount.classList.add("centered");
    $("#deck").append(deckCount);

    // Display Bomb Count.
    let bombCountTitle = document.createElement("h3");
    bombCountTitle.innerText = "Bombs remaining: " + remainingBombs;
    $("#bombs").append(bombCountTitle);
}
