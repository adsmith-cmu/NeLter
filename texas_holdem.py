from cards import Card

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
        self.absolute_min_raise = max(*blinds, ante)
        self.reset_round()

        # Deal initial cards and put in blinds/ante
        for i in range(2):
            for player in self.players:
                if i == 0:
                    player.stack -= ante
                    self.pot += ante
                player.deal_card(self.deck.pop(0))
                self.next_player()

        for blind in blinds:
            self.bet(blind)
            self.closing_action = self.action
            self.next_player()


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
        self.current_wager = self.absolute_min_raise
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


    def bet(self, wager):
        player = self.players[self.action]
        wager = min(wager, player.stack)
        player.stack -= wager
        self.pot += wager


    # NEED LOGGING FOR HAND AND PLAYER
    def act(self, wager):
        # Player Raises
        if wager >= self.current_wager + self.relative_min_raise:
            self.bet(wager)
            self.relative_min_raise = 2*(wager - self.current_wager)
            self.closing_action = self.action
            self.next_player()
            print(f'Player: {self.action} raises')
        else:
            # Player Folds
            if wager < self.current_wager:
                self.players.pop(self.action)
                print(f'Player: {self.action} folds')
            # Player Calls or Checks
            else:
                self.bet(self.current_wager)
                print(f'Player: {self.action} calls')

            if self.closing_action == self.action:
                self.progress_game() 
            else:
                self.next_player() 


    def showdown(self):
        return None
    
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

    def muck(self):
        self.hole_cards = list()

    def __repr__(self):
        return f'Player(Seat: {self.seat}, Stack: {self.stack}, Cards: {self.hole_cards})'

players = [Player(100, 1), Player(100, 0)]
hand1 = Hand(players, 0, 5, 10)
print(hand1.absolute_min_raise)
#hand1.act(5)
#hand1.act(5)
print(hand1)
