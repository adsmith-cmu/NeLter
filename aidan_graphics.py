from cmu_112_graphics import *
from tkinter import _flatten

class AidanButton(object):
    def __init__(self, *args, **kwargs):
        self.coords = _flatten(args)
        self.color = kwargs.get('color', 'white')
        self.border_size = kwargs.get('border_size', 5)

        self.text = kwargs.get('text', '')
        font_family = kwargs.get('font_family', 'Helvetica')
        font_size = kwargs.get('font_size', 16)
        self.font = kwargs.get('font', f'{font_family} {font_size} bold')

        self.function = kwargs.get('function', lambda: None)
        self.parameters = kwargs.get('parameters', None)
        self.pressed_effect = kwargs.get('press_effect', True)
        self.pressed = False
        self.hover_effect = kwargs.get('hover_effect', True)
        self.hovering = False
    

    def update_hovering(self, event):
        x0, y0, x1, y1 = self.coords
        self.hovering = (x0 < event.x < x1) and (y0 < event.y < y1)


    def update_pressed(self, event):
        if self.hovering:
            self.pressed = True


    def draw(self, canvas):
        canvas.create_rectangle(self.coords, fill=self.color, width=self.border_size)
        canvas.create_text(_midpoint(self.coords), text=self.text, font=self.font)

        if self.pressed_effect and self.pressed:
            canvas.create_rectangle(self.coords, width=1.5*self.border_size)
        elif self.hover_effect and self.hovering:
            pass

    
    def released(self):
        if self.pressed and self.hovering:
            if self.parameters is None:
                self.function()
            elif isinstance(self.parameters, (list, tuple)):
                self.function(*_flatten(self.parameters))
            else:
                self.function(self.parameters)
        self.pressed = False


def _midpoint(*coordinates):
    coordinates = _flatten(coordinates)
    if len(coordinates) % 2 == 1 or len(coordinates) == 0:
        raise TypeError(f'midpoint expected 2*k arguments got {len(coordinates)}')
    x_coordinates = coordinates[0::2]
    y_coordinates = coordinates[1::2]
    return sum(x_coordinates)/len(x_coordinates), sum(y_coordinates)/len(y_coordinates)
