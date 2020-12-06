from cards import *
from tkinter import ARC, _flatten
from PIL import Image, ImageTk
from aidan_graphics import *

class Hand(object):
    count = 0 # Keep track of hand number for logs
    button_sprite = Image.open('resources/button.png').convert("RGB")

    SEATS = 8
    PRE_FLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4


    def __init__(self, players, *blinds, ante=0):
        self.players = [None for _ in range(Hand.SEATS)]
        self.player_count = 0
        for player in players:
            self.players[player.seat] = player
            self.player_count += 1

        self.deck = Card.new_deck()
        self.community_cards = list()
        self.pot = 0

        self.betting_round = 0
        self.button = Hand.count % len(self.players)
        self.absolute_min_raise = max(*_flatten(blinds), 0)
        self.reset_round()

        # Deal initial cards and put in blinds/ante
        for i in range(2):
            for player in players:
                if i == 0:
                    player.reset_cards()
                    player.stack -= ante
                    self.pot += ante
                player.deal_card(self.deck.pop(0))

        for blind in _flatten(blinds):
            player = self.players[self.action]
            player.stack -= blind
            self.pot += blind
            self.current_bet[self.action] += blind
            self.closing_action = self.action
            self.action = self.next_player() 
            
        # Initialize hand log -- HANDLE WITH LOG CLASS??
        Hand.count += 1
        self.log = f'Hand #{Hand.count} is being delt to {len(self.players)} players.'


    # Move the "action" onto the next player 
    def next_player(self, button=None):
        if button != None:
            seat = (button + 1) % len(self.players)
        else:
            seat = (self.action + 1) % len(self.players)
        if self.players[seat] == None:
            return self.next_player(seat)
        return seat
    

    def previous_player(self, button=None):
        if button != None:
            seat = (button - 1) % len(self.players)
        else:
            seat = (self.action - 1) % len(self.players)
        if self.players[seat] == None:
            return self.previous_player(seat)
        return seat


    # Reset variables for a new round of betting
    def reset_round(self):
        self.action = self.next_player(self.button)
        self.closing_action = self.previous_player()
        self.current_bet = [0 for _ in self.players]
        self.relative_min_raise = self.absolute_min_raise
        Player.community_cards = self.community_cards


    def progress_game(self):
        self.betting_round += 1
        if self.betting_round == Hand.SHOWDOWN:
            self.showdown()
        else:
            self.deck.pop(0)
            if self.betting_round == Hand.FLOP:
                for _ in range(3):
                    self.community_cards.append(self.deck.pop(0))
            else:
                self.community_cards.append(self.deck.pop(0))
            self.reset_round()
            


    # NEED LOGGING FOR HAND AND PLAYER
    def bet(self, amount=0):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise
        if player.stack > call_price:
            amount = max(amount, min(min_raise, player.stack))
            player.stack -= amount
            self.pot += amount
            self.current_bet[self.action] += amount 
            self.relative_min_raise = amount - call_price
            self.closing_action = self.previous_player()
            self.action = self.next_player() 
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

            if self.closing_action == self.action:
                self.progress_game() 
            else:
                self.action = self.next_player() 
        else:
            self.fold()

        
    def fold(self):
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if call_price > 0:
            self.players[self.action] = None
            self.player_count -= 1
            if self.player_count <= 1:
                self.showdown()
                return None
        if self.closing_action == self.action:
            self.progress_game() 
        else:
            self.action = self.next_player() 


    def showdown(self):
        self.betting_round = Hand.SHOWDOWN
        #showdown_players = [player in self.players if player != None]
        self.winner = max(self.players)
        self.winner.stack += self.pot
        
    

    @staticmethod
    def _chip_map(app, seat):
        map = [((1/2)*app.width, (2/3)*app.height, 's'), 
               ((1/4)*app.width, (2/3)*app.height, 'sw'),
               ((1/8)*app.width, (5/12)*app.height, 'w'),
               ((1/4)*app.width, (1/6)*app.height, 'nw'),
               ((1/2)*app.width, (1/6)*app.height, 'n'),
               ((3/4)*app.width, (1/6)*app.height, 'ne'),
               ((7/8)*app.width, (5/12)*app.height, 'e'),
               ((3/4)*app.width, (2/3)*app.height, 'se'),]
        return map[seat]


    def _draw_community_cards(self, app, canvas):
        padding = 10
        if self.betting_round > 0:
            sprite = self.community_cards[0].sprite()
            scaling_factor = app.height / 8 / sprite.size[1]
            sprite_x = int(sprite.size[0] * scaling_factor)
            sprite_y = int(sprite.size[1] * scaling_factor)
            for i in range(len(self.community_cards)):
                card = self.community_cards[i].sprite().resize((sprite_x, sprite_y))
                x_pos = app.width/2 + (i - 2) * (sprite_x + padding)
                canvas.create_image(x_pos, (5/12)*app.height, image=ImageTk.PhotoImage(card))
        canvas.create_text(app.width/2, (23/48)*app.height + 2*padding, text=f'Pot: {self.pot}', font='Helvetica 16 bold')
    

    def draw_cards(self, app, canvas):
        self._draw_community_cards(app, canvas)
        for player in self.players:
            if player != None:
                if self.betting_round == Hand.SHOWDOWN:
                    player._draw_player_info(app, canvas, False)  
                else:
                    player._draw_player_info(app, canvas, not player.is_user(), player.seat == self.action)


    def draw_chips(self, app, canvas):
        x, y, anchor = Hand._chip_map(app, self.button)
        scaling_factor = app.height / 32 / Hand.button_sprite.size[1]
        button_size = int(Hand.button_sprite.size[0] * scaling_factor)
        button_sprite = Hand.button_sprite.resize((button_size, button_size))
        canvas.create_image(x, y, image=ImageTk.PhotoImage(button_sprite), anchor=anchor)


    def init_user_controls(self, app):
        padding = 50
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise

        button_coords = [[None]*2, [None]*3]
        for i in range(len(button_coords)):
            button_width = app.width//3//len(button_coords[i]) + padding
            for j in range(len(button_coords[i])):
                button_coords[i][j] = (padding + j*button_width, (5/6)*app.height + padding, 0 + (j+1)*button_width, app.height - padding)

        self.buttons = [AidanButton(button_coords[0][0], text='Check', function=self.call),
                   AidanButton(button_coords[0][1], function=self.bet, parameters=min_raise),
                   AidanButton(button_coords[1][0], text='Fold', function=self.fold),
                   AidanButton(button_coords[1][1], function=self.call),
                   AidanButton(button_coords[1][2], function=self.bet, parameters=min_raise)]
        
        self.update_user_controls()


    def update_user_controls(self):
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise
        self.buttons[1].text = f'Bet {min(min_raise, player.stack)}'
        self.buttons[3].text = f'Call {min(call_price, player.stack)}'
        self.buttons[4].text = f'Raise {min(min_raise, player.stack)}'

        if call_price == 0:
            for i in range(2):
                self.buttons[i].turn_on()
            for j in range(2,len(self.buttons)):
                self.buttons[j].turn_off()
        else:
            for i in range(2):
                self.buttons[i].turn_off()
            for j in range(2,len(self.buttons)):
                self.buttons[j].turn_on()


    def __repr__(self):
        output = f'Pot: {self.pot} Board: {self.community_cards}'
        for i in range(len(self.players)):
            output += f'\n{self.players[i]}'
            if self.players[i] != None:
                if i == self.button: output += ' BUTTON'
                if i == self.action: output += ' <- ACTION'
        return output

    
