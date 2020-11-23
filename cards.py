import math, random, string

class Card(object):
    ranks = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
    ranksShorthand = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    suitsShorthand = ['S', 'D', 'C', 'H']

    @staticmethod
    def newDeck(shuffled=True):
        deck = list()
        for suit in suits:
            for 


    def __init__(self, rank, suit):
        if rank in range(1, len(Card.ranks)+1):
            self.rank = rank-1
        elif rank in Card.ranks:
            self.rank = Card.ranks.index(rank)
        elif rank in Card.ranksShorthand:
            self.rank = Card.ranksShorthand.index(rank)
        else:
            raise Exception(f'{rank} not a valid rank')
        
        if suit in range(len(Card.suits)):
            self.suit = suit
        elif suit in Card.suits:
            self.suit = Card.suits.index(suit)
        elif suit in Card.suitsShorthand:
            self.suit = Card.suitsShorthand.index(suit)
        else:
            raise Exception(f'{suit} not a valid suit')

    def __cmp__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 0 else 13
            rank2 = other.rank if other.rank > 0 else 13
            return rank1 - rank2
    
    def __hash__(self):
        return hash((Card.ranks[self.rank], Card.suits[self.suit]))

    def __repr__(self):
        return f'{Card.ranksShorthand[self.rank]}{Card.suitsShorthand[self.suit]}'

    def __str__(self):
        return f'{Card.ranks[self.rank]} of {Card.suits[self.suit]}'


def bestPokerHand(holeCards, communityCards):
    cards = holdCards + communityCards
    rankCount = dict()
    suitCount = dict()
    for card in cards:
        rankCount[card.rank] = rankCount.get(card.rank, 0) + 1
        suitCount[card.suit] = rankCount.get(card.suit, 0) + 1
    return None