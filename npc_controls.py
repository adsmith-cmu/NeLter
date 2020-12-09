from cards import *
from tkinter import _flatten
import numpy as np
import itertools as it
import time


class Range(object):
    community_cards = []
    sorting_key = lambda *hand:PokerHand(*hand, Range.community_cards)

    def __init__(self, *args):
        cards = Card.new_deck(False)
        blocked_cards = _flatten(args)
        for card in blocked_cards:
            if card in cards:
                cards.remove(card)
        
        card_pairs = it.combinations(cards, 2)
        hands = list()

        for hand in card_pairs:
            ordered_hand = sorted(list(hand), reverse=True)
            if ordered_hand not in blocked_cards:
                hands.append(ordered_hand)

        self.hands = sorted(hands, key=Range.sorting_key, reverse=True)

    def update(self, *args):
        blocked_cards = list(_flatten(args)) + Range.community_cards
        for hand in self.hands:
            if hand[0] or hand[1] in blocked_cards:
                self.hands.remove(hand)

    def take_top_percent(self, proportion):
        index = int(len(self.hands) * proportion)
        self.hands = self.hands[:index]

    def take_bot_percent(self, proportion):
        index = int(len(self.hands) * proportion)
        self.hands = self.hands[index:]

    def rank_hand(self, hole_cards):
        if len(self.hands) < 1:
            return 0
        beat_hands = 0
        for hand in self.hands:
            if Range.sorting_key(hole_cards) >= Range.sorting_key(hand):
                beat_hands += 1
        return beat_hands / len(self.hands)
 
    def __len__(self):
        return len(self.hands)

    def __repr__(self):
        return f'{self.hands}'


