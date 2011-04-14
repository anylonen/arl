import libtcodpy as libtcod

class GameObject():
    """ This is a generic class for different game objects. """
    def __init__(self, position, character, color, blocks_movement = False):
        self.position = position
        self.character = character
        self.color = color
        
    def draw(self, console):
        x, y = self.position
        libtcod.console_set_foreground_color(console, self.color)
        libtcod.console_put_char(console, x, y, self.character, libtcod.BKGND_NONE)

class Rectangle():
    """ Rectangle class. Used for room creations etc. """
    
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        
    def get_rectangle(self):
        return (self.x1, self.y1, self.x2, self.y2)
    
    def get_center(self):
        return (((self.x1 + self.x2) / 2), ((self.y1 + self.y2) / 2))
    
    def does_intersect(self, otherRectangle):
        return (self.x1 <= otherRectangle.x2 and self.x2 >= otherRectangle.x1 and
                self.y1 <= otherRectangle.y2 and self.y2 >= otherRectangle.y1)

