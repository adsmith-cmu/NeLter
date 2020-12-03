from cards import Card
from tkinter import ARC
from PIL import ImageTk

class Hand(object):
    count = 0 # Keep track of hand number for logs

    PRE_FLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4


    def __init__(self, players, button, *blinds, ante=0):
        self.players = sorted(players, key=lambda player: player.seat)
        self.deck = Card.new_deck()
        self.community_cards = list()
        self.pot = 0

        self.betting_round = 0
        self.button = button
        self.absolute_min_raise = max(*blinds, 0)
        self.reset_round()

        # Deal initial cards and put in blinds/ante
        for i in range(2):
            for player in self.players:
                if i == 0:
                    player.stack -= ante
                    self.pot += ante
                player.deal_card(self.deck.pop(0))

        for blind in blinds:
            player = self.players[self.action]
            player.stack -= blind
            self.pot += blind
            self.current_bet[self.action] += blind
            self.next_player()
            self.closing_action = self.action

        # Initialize hand log -- HANDLE WITH LOG CLASS??
        Hand.count += 1
        self.log = f'Hand #{Hand.count} is being delt to {len(self.players)} players.'


    # Move the "action" onto the next player 
    def next_player(self, button=None):
        if button != None:
            self.action = (button + 1) % len(self.players)
        else:
            self.action = (self.action + 1) % len(self.players)


    # Reset variables for a new round of betting
    def reset_round(self):
        self.next_player(self.button)
        self.closing_action = self.button
        self.current_bet = [0 for _ in self.players]
        self.relative_min_raise = self.absolute_min_raise


    def progress_game(self):
        self.betting_round += 1
        if self.betting_round == Hand.SHOWDOWN:
            self.showdown()
        else:
            self.reset_round()
            self.deck.pop(0)
            if self.betting_round == Hand.FLOP:
                for _ in range(3):
                    self.community_cards.append(self.deck.pop(0))
            else:
                self.community_cards.append(self.deck.pop(0))


    # NEED LOGGING FOR HAND AND PLAYER
    def bet(self, amount):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise
        if player.stack > call_price:
            amount = max(amount, min(min_raise, player.stack))
            player.stack -= amount
            self.pot += amount
            self.current_bet[self.action] += amount 
            self.relative_min_raise = amount - call_price
            self.closing_action = self.action
            self.next_player()
        else:
            self.call()
        

    def call(self):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if player.stack > 0 or call_price <= 0:
            amount = min(call_price, player.stack)
            player.stack -= amount
            self.pot += amount
            self.current_bet[self.action] += amount

            self.next_player() 
            if self.closing_action == self.action:
                self.progress_game() 
        else:
            self.fold()

        
    def fold(self):
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if call_price > 0:
            self.players.pop(self.action)
            self.current_bet.pop(self.action)

        if len(self.players) == 1:
            self.showdown()
        else:
            self.next_player() 
            if self.closing_action == self.action:
                self.progress_game() 


    def showdown(self):
        return None
    

    def draw_community_cards(self, app, canvas):
        pass


    def __repr__(self):
        output = f'Pot: {self.pot} Board: {self.community_cards}'
        for i in range(len(self.players)):
            output += f'\n{self.players[i]}'
            if i == self.button: output += ' **'
            if i == self.action: output += ' <- ACTION'
        return output

    
class Player(object):

    def __init__(self, stack, seat):
        self.stack = stack
        self.seat = seat
        self.hole_cards = list()

    def deal_card(self, card):
        self.hole_cards.append(card)
        self.hole_cards.sort(reverse=True)

    
    def draw_hole_cards(self, app, canvas):
        sprite = self.hole_cards[0].sprite()
        scaling_factor = app.height / 6 / sprite.size[1]
        sprite_x = int(sprite.size[0] * scaling_factor)
        sprite_y = int(sprite.size[1] * scaling_factor)

        card1 = self.hole_cards[0].sprite().resize((sprite_x, sprite_y))
        card2 = self.hole_cards[1].sprite().resize((sprite_x, sprite_y))
        canvas.create_image(app.width/2 - (sprite_x/2 + 10), (2/3)*app.height, image=ImageTk.PhotoImage(card1))
        canvas.create_image(app.width/2 + (sprite_x/2 + 10), (2/3)*app.height, image=ImageTk.PhotoImage(card2))

    def __repr__(self):
        return f'Player(Seat: {self.seat}, Stack: {self.stack}, Cards: {self.hole_cards})'


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
            if card.suit == flush_suit:
                return None
    return None


def draw_table(app, canvas):
    top_rail = ((1/4)*app.width-1, (1/6)*app.height, 
                (3/4)*app.width+1, (1/6)*app.height)
    bottom_rail = ((1/4)*app.width-1, (2/3)*app.height, 
                   (3/4)*app.width+1, (2/3)*app.height)
    left_rail = ((1/8)*app.width, (1/6)*app.height,
                 (3/8)*app.width, (2/3)*app.height)
    right_rail = ((5/8)*app.width, (1/6)*app.height, 
                  (7/8)*app.width, (2/3)*app.height)
    # Color in the table
    
    canvas.create_arc(left_rail, fill='dark green', width=0, start=90, extent=180)
    canvas.create_arc(right_rail, fill='dark green', width=0, start=90, extent=-180)
    canvas.create_rectangle(top_rail[0:2], bottom_rail[2:], fill='dark green', width=0)
    # Draw the borders
    canvas.create_line(top_rail, width=5)
    canvas.create_line(bottom_rail, width=5)
    canvas.create_arc(left_rail, width=5, start=90, extent=180, style=ARC)
    canvas.create_arc(right_rail, width=5, start=90, extent=-180, style=ARC)
