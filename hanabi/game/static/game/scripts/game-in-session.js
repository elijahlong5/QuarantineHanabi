const GAME_UPDATE_INTERVAL_MILLIS = 5000;
const ID_DECK_IMG = 'deck-image';
const ID_BOMBS = 'bombs-remaining';
const ID_CARDS_REMAINING = 'cards-remaining';
const CARD_ID_SUFFIX = "s-cards"; // playerName + suffix

// Card link strings
const LINK_BASE_CARD = "/static/hanabi_deck/";
const LINK_CARD_BACK = LINK_BASE_CARD + "card_back.png";

// css classes
const UNSELECTED_CARD_CLASS = "unselected-card";
const SELECTED_CARD_CLASS = "selected-card";

let prevGameState = {};

// Variables set from the template
const GAME_CODE = window.gameCode;
const PLAYER_NAME = window.playerName;

// Hint button ids
const ID_BUTTON_NUMBER_HINT = "hint-number-button-id";
const ID_BUTTON_COLOR_HINT = "hint-color-button-id";

// Card image attributes
const ATTR_NAME = "data-player-name";
const ATTR_COLOR = "data-card-color";
const ATTR_NUMBER = "data-card-number";
const ATTR_PILE_NUM = "data-pile-for-"; // attr + color for the pile attribute

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
    // Function when page is loaded.  Displays bombs, hands, piles, deck etc.

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

    initiatePiles(gameState);

    prevGameState = gameState;
}

function manageHandDisplay(cardsDiv, currentPlayerDict) {
    // Displays images for the cards in  each players hand
    // Sets card attributes
    let playerCards = currentPlayerDict["cards"];
    let curPlayerName = currentPlayerDict["name"];
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
            curImg.classList.add(UNSELECTED_CARD_CLASS);

            // Set card attributes into the image.
            curImg.setAttribute(ATTR_NAME, curPlayerName);
            if ('color' in playerCards[card]) { // Assuming if color then number.
                curImg.setAttribute(ATTR_COLOR, playerCards[card]["color"]);
                curImg.setAttribute(ATTR_NUMBER, playerCards[card]["number"]);
            }

            cardsDiv.appendChild(curImg);
            curImg.addEventListener("click", function () {
                event.preventDefault();
                if (genCardLink(playerCards[card]) === LINK_CARD_BACK) {
                    handlePlayerMove(cardId);
                } else {
                    handleOnClickCreateHintOptions(cardId);
                }
            });
        }
    }

    for(let i of activeIdList){
        if (childCardIds.indexOf(i) !== -1) {
            childCardIds.splice(childCardIds.indexOf(i), 1);
        }
    }
    childCardIds.forEach(id => {
       cardsDiv.removeChild(document.getElementById(id));
    });
}

function handleOnClickCreateHintOptions(cardId) {
    let choiceDiv = document.createElement("div");
    const HINT_CHOICES_ID = "hint-choices";
    choiceDiv.id = HINT_CHOICES_ID;

    let bodyElem = document.getElementsByTagName("body")[0];
    let cardImgElem = document.getElementById(cardId);

    // Manage the element classes
    cardImgElem.classList.remove(UNSELECTED_CARD_CLASS);
    cardImgElem.classList.add(SELECTED_CARD_CLASS);

    let cardHandDiv = cardImgElem.parentElement.parentElement;

    let cardPosition = $("#"+cardHandDiv.id).position();

    // Create the two buttons
    let buttonHintNumber = document.createElement('button');
    buttonHintNumber.innerText = "Number";
    buttonHintNumber.id = ID_BUTTON_NUMBER_HINT;
    let buttonHintColor = document.createElement('button');
    buttonHintColor.innerText = "Color";
    buttonHintColor.id = ID_BUTTON_COLOR_HINT;

    buttonHintNumber.addEventListener("click", function() {
        event.preventDefault();
        fetchPostPlayerHint(cardId, "number", cardHandDiv.id)
            .then(r => {
                console.log(r);
                clearHintOptions();
            })
    });
    buttonHintColor.addEventListener("click", function() {
        event.preventDefault();
        fetchPostPlayerHint(cardId, "color", cardHandDiv.id)
            .then(r => {
                console.log(r);
                clearHintOptions();
            })
    });

    // Append the elements and position the button div
    choiceDiv.appendChild(buttonHintNumber);
    choiceDiv.appendChild(buttonHintColor);

    $("#"+HINT_CHOICES_ID).remove();
    bodyElem.appendChild(choiceDiv);

    $("#"+HINT_CHOICES_ID).css({
        position: "absolute",
        top: cardPosition.bottom + "px",
        left: (cardPosition.left) + "px",
        width: "150%",
    });
}

async function fetchPostPlayerHint( cardId, hintType, targetPlayerName ) {
    let cardElem = document.getElementById(cardId);
    let cardColor = cardElem.getAttribute(ATTR_COLOR);
    let cardNumber = cardElem.getAttribute(ATTR_NUMBER);
    let cardAttr = cardNumber;
    if (hintType === "number"){
        cardAttr = cardNumber;
    } else {
        cardAttr = cardColor;
    }

    let data = {
        "action_type": "HINT",
        "player_name": PLAYER_NAME,
        'hint_action': {
            [hintType]: cardAttr,
            "target_player_name": targetPlayerName,
        }
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

function genCardLink(card) {
    // Creates the image source link for the card.
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

    updatePiles(gameState);

    for (let p in players) {
        let curP = players[p];
        let curPlayerName = players[p]["name"];
        let playerCards = players[p]["cards"];
        let playerOrder = players[p]["order"];

        let cardsDivId = curPlayerName + CARD_ID_SUFFIX;
        let cardsDiv = document.getElementById(cardsDivId);
        manageHandDisplay(cardsDiv, curP);
    }
}

function clearHintOptions() {
    // Removes number and color buttons.  Resets all cards to 'unselected'

    for (let c of document.getElementsByClassName(SELECTED_CARD_CLASS)){
        c.classList.remove(SELECTED_CARD_CLASS);
        c.classList.add(UNSELECTED_CARD_CLASS);
    }
    let bColor = document.getElementById(ID_BUTTON_COLOR_HINT);
    let bNumber = document.getElementById(ID_BUTTON_NUMBER_HINT);
    console.log('here');
    bColor.parentNode.removeChild(bColor);
    bNumber.parentNode.removeChild(bNumber);
}

function initiatePiles(gameState) {
    // Displays 1 pile for each color being used of blank cards

    let piles = gameState['piles'];
    const colorsUsed = Object.keys(piles);
    let pilesDiv = document.getElementById('piles');

    for (let c of colorsUsed) {
        // Create the image with attribute and id
        let pileImg = document.createElement("img");
        pileImg.setAttribute(ATTR_PILE_NUM+c, 0);
        pileImg.id = ATTR_PILE_NUM+c;
        pileImg.src = LINK_CARD_BACK;
        console.log(c);

        pilesDiv.appendChild(pileImg);
    }
}

function updatePiles(gameState) {
    // Update the image and image attribute for the top card in the piles

    let piles = gameState['piles'];
    for (let c in piles) {
        let pileAttr = ATTR_PILE_NUM+c;
        let curPile = document.getElementById(pileAttr);
        let attr = curPile.getAttribute(pileAttr);
        if (parseInt(attr) !== piles[c]) {
            curPile.setAttribute(pileAttr, piles[c]);
            curPile.src = LINK_BASE_CARD + c + "_" + piles[c] + ".png";
        }
    }
}