class Player(object):
    community_cards = list()

    def __init__(self, stack, seat, user=False):
        self.stack = stack
        self.seat = seat
        self.hole_cards = list()
        self.user = user

    def is_user(self):
        return self.user

    def deal_card(self, card):
        self.hole_cards.append(card)
        self.hole_cards.sort(reverse=True)

    def __eq__(self, other):
        if isinstance(other, Player):
            return PokerHand(Player.community_cards, self.hole_cards) == PokerHand(Player.community_cards, self.hole_cards)

    def __lt__(self, other):
        if isinstance(other, Player):
            return PokerHand(Player.community_cards, self.hole_cards) < PokerHand(Player.community_cards, self.hole_cards)

    def __le__(self, other):
        if isinstance(other, Player):
            return PokerHand(Player.community_cards, self.hole_cards) <= PokerHand(Player.community_cards, self.hole_cards)

    def __gt__(self, other):
        if isinstance(other, Player):
            return PokerHand(Player.community_cards, self.hole_cards) > PokerHand(Player.community_cards, self.hole_cards)

    def __ge__(self, other):
        if isinstance(other, Player):
            return PokerHand(Player.community_cards, self.hole_cards) >= PokerHand(Player.community_cards, self.hole_cards)

    def reset_cards(self):
        self.hole_cards = list()

    def _seat_map(self, app):
        map = [((1/2)*app.width, (2/3)*app.height, 'n'), 
               ((1/4)*app.width, (2/3)*app.height, 'ne'),
               ((1/8)*app.width, (5/12)*app.height, 'e'),
               ((1/4)*app.width, (1/6)*app.height, 'se'),
               ((1/2)*app.width, (1/6)*app.height, 's'),
               ((3/4)*app.width, (1/6)*app.height, 'sw'),
               ((7/8)*app.width, (5/12)*app.height, 'w'),
               ((3/4)*app.width, (2/3)*app.height, 'nw'),]
        return map[self.seat]

    def _draw_player_info(self, app, canvas, face_down=True, indicator=False):
        x, y, anchor = self._seat_map(app)
        padding = 10
        sprite = self.hole_cards[0].sprite()
        scaling_factor = app.height / 8 / sprite.size[1]
        sprite_x = int(sprite.size[0] * scaling_factor)
        sprite_y = int(sprite.size[1] * scaling_factor)
        
        card1 = self.hole_cards[0].sprite(face_down).resize((sprite_x, sprite_y))
        card2 = self.hole_cards[1].sprite(face_down).resize((sprite_x, sprite_y))
        canvas.create_image(x - (sprite_x/2 + padding), y, image=ImageTk.PhotoImage(card1))#, anchor=anchor)
        canvas.create_image(x + (sprite_x/2 + padding), y, image=ImageTk.PhotoImage(card2))#, anchor=anchor)
        
        if indicator:
            outline = 'yellow'
        else:
            outline = 'black'
        stack_box = (x - (sprite_x + padding), y + sprite_y/2 + padding,
                     x + (sprite_x + padding), y + sprite_y/2 + 3*padding)
        canvas.create_rectangle(stack_box, fill='white', width=3, outline=outline)
        canvas.create_text(x, y + 2*padding + sprite_y/2, text=(self.stack), font='Helvetica 16 bold')
        

    def __repr__(self):
        return f'Player(Seat: {self.seat}, Stack: {self.stack}, Cards: {self.hole_cards})'


def draw_table(app, canvas):
    thickness = 10
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
    canvas.create_line(top_rail, width=thickness)
    canvas.create_line(bottom_rail, width=thickness)
    canvas.create_arc(left_rail, width=thickness, start=90, extent=180, style=ARC)
    canvas.create_arc(right_rail, width=thickness, start=90, extent=-180, style=ARC)


players = [Player(100, 0, True), Player(100, 1)]
hand = Hand(players, 5, 10)

hand.progress_game()
hand.progress_game()
hand.progress_game()
print(hand.community_cards)
for player in hand.players:
    if player != None:
        print('hole', player.hole_cards)
        PokerHand(Player.community_cards, player.hole_cards)
print(max(hand.players))