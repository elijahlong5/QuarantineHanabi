from collections import namedtuple

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
    def __init__(self, name):
        self.name = name
        self.hand = []

    def give_card(self, card):
        self.hand.append(card)

    def play_card(self, card):
        self.hand.pop(card)


class Deck:
    def __init__(self):
        self.deck = create_deck()
        self.cards_left = len(self.deck)

    def draw_card(self):
        self.cards_left -= 1
        return self.deck.pop(self.cards_left)


class HanabiGame:
    def __init__(self):
        self.game_in_session = False
        self.deck = Deck()
        self.players = {Player("elijah")}
        self.HAND_LIMIT = 4
        self.deal()

    def deal(self):
        for p in self.players:
            for i in range(0, self.HAND_LIMIT):
                p.give_card(self.deck.draw_card())

            print(f'{p.name} was given these cards:')
            for c in p.hand:
                print(f'The {c.Color} {c.Rank}.')




