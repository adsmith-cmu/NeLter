from cmu_112_graphics import *
from aidan_graphics import *

from texas_holdem import *
import random, time

# Background taken from https://opengameart.org/content/boardgame-pack

class TitleScreenMode(Mode):
    def appStarted(self):
        start_coords = (self.width/3, self.height/3, 2*self.width/3, self.height/2)
        self.buttons = [AidanButton(start_coords, text='Start Game', font=self.app.default.medium_font, function=self.app.setActiveMode, parameters=self.app.game)]
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

class GameMode(Mode):
    def appStarted(self):
        self.gamers = [Player(100, 0, True)]
        for i in range(1,8):
            self.gamers.append(Player(100, i))
        self.blinds = (5,10)
        self.new_hand(self.gamers, self.blinds)
       
    def new_hand(self, players, *blinds):
        self.hand = Hand(players, *blinds)
        self.hand.init_user_controls(self)

    def timerFired(self):
        self.hand.update_user_controls()


    def keyPressed(self, event):
        if self.hand.betting_round == Hand.SHOWDOWN:
            self.new_hand(self.gamers, self.blinds)

    def mousePressed(self, event):
        for button in self.hand.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.hand.buttons:
            button.released(event)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='RoyalBlue4')
        draw_table(self, canvas)
        self.hand.draw_cards(self, canvas)
        self.hand.draw_chips(self, canvas)
        for button in self.hand.buttons:
            button.draw(canvas)
        


class Nelter(ModalApp):
    def appStarted(app):
        app.default = GraphicsDefaults(app)
        app.title_screen = TitleScreenMode()
        app.game = GameMode()
        #app.timerDelay = 1000
        app.setActiveMode(app.title_screen)

app = Nelter(width=1600, height=900)