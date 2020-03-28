from collections import namedtuple
import random

Card = namedtuple("Card", ["Color", "Rank", "Id"])
Colors = ["Red", "Green", "Yellow", "White", "Blue"]


card_num_counts = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}


def create_deck():
    deck = []
    cur_id = 0
    for color in Colors:
        for num in range(1, 6):
            for card in range(card_num_counts[num]):
                deck.append(Card(color, num, cur_id))
                cur_id += 1
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
        random.shuffle(self.deck)

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
        self.hints_left = 8
        self.players = {}
        self.discard_pile = []
        self.bomb_count = 3
        self.whose_turn = 0
        self.piles = {}

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
        self.game_in_session = True
        self.deal()
        self.discard_pile = []
        self.bomb_count = 3
        self.piles = {}
        for c in Colors:
            self.piles[c] = 0
        start = random.choice(list(self.players.keys()))
        self.whose_turn = start

    def get_game_state(self, player_id):
        game_state = {
            "whose-game-state": player_id,
            "players": {},
            "game-log": self.game_log,
            "piles": self.piles,
            "discard-pile": self.discard_pile,
            "bomb-count": self.bomb_count,
            "whose-turn": self.whose_turn,
            "cards-in-deck": self.deck.cards_left,
        }

        for p in self.players.values():
            if p.name != player_id:
                game_state["players"][p.name] = p.hand
            else:
                game_state["players"][p.name] = {
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 3,
                }
        return game_state

    def handle_move_request(self, move_request, player_id):
        # check if the it is this players' turn
        if self.whose_turn == player_id:
            # make the move
            if move_request["move"] == "play":
                status = self.play_card(move_request)
            elif move_request["move"] == "discard":
                status = self.discard(move_request)
            elif move_request["move"] == "hint":
                status = self.give_hint(move_request)
            self.increment_turn()
            return {"status": status}
        else:
            return {"status": "not your turn"}

    def add_hint(self):
        self.hints_left = (self.hints_left + 1) if self.hints_left < 7 else 8

    def remove_hint(self):
        self.hints_left = (self.hints_left - 1) if self.hints > 1 else 0

    def add_bomb(self):
        self.bomb_count -= 1
        if self.bomb_count == 0:
            print("game over")

    def increment_turn(self):
        index = list(self.players.keys()).index(self.whose_turn)
        print(index)
        new_index = (index + 1) % 4
        self.whose_turn = list(self.players.keys())[new_index]

    # Possible moves
    def less_card_helper(self, player, card_index):
        p = player
        card = p.hand.pop(card_index)
        if self.deck.cards_left > 0:
            p.give_card(self.deck.draw_card())
        return card

    def play_card(self, move_request):
        card_index = int(move_request["card-index"])  # Index 0-3
        p = self.players[move_request["player-id"]]

        card = self.less_card_helper(p, card_index)
        rank = int(card.Rank)
        color = card.Color
        if self.piles[color] == rank - 1:
            # Th card is valid to play
            self.piles[color] = rank
            if rank == 5:
                self.add_hint()
            return f"Nice, you played {color} {rank}."
        else:
            # The card was unplayable
            self.add_bomb()
            return f"Oh No a bomb, you tried to play the {color} {rank}."

    def discard_card(self, move_request):
        card_index = int(move_request["card-index"])  # Index 0-3
        p = self.players[move_request["player-id"]]
        card = self.less_card_helper(p, card_index)
        self.add_hint()

        self.discard_pile.append(card)
        return f"You discarded the {card.Color} {card.Rank}"

    def give_hint(self, move_request):
        return "You gave a hint... smgdh."
