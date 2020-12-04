from cmu_112_graphics import *
from aidan_graphics import AidanButton

from texas_holdem import *
import random


class TitleScreenMode(Mode):
    def appStarted(self):
        start_coords = (self.width/3, self.height/3, 2*self.width/3, self.height/2)
        self.buttons = [AidanButton(start_coords, text='Start Game', font=self.app.medium_font, function=self.app.setActiveMode, parameters=self.app.game)]
        self.background = self.loadImage('resources/aces.png').convert("RGB").resize((self.width, self.height))

    def mouseMoved(self, event):
        for button in self.buttons:
            button.update_hovering(event)
    
    def mouseDragged(self, event):
        for button in self.buttons:
            button.update_hovering(event)

    def mousePressed(self, event):
        for button in self.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.buttons:
            button.released()

    def redrawAll(self, canvas):
        #canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.background))
        canvas.create_text(self.width/2, self.height/6, text='Nelter', font=self.app.large_font)
        for button in self.buttons:
            button.draw(canvas)

class GameMode(Mode):
    def appStarted(self):
        self.players = []
        for i in range(8):
            self.players.append(Player(100, i))
        self.players.pop(3)
        self.hand1 = Hand(self.players, 0, 5, 10)
        self.hand1.progress_game()
        self.hand1.progress_game()
        self.hand1.progress_game()
        self.buttons = []

    def mouseMoved(self, event):
        for button in self.buttons:
            button.update_hovering(event)
    
    def mouseDragged(self, event):
        for button in self.buttons:
            button.update_hovering(event)

    def mousePressed(self, event):
        for button in self.buttons:
            button.update_pressed(event)

    def mouseReleased(self, event):
        for button in self.buttons:
            button.released()

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='RoyalBlue4')
        draw_table(self, canvas)
        self.hand1.draw_community_cards(self, canvas)
        for player in self.players:
            player.draw_hole_cards(self, canvas)
        
        



class NeLter(ModalApp):
    def appStarted(app):
        app.title_screen = TitleScreenMode()
        app.game = GameMode()
        app.margin = 10
        app.font_family = 'Helvetica'
        app.small_font = f'{app.font_family} {app.height//30} bold'
        app.medium_font = f'{app.font_family} {app.height//20} bold'
        app.large_font = f'{app.font_family} {app.height//10} bold'

        app.setActiveMode(app.title_screen)

app = NeLter(width=1600, height=1000)