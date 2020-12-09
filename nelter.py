from cmu_112_graphics import *
from aidan_graphics import *

from texas_holdem import *
import random, time

# Background taken from https://opengameart.org/content/boardgame-pack

class TitleScreenMode(Mode):
    def appStarted(self):
        start_coords = (self.width/3, self.height/3, 2*self.width/3, self.height/2)
        help_coords = (self.width/3, self.height/2 + self.app.default.padding, 2*self.width/3, 2*self.height/3 + self.app.default.padding)
        quit_coords = (10, 10, self.width/6, self.height/10)
        self.buttons = [AidanButton(start_coords, text='Start Game', font=self.app.default.medium_font, function=self.app.setActiveMode, parameters=self.app.game),
                        AidanButton(help_coords, text='Help', font=self.app.default.medium_font, function=self.app.setActiveMode, parameters=self.app.help),
                        AidanButton(quit_coords, text='Quit', font=self.app.default.medium_font, function=self.app.quit)]
        self.background = format_image(self.width, self.height, self.loadImage('resources/aces.jpg'))

    def mousePressed(self, event):
        for button in self.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.buttons:
            button.released(event)

    def redrawAll(self, canvas):
        canvas.create_image(self.width/2, self.height/2, image=self.background)
        canvas.create_text(self.width/2, self.height/6, text='Nelter', font=self.app.default.large_font)
        for button in self.buttons:
            button.draw(canvas)


# Background taken from https://www.pokernews.com/poker-hands.htm

class HelpMode(Mode):
    def appStarted(self):
        back_coords = [self.app.default.padding, self.app.default.padding, self.width/6, self.height/10]
        self.buttons = [AidanButton(back_coords, text='Back', font=self.app.default.medium_font, function=self.app.setActiveMode, parameters=self.app.title_screen)]
        self.background = format_image(self.width, self.height, self.loadImage('resources/hand_ranks.png'))

    def mousePressed(self, event):
        for button in self.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.buttons:
            button.released(event)

    def redrawAll(self, canvas):
        how_to_play = 'How to play:'
        how_to_play += '\n1. 4 rounds of no limit betting before showdown (use arrow keys to adjust bet)'
        how_to_play += '\n2. Best 5 card poker combination of community and hole cards wins'
        how_to_play += '\n3. See below for hand rankings'

        canvas.create_image(self.width/2, self.height/2, image=self.background)
        canvas.create_rectangle(0, 0, self.width, self.height/4, fill='cyan', width=0)
        canvas.create_text(self.width/4, self.height/8, 
                           text=how_to_play, font=self.app.default.small_font, anchor='w')
        for button in self.buttons:
            button.draw(canvas)


class GameMode(Mode):
    def appStarted(self):
        back_coords = [10, 10, self.width/6, self.height/10]
        self.buttons = [AidanButton(back_coords, text='Back', font=self.app.default.medium_font, function=self.app.setActiveMode, parameters=self.app.title_screen)]
        self.gamers = [Player(100, 0, True)]
        for i in range(1,8):
            self.gamers.append(Player(100, i))

        self.blinds = (1,2)
        self.new_hand(self.gamers, self.blinds)
       
    def new_hand(self, players, *blinds):
        self.hand = Hand(players, *blinds)
        self.hand.init_user_controls(self)
        self.bots = [PokerBot(self.hand, player.seat) if player != None and not player.user else None for player in self.hand.players]

    def timerFired(self):
        self.hand.update_user_controls()
        if self.bots[self.hand.action] != None:
            self.bots[self.hand.action].act()

    def keyPressed(self, event):
        #self.new_hand(self.gamers, self.blinds)
        if self.hand.betting_round == Hand.SHOWDOWN:
            self.new_hand(self.gamers, self.blinds)
        elif event.key == 'Up':
            print('up')
            self.hand.amount += self.hand.absolute_min_raise
            print(self.hand.amount)
        elif event.key == 'Down':
            print('down')
            self.hand.amount -= self.hand.absolute_min_raise
            print(self.hand.amount)

    def mousePressed(self, event):
        for button in self.hand.buttons:
            button.update_pressed(event)
        for button in self.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.hand.buttons:
            button.released(event)
        for button in self.buttons:
            button.released(event)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='RoyalBlue4')
        draw_table(self, canvas)
        self.hand.draw_cards(self, canvas)
        self.hand.draw_chips(self, canvas)
        for button in self.hand.buttons:
            button.draw(canvas)
        for button in self.buttons:
            button.draw(canvas)
        


class Nelter(ModalApp):
    def appStarted(app):
        app.default = GraphicsDefaults(app)
        app.title_screen = TitleScreenMode()
        app.help = HelpMode()
        app.game = GameMode()
        #app.timerDelay = 1000
        app.setActiveMode(app.title_screen)

app = Nelter(width=1720, height=990)