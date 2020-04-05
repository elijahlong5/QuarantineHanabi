const GAME_UPDATE_INTERVAL_MILLIS = 5000;
const ID_DECK_IMG = 'deck-image';
const ID_BOMBS = 'bombs-remaining';
const ID_CARDS_REMAINING = 'cards-remaining';
const CARD_ID_SUFFIX = "s-cards"; // playerName + suffix

const LINK_BASE_CARD = "/static/hanabi_deck/";
const LINK_CARD_BACK = LINK_BASE_CARD + "card_back.png";

let prevGameState = {};

const GAME_CODE = window.gameCode;
const PLAYER_NAME = window.playerName;

async function fetchGameState() {
    return fetch("/api/games/" + GAME_CODE + "/?as_player=" + PLAYER_NAME)
        .then(function(response) {
            return response.json();
        });
}

function handlePlayerMove( cardId ){
    fetchPostPlayerMove(cardId)
        .then( r => {
            console.log(r);
        })
}

async function fetchPostPlayerMove( cardId ) {
    let data = {
        "action_type": "PLAY",
        "player_name": PLAYER_NAME,
        "play_action": {
            "card_id": cardId,
        },
    };
    url = "/api/games/" + GAME_CODE + "/actions/";
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
        body: JSON.stringify(data),
    });

    return await response.json();
}

function initiateDisplay() {
    fetchGameState()
        .then(populateDisplay.bind(this))
        .then(pollGameState.bind(this));
}

function pollGameState() {
    fetchGameState()
        .then(updateDisplay.bind(this))
        .then( function() {
           setTimeout(
             pollGameState.bind(this),
               GAME_UPDATE_INTERVAL_MILLIS
           );
        });
}

function populateDisplay( gameState ) {
    // game state elements
    let remainingBombs = gameState["remaining_bombs"];
    let remainingCards = gameState["remaining_cards"];
    let players = gameState["players"];

    document.getElementById("hands").innerHTML = "";
    document.getElementById("deck").innerHTML = "";
    document.getElementById("bombs").innerHTML = "";
    document.getElementById("piles").innerHTML = "";
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
        cardsDiv.id = curPlayerName + CARD_ID_SUFFIX;
        cardsDiv.classList.add("cards-container");
        playerDiv.appendChild(cardsDiv);

        manageHandDisplay(cardsDiv, playerCards);
    }

    // Display deck.
    let deckImg = document.createElement("img");
    deckImg.id = ID_DECK_IMG;
    deckImg.classList.add("card");
    deckImg.src = LINK_CARD_BACK;
    $("#deck").append(deckImg);
    let deckCount = document.createElement("h3");
    deckCount.id = ID_CARDS_REMAINING;
    deckCount.innerHTML = "Remaining:</br>" + remainingCards;
    deckCount.classList.add("centered");
    $("#deck").append(deckCount);

    // Display Bomb Count.
    let bombCountTitle = document.createElement("h3");
    bombCountTitle.id = ID_BOMBS;
    bombCountTitle.innerText = "Bombs remaining: " + remainingBombs;
    $("#bombs").append(bombCountTitle);

    prevGameState = gameState;
}

function manageHandDisplay(cardsDiv, playerCards) {
    let activeIdList = [];

    let childCardIds = [];
    if ( cardsDiv.children ) {
        Array.from(cardsDiv.children).forEach(element => {
            if (element.id !== undefined) {
                childCardIds.push(element.id);
            }
        });
    }

    for (let card in playerCards) {
        let cardOrder = card;
        let cardId = playerCards[card]["id"];

        activeIdList.push(cardId);

        if (!(childCardIds.indexOf(cardId) >= 0) && cardId !== undefined) {
            let curImg = document.createElement("img");
            curImg.id = cardId;
            curImg.src = genCardLink(playerCards[card]);
            cardsDiv.appendChild(curImg);
            curImg.addEventListener("click", function () {
                event.preventDefault();
                handlePlayerMove(cardId);
            });
        }
    }

    for( let i of activeIdList){
        if (childCardIds.indexOf(i) !== -1) {
            childCardIds.splice(childCardIds.indexOf(i), 1);
        }
    }
    childCardIds.forEach(id => {
       cardsDiv.removeChild(document.getElementById(id));
    });
}

function genCardLink(card) {
    let link = LINK_CARD_BACK;

    if ("color" in card) {
        let color = card["color"];
        let rank = card["number"];
        link = LINK_BASE_CARD + color + "_" + rank + ".png";
    }
    return link;
}

function updateDisplay(gameState) {
    console.log(gameState);
    let remainingBombs = gameState["remaining_bombs"];
    let remainingCards = gameState["remaining_cards"];
    let players = gameState["players"];
    let bombCount = document.getElementById(ID_BOMBS);
    let deckCount = document.getElementById(ID_CARDS_REMAINING);

    bombCount.innerText = "Bombs remaining: " + remainingBombs;
    deckCount.innerHTML = "Remaining:</br>" + remainingCards;

    for (let p in players) {
        let curP = players[p];
        let curPlayerName = players[p]["name"];
        let playerCards = players[p]["cards"];
        let playerOrder = players[p]["order"];

        let cardsDivId = curPlayerName + CARD_ID_SUFFIX;
        let cardsDiv = document.getElementById(cardsDivId);
        manageHandDisplay(cardsDiv, playerCards);
    }
}
