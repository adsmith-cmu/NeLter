import math, random, string

class Card(object):
    ranks = [None, 'Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
    suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
    ranks_shorthand = [None, 'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    suits_shorthand = ['S', 'D', 'C', 'H']

    @staticmethod
    def new_deck(shuffled=True):
        deck = list()
        for suit in Card.suits:
            for rank in range(1, len(Card.ranks)):
                if suit in {'Clubs', 'Hearts'}:
                    deck.append(Card(len(Card.ranks) - rank,suit))
                else:
                    deck.append(Card(rank, suit))
        if shuffled: 
            random.shuffle(deck)
        return deck

    def __init__(self, rank, suit):
        if rank in range(1, len(Card.ranks)):
            self.rank = rank
        elif (rank in Card.ranks) and (rank != None):
            self.rank = Card.ranks.index(rank)
        elif (rank in Card.ranks_shorthand) and (rank != None):
            self.rank = Card.ranks_shorthand.index(rank)
        else:
            raise AttributeError(f'{rank} not a valid rank')
        
        if suit in range(len(Card.suits)):
            self.suit = suit
        elif suit in Card.suits:
            self.suit = Card.suits.index(suit)
        elif suit in Card.suits_shorthand:
            self.suit = Card.suits_shorthand.index(suit)
        else:
            raise AttributeError(f'{suit} not a valid suit')

    def __eq__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 1 else len(Card.ranks)
            rank2 = other.rank if other.rank > 1 else len(Card.ranks)
            return rank1 == rank2

    def __lt__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 1 else len(Card.ranks)
            rank2 = other.rank if other.rank > 1 else len(Card.ranks)
            return rank1 < rank2

    def __le__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 1 else len(Card.ranks)
            rank2 = other.rank if other.rank > 1 else len(Card.ranks)
            return rank1 <= rank2

    def __gt__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 1 else len(Card.ranks)
            rank2 = other.rank if other.rank > 1 else len(Card.ranks)
            return rank1 > rank2

    def __ge__(self, other):
        if isinstance(other, Card):
            rank1 = self.rank if self.rank > 1 else len(Card.ranks)
            rank2 = other.rank if other.rank > 1 else len(Card.ranks)
            return rank1 >= rank2
    
    def __hash__(self):
        return hash((Card.ranks[self.rank], Card.suits[self.suit]))

    def __repr__(self):
        return f'{Card.ranks_shorthand[self.rank]}{Card.suits_shorthand[self.suit]}'

    def __str__(self):
        return f'{Card.ranks[self.rank]} of {Card.suits[self.suit]}'




def best_poker_hand(hole_cards, community_cards=list()):
    cards = sorted(list(hole_cards) + community_cards)
    rank_count = dict()
    suit_count = dict()
    for card in cards:
        rank_count[card.rank] = rank_count.get(card.rank, 0) + 1
        suit_count[card.suit] = rank_count.get(card.suit, 0) + 1
    
    flush_suit = max(suit_count)
    if suit_count[flush_suit] >= 5:
        for card in range(1, len(cards)):
            if card.suit == flush_suit and 



    

    
    
    return None

