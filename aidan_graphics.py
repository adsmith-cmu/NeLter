from cmu_112_graphics import *
from tkinter import _flatten


def _midpoint(*coordinates):
    coordinates = _flatten(coordinates)
    if len(coordinates) % 2 == 1 or len(coordinates) == 0:
        raise TypeError(f'midpoint expected 2*k arguments got {len(coordinates)}')
    x_coordinates = coordinates[0::2]
    y_coordinates = coordinates[1::2]
    return sum(x_coordinates)/len(x_coordinates), sum(y_coordinates)/len(y_coordinates)


# Adapted from https://www.kosbie.net/cmu/fall-19/15-112/notes/notes-animations-part2.html#cachingPhotoImages
def format_image(width, height, image):
        if ('cached_image' not in image.__dict__):
            image.cached_image = ImageTk.PhotoImage(image.resize((width, height)))
        return image.cached_image


class GraphicsDefaults(object):
    def __init__(self, app, **kwargs):
        self.margin = 10
        self.padding = 10
        self.font_family = kwargs.get('font_family', 'Helvetica')
        self.small_font = f'{self.font_family} {app.height//30} bold'
        self.medium_font = f'{self.font_family} {app.height//20} bold'
        self.large_font = f'{self.font_family} {app.height//10} bold'


class AidanButton(object):
    def __init__(self, *args, **kwargs):
        self.on = True
        self.coords = _flatten(args)
        self.color = kwargs.get('color', 'white')
        self.border_size = kwargs.get('border_size', 5)

        self.text = kwargs.get('text', '')
        font_family = kwargs.get('font_family', 'Helvetica')
        font_size = kwargs.get('font_size', int((self.coords[3]-self.coords[1])/2))
        self.font = kwargs.get('font', f'{font_family} {font_size} bold')

        self.function = kwargs.get('function', lambda: None)
        self.parameters = kwargs.get('parameters', None)
        self.pressed_effect = kwargs.get('press_effect', True)
        self.pressed = False
    

    def turn_on(self):
        self.pressed = False
        self.on = True


    def turn_off(self):
        self.pressed = False
        self.on = False


    def update_pressed(self, event):
        x0, y0, x1, y1 = self.coords
        if (x0 < event.x < x1) and (y0 < event.y < y1):
            self.pressed = True

    
    def released(self, event):
        if self.on:
            x0, y0, x1, y1 = self.coords
            if self.pressed and (x0 < event.x < x1) and (y0 < event.y < y1):
                if self.parameters is None:
                    self.function()
                elif isinstance(self.parameters, (list, tuple)):
                    self.function(*_flatten(self.parameters))
                else:
                    self.function(self.parameters)
            self.pressed = False


    def draw(self, canvas):
        if self.on:
            canvas.create_rectangle(self.coords, fill=self.color, width=self.border_size)
            canvas.create_text(_midpoint(self.coords), text=self.text, font=self.font)

            if self.pressed_effect and self.pressed:
                canvas.create_rectangle(self.coords, width=1.5*self.border_size)

