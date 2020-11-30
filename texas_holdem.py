from cards import Card

class Game(object):

    def __init__(self, player_count)
        community_cards = list()
        deck = Card.new_deck()


class Hand(object):
    def __init__(self, players):
        self.players = players
        self.deck = Card.new_deck()

class Player(object):
    community_cards = list()
    deck = Card.new_deck()

    def __init__(self, seat, player_count):
        self.hole_cards = deck[seat], deck[seat + player_count]


