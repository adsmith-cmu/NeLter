import math, random, string
from PIL import Image
from tkinter import _flatten

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
     
    def sprite(self, face_down=False):
        if face_down:
            path = f'resources/purple_back.jpg'
        else:
            path = f'resources/cards_jpg/{self.__repr__()}.jpg'
        return Image.open(path)#.convert("RGB")

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


class PokerHand(object):
    STRAIGHT_FLUSH = 9
    QUADS = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    SET = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH_CARD = 1

    def __init__(self, *cards):
        self.hand, self.value = PokerHand.best_poker_hand(*cards)

    def __eq__(self, other):
        if isinstance(other, PokerHand):
            if self.value[0] == other.value[0]:
                for i in range(len(self.value[1])):
                    if self.value[1][i] != other.value[1][i]:
                        return False
                return True
            return self.value[0] == other.value[0]

    def __lt__(self, other):
        if isinstance(other, PokerHand):
            if self.value[0] == other.value[0]:
                for i in range(len(self.value[1])):
                    if self.value[1][i] >= other.value[1][i]:
                        return False
                return True
            return self.value[0] < other.value[0]

    def __le__(self, other):
        if isinstance(other, PokerHand):
            if self.value[0] == other.value[0]:
                for i in range(len(self.value[1])):
                    if self.value[1][i] > other.value[1][i]:
                        return False
                return True
            return self.value[0] <= other.value[0]

    def __gt__(self, other):
        if isinstance(other, PokerHand):
            if self.value[0] == other.value[0]:
                for i in range(len(self.value[1])):
                    if self.value[1][i] <= other.value[1][i]:
                        return False
                return True
            return self.value[0] > other.value[0]

    def __ge__(self, other):
        if isinstance(other, PokerHand):
            if self.value[0] == other.value[0]:
                for i in range(len(self.value[1])):
                    if self.value[1][i] < other.value[1][i]:
                        return False
                return True
            return self.value[0] >= other.value[0]

    @staticmethod
    def best_poker_hand(*cards):
        for func in [PokerHand._best_flush, PokerHand._best_straight, PokerHand._best_set]:
            best_hand = func(*cards)
            if best_hand != None:
                return best_hand

    @staticmethod
    def _best_flush(*cards):
        cards = sorted(_flatten(cards))
        suit_count = dict()
        for card in cards:
            suit_count[card.suit] = suit_count.get(card.suit, list()) + [card]
        possible_flush = max(suit_count.values(), key=len)
        if len(possible_flush) >= 5:
            possible_straight_flush = PokerHand._best_straight(possible_flush)
            if possible_straight_flush != None:
                return possible_straight_flush[0], (PokerHand.STRAIGHT_FLUSH, max(possible_straight_flush))
            else:
                flush = possible_flush[len(possible_flush) - 5: len(possible_flush)]
                return flush, (PokerHand.FLUSH, [max(flush)])
        return None

    @staticmethod
    def _best_straight(*cards):
        cards = sorted(_flatten(cards), key=lambda card : card.rank)
        print(cards)
        best_hand = [cards[0]]
        for i in range(len(cards)-1):
            if cards[i].rank + 1 == cards[i+1].rank:
                best_hand.append(cards[i+1])
            else:
                best_hand = [cards[i+1]]
        if len(best_hand) >= 5:
            straight = best_hand[len(best_hand) - 5: len(best_hand)]
            return straight, (PokerHand.STRAIGHT, [max(straight)])
        return None

    @staticmethod
    def _best_set(*cards, hand_size=5, value=(0, list())):
        cards = sorted(_flatten(cards))
        hand_size = min(hand_size, len(cards))
        if hand_size < 1:
            best_hand = list()
        else:
            rank_count = dict()
            for card in cards:
                rank_count[card.rank] = rank_count.get(card.rank, list()) + [card]
            card_sets = sorted(rank_count.values(), key=PokerHand._sorting_card_lists, reverse=True)
            
            value_map = [None, PokerHand.HIGH_CARD, PokerHand.PAIR, PokerHand.SET, PokerHand.QUADS]
            if value[0] == PokerHand.SET and value_map[len(card_sets[0])] == PokerHand.PAIR:
                value[0] = PokerHand.FULL_HOUSE
            elif value[0] == PokerHand.PAIR and value_map[len(card_sets[0])] == PokerHand.PAIR:
                value[0] = PokerHand.TWO_PAIR
            else:
                value[0] = max(value[0], value_map[len(card_sets[0])])
            value[1].append(card_sets[0][0])
            print('val', value[1])
            if len(max(card_sets, key=len)) == 1:
                best_hand = list(_flatten(card_sets[0:hand_size]))
            else:
                best_hand = card_sets[0] + PokerHand._best_set(card_sets[1:], hand_size=hand_size-len(card_sets[0]), value=value)[0]
        return best_hand, value

    @staticmethod
    def _sorting_card_lists(cards):
        rank = cards[0].rank if cards[0].rank > 1 else len(Card.ranks)
        return len(cards)*len(Card.ranks) + rank

    def __repr__(self):
        return f'{self.hand}, {self.value}'

community = [Card(3, 'S'), Card('A', 'S'), Card(8, 'C'), Card(9, 'C'), Card(2, 'C')]
hole = [Card(10, 'H'), Card(4, 'C')]
print(PokerHand._best_straight(community, hole))