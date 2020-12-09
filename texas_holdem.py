from cards import *
from tkinter import ARC, _flatten
from PIL import Image, ImageTk
from aidan_graphics import *
from npc_controls import *

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

        self.deck = Card.new_deck()
        self.community_cards = list()
        self.pot = 0

        self.betting_round = 0
        self.button = players[Hand.count % len(players)].seat
        self.absolute_min_raise = max(*_flatten(blinds), 0)

        for player in players:
            if player.stack > self.absolute_min_raise:
                self.players[player.seat] = player
                self.player_count += 1
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
        if self.players[seat] == None or self.players[seat].stack == 0:
            return self.next_player(seat)
        return seat
    

    def previous_player(self, button=None):
        if button != None:
            seat = (button - 1) % len(self.players)
        else:
            seat = (self.action - 1) % len(self.players)
        if self.players[seat] == None or self.players[seat].stack == 0:
            return self.previous_player(seat)
        return seat


    # Reset variables for a new round of betting
    def reset_round(self):
        self.action = self.next_player(self.button)
        self.closing_action = self.previous_player()
        self.current_bet = [0 for _ in self.players]
        self.relative_min_raise = self.absolute_min_raise
        Player.community_cards = self.community_cards
        Range.community_cards = self.community_cards


    def progress_game(self):
        self.betting_round += 1
        if self.betting_round == Hand.SHOWDOWN:
            self.showdown()
        else:
            for player in self.players:
                if player != None and player.stack == 0:
                    player.sidepot += self.player_count * self.current_bet[player.seat]
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
            if player.stack < min_raise:
                amount = player.stack
                player.sidepot = self.pot - sum(self.current_bet)
                player.stack -= amount
                self.pot += amount
                self.current_bet[self.action] += amount
                self.player_count -= 1

                if self.closing_action == self.action:
                    self.progress_game() 
                else:
                    self.action = self.next_player() 
            else:
                amount = max(amount, min_raise)
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
        if player.stack > 0:
            if player.stack < call_price:
                amount = player.stack
                player.sidepot += self.pot - sum(self.current_bet)
            else:
                amount = call_price
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
        player = self.players[self.action]
        call_price = max(self.current_bet) - self.current_bet[self.action]
        if call_price > 0 and player.stack > 0:
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
        showdown_players = [player for player in self.players if player != None]
        self._distribute_pot(showdown_players)


    def _distribute_pot(self, showdown_players):
        self.winner = max(showdown_players)
        if self.winner.sidepot == 0:
            self.winner.stack += self.pot
        else:
            self.winner.stack += self.winner.sidepot
            self.pot -= self.winner.sidepot
            showdown_players.remove(self.winner)
            self._distribute_pot(showdown_players)
            

    @staticmethod
    def _chip_map(app, seat):
        map = [((1/2)*app.width, (27/48)*app.height, 's', 'n'), 
               ((1/4)*app.width, (27/48)*app.height, 'sw', 'ne'),
               ((3/16)*app.width, (5/12)*app.height, 'w', 'e'),
               ((1/4)*app.width, (13/48)*app.height, 'nw', 'se'),
               ((1/2)*app.width, (13/48)*app.height, 'n', 's'),
               ((3/4)*app.width, (13/48)*app.height, 'ne', 'sw'),
               ((13/16)*app.width, (5/12)*app.height, 'e', 'w'),
               ((3/4)*app.width, (27/48)*app.height, 'se', 'nw'),]
        return map[seat]


    def _draw_community_cards(self, app, canvas):
        padding = 10
        if len(self.community_cards) > 0:
            sprite = self.community_cards[0].sprite()
            scaling_factor = app.height / 8 / sprite.size[1]
            sprite_x = int(sprite.size[0] * scaling_factor)
            sprite_y = int(sprite.size[1] * scaling_factor)
            for i in range(len(self.community_cards)):
                card = format_image(sprite_x, sprite_y, self.community_cards[i].sprite())
                x_pos = app.width/2 + (i - 2) * (sprite_x + padding)
                canvas.create_image(x_pos, (5/12)*app.height, image=card)
        canvas.create_text(app.width/2, (23/48)*app.height + 2*padding, text=f'Pot: {self.pot}', font='Helvetica 16 bold')
    

    def draw_cards(self, app, canvas):
        self._draw_community_cards(app, canvas)
        for player in self.players:
            if player != None:
                if self.betting_round == Hand.SHOWDOWN:
                    player._draw_player_info(app, canvas, False)  
                else:
                    player._draw_player_info(app, canvas, not player.user, player.seat == self.action)
        if self.betting_round == Hand.SHOWDOWN:
            canvas.create_text(app.width/2, (5/12)*app.height, text=f'Player {self.winner.seat} wins!', font='Helvetica 32 bold', anchor='s')
            canvas.create_text(app.width/2, (5/12)*app.height, text='Press any key to deal next hand.', font='Helvetica 32 bold', anchor='n')


    def draw_chips(self, app, canvas):
        x, y, anchor1, anchor2 = Hand._chip_map(app, self.button)
        if self.button in [0,1,7]:
            x -= (1/16)*app.width
            y += (1/48)*app.height
        elif self.button in [3,4,5]:
            x += (1/15)*app.width
            y -= (1/64)*app.height
        elif self.button == 6:
            x += (1/26)*app.width
            y -= (1/12)*app.height
        else:
            x -= (1/26)*app.width
            y -= (1/12)*app.height
        scaling_factor = app.height / 32 / Hand.button_sprite.size[1]
        button_size = int(Hand.button_sprite.size[0] * scaling_factor)
        button_sprite = format_image(button_size, button_size, Hand.button_sprite)
        canvas.create_image(x, y, image=button_sprite)
        for i in range(len(self.players)):
            if self.players[i] != None or self.current_bet[i] != 0:
                x, y, anchor1, anchor2 = Hand._chip_map(app, i)
                canvas.create_text(x, y, text=self.current_bet[i], font='Helvetica 16 bold')


    def init_user_controls(self, app):
        padding = 50
        call_price = max(self.current_bet) - self.current_bet[self.action]
        min_raise = call_price + self.relative_min_raise
        self.amount = min_raise

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
        if self.betting_round == Hand.SHOWDOWN or not player.user:
            for i in range(len(self.buttons)):
                    self.buttons[i].turn_off()
        else:
            call_price = max(self.current_bet) - self.current_bet[self.action]
            min_raise = call_price + self.relative_min_raise
            self.amount = max(self.amount, min_raise)
            self.buttons[1].parameters = min(self.amount, player.stack)
            self.buttons[4].parameters = min(self.amount, player.stack)
            self.buttons[1].text = f'Bet {self.buttons[1].parameters}'
            self.buttons[3].text = f'Call {min(call_price, player.stack)}'
            self.buttons[4].text = f'Raise {self.buttons[4].parameters}'

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
        self.sidepot = 0

    def poker_hand(self):
        return PokerHand(Player.community_cards, self.hole_cards)

    def deal_card(self, card):
        self.hole_cards.append(card)
        self.hole_cards.sort(reverse=True)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.poker_hand() == other.poker_hand()

    def __lt__(self, other):
        if isinstance(other, Player):
            return self.poker_hand() < other.poker_hand()

    def __le__(self, other):
        if isinstance(other, Player):
            return self.poker_hand() <= other.poker_hand()

    def __gt__(self, other):
        if isinstance(other, Player):
            return self.poker_hand() > other.poker_hand()

    def __ge__(self, other):
        if isinstance(other, Player):
            return self.poker_hand() >= other.poker_hand()

    def reset_cards(self):
        self.hole_cards = list()

    def _seat_map(self, app):
        map = [((1/2)*app.width, (2/3)*app.height, 'n'), 
               ((1/4)*app.width, (2/3)*app.height, 'ne'),
               ((1/10)*app.width, (5/12)*app.height, 'e'),
               ((1/4)*app.width, (1/7)*app.height, 'se'),
               ((1/2)*app.width, (1/7)*app.height, 's'),
               ((3/4)*app.width, (1/7)*app.height, 'sw'),
               ((9/10)*app.width, (5/12)*app.height, 'w'),
               ((3/4)*app.width, (2/3)*app.height, 'nw'),]
        return map[self.seat]

    def _draw_player_info(self, app, canvas, face_down=True, indicator=False):
        x, y, anchor = self._seat_map(app)
        padding = 10
        sprite = self.hole_cards[0].sprite()
        scaling_factor = app.height / 8 / sprite.size[1]
        sprite_x = int(sprite.size[0] * scaling_factor)
        sprite_y = int(sprite.size[1] * scaling_factor)
        
        card1 = format_image(sprite_x, sprite_y, self.hole_cards[0].sprite(face_down))
        card2 = format_image(sprite_x, sprite_y, self.hole_cards[1].sprite(face_down))
        canvas.create_image(x - (sprite_x/2 + padding), y, image=card1)#, anchor=anchor)
        canvas.create_image(x + (sprite_x/2 + padding), y, image=card2)#, anchor=anchor)
        
        if indicator:
            outline = 'yellow'
        else:
            outline = 'black'
        stack_box = (x - (sprite_x + padding), y + sprite_y/2 + padding,
                     x + (sprite_x + padding), y + sprite_y/2 + 3*padding)
        canvas.create_rectangle(stack_box, fill='white', width=3, outline=outline)
        canvas.create_text(x, y + 2*padding + sprite_y/2, text=f'Player {self.seat}: {self.stack}', font='Helvetica 16 bold')
        

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


class PokerBot(object):
    def __init__(self, hand, player_seat):
        self.hand = hand
        self.player = self.hand.players[player_seat]
        self.ranges = [Range(self.player.hole_cards) for player in self.hand.players if player != None and player != self.player]

    def update_ranges(self):
        for i in range(len(self.ranges)):
            if self.ranges[i] != None:
                if self.hand.players[i] is None:
                    self.ranges[i] = None
                else:
                    self.ranges[i].update(self.hand.community_cards)

    def evaluate(self):
        aggregate_rank = 0
        for i in range(len(self.ranges)):
            if self.ranges[i] != None:
                if self.hand.players[i] is None:
                    self.ranges[i] = None
                else:
                    aggregate_rank += self.ranges[i].rank_hand(self.player.hole_cards)
        return aggregate_rank / (self.hand.player_count - 1)

    def act(self):
        if self.hand.betting_round != Hand.SHOWDOWN:
            self.update_ranges()
            for i in range(len(self.ranges)):
                if self.ranges[i] != None:
                    self.ranges[i].take_top_percent(1 - (self.hand.current_bet[i]/self.hand.players[i].stack))
            eval = self.evaluate()
            if eval > 0.85: 
                stack_blinds = self.player.stack / self.hand.relative_min_raise 
                bet_amount1 = int(1 + (((1/0.85)*(eval - 0.85))**3)*(stack_blinds-1))
                bet_amount2 = int((eval/0.85)**2 * self.hand.relative_min_raise)
                if eval > 0.95:
                    self.hand.bet(bet_amount1)
                else:
                    self.hand.bet(bet_amount2)
            elif eval > 0.5: self.hand.call()
            else: self.hand.fold()

    


    