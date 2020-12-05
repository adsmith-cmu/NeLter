from tkinter import _flatten
from cards import *

def best_flush(*cards):
    cards = sorted(_flatten(cards))
    suit_count = dict()
    for card in cards:
        suit_count[card.suit] = suit_count.get(card.suit, list()) + [card]
    possible_flush = max(suit_count.values(), key=len)
    if len(possible_flush) >= 5:
        possible_straight_flush = best_straight(possible_flush)
        if possible_straight_flush != None:
            return possible_straight_flush
        else:
            return possible_flush[len(possible_flush) - 5: len(possible_flush)]
    return None


def best_straight(*cards):
    cards = sorted(_flatten(cards), key=lambda card : card.rank)
    best_hand = [cards[0]]
    for i in range(len(cards)-1):
        if cards[i].rank + 1 == cards[i+1].rank:
            best_hand.append(cards[i+1])
        elif len(best_hand) < 4:
            best_hand = [cards[i+1]] 
    if len(best_hand) >= 5:
        return best_hand[len(best_hand) - 5: len(best_hand)]
    return None

def best_set(*cards):
    cards = sorted(_flatten(cards))
    best_hand = list()
    rank_count = dict()
    for card in cards:
        rank_count[card.rank] = rank_count.get(card.rank, list()) + [card]
    something = sorted(rank_count.values(), key=len, reverse=True)
    
    return None

cards = []
for i in range(1,8):
    cards.append(Card(i, 'S'))
cards[2] = Card('K', 'D')
cards.pop(5)
print(cards)
print(best_flush(cards))