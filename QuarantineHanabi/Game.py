from collections import namedtuple
import random

Card = namedtuple("Card", ["Color", "Rank"])


def create_deck():
    deck = []
    for c in ["Red", "Green", "Yellow", "White", "Blue"]:
        deck.append(Card(c, 1))
        for i in range(1, 6):
            deck.append(Card(c, i))
            if i != 5:
                deck.append(Card(c, i))
    return deck


class Player:
    def __init__(self, name, order):
        self.name = name
        self.hand = []
        self.turn_order = order

    def give_card(self, card):
        self.hand.append(card)


class Deck:
    def __init__(self):
        self.deck = create_deck()
        self.cards_left = len(self.deck)
        self.shuffle()

    def shuffle(self):
        for i in range(len(self.deck)-1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0, i + 1)
            # Swap arr[i] with the element at random index
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]

    def draw_card(self):
        self.cards_left -= 1
        return self.deck.pop(self.cards_left)


class HanabiGame:
    def __init__(self):
        self.game_in_session = False
        self.deck = Deck()
        self.HAND_LIMIT = 4
        self.order = 0

        self.game_log = []
        self.players = {}
        self.discard_pile = []
        self.piles = []
        self.bomb_count = 3
        self.whose_turn = ""

    def add_player(self, name):
        if name in self.players.keys():
            return ValueError
        else:
            self.players[name] = Player(name, self.order)
            self.order += 1

    def deal(self):
        for p in self.players.values():
            for i in range(0, self.HAND_LIMIT):
                p.give_card(self.deck.draw_card())

    def start_game(self):
        self.deal()
        self.discard_pile = []
        self.bomb_count = 3
        self.piles = []
        self.whose_turn = 1
        print("--------starting game-------")
        for p in self.players.values():
            print(p.name)
            for c in p.hand:
                print(f'The {c.Color} {c.Rank}.')

    def get_game_state(self, player_id):
        game_state = {
            "players": {},
            "game-log": self.game_log,
            "piles": self.piles,
            "discard-pile": self.discard_pile,
            "bomb-count": self.bomb_count,
            "whose-turn": self.current_turn_id,
        }

        for p in self.players.values():
            if self.players[p].name != player_id:
                game_state['players'][p.name] = p.hand
            else:
                game_state['players'][p.name] = []
        return game_state

    def handle_move_request(self, move_request):
        # check if the it is this players' turn
        if self.whose_turn == move_request['player-id']:
            # make the move
            if move_request['move'] == "play":
                return self.play_card(move_request)
            elif move_request['move'] == "discard":
                return self.discard(move_request)
            elif move_request['move'] == "hint":
                return self.give_hint(move_request)
        else:
            return ValueError

    # Possible moves
    def less_card_helper(self, player, card):
        p = player
        p.hand.pop(card)
        if self.deck.cards_left > 0:
            p.give_card(self.deck.draw_card())
        return card

    def play_card(self, move_request):
        card = move_request['card']
        p = self.players[move_request['player-id']]
        self.less_card_helper(p, card)
        self.piles.append(card)

    def discard_card(self, move_request):
        card = move_request['card']
        p = self.players[move_request['player-id']]
        self.less_card_helper(p, card)
        self.discard_pile.append(card)
