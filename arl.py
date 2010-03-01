#!/usr/bin/env python

import os
import libtcodpy as libtcod
from game import map
from game import player

class arl(object):
    """The main class to handle stuff."""
    
    def __init__(self):
        """ Constants """
        self.WINDOW_WIDTH = 20
        self.WINDOW_HEIGHT = 20
    
        self.do_movement = {}
        self.do_action = {}
    
        self.key_bindings = {}
        
        self.player = player.Player((1,1))
        
        self.level_map = None
        self.fov_map = None
        self.fov_radius = 0
        self.fov_colors = {}

    def init(self):
        self.font = os.path.join("data/fonts", "arial12x12.png")
        libtcod.console_set_custom_font(self.font, libtcod.FONT_LAYOUT_TCOD | libtcod.FONT_TYPE_GREYSCALE)
        libtcod.console_init_root(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Anylo's RogueLike", False)
        
        self.init_movement()
        self.init_action()
        self.init_bindings()
        self.init_map()
        self.init_fov()

    def do_nothing(self):
        print "Doing nothing"

    def init_movement(self):
        self.do_movement = {
                       "north":     (0, -1),
                       "northeast": (1, -1),
                       "east":      (1, 0),
                       "southeast": (1, 1),
                       "south":     (0, 1),
                       "southwest": (-1, 1),
                       "west":      (-1, 0),
                       "northwest": (-1, -1)
                       }
    
    def init_action(self):
        self.do_action = {
                          "nothing":    self.do_nothing
                          }

    def init_bindings(self):
        self.keys = {
                    libtcod.KEY_KP8:    ("movement", self.do_movement["north"]),
                    libtcod.KEY_KP9:    ("movement", self.do_movement["northeast"]),
                    libtcod.KEY_KP6:    ("movement", self.do_movement["east"]),
                    libtcod.KEY_KP3:    ("movement", self.do_movement["southeast"]),
                    libtcod.KEY_KP2:    ("movement", self.do_movement["south"]),
                    libtcod.KEY_KP1:    ("movement", self.do_movement["southwest"]),
                    libtcod.KEY_KP4:    ("movement", self.do_movement["west"]),
                    libtcod.KEY_KP7:    ("movement", self.do_movement["northwest"]),
                    libtcod.KEY_KP5:    ("action",  self.do_action["nothing"])
                    }
    
    def init_map(self):
        px, py = self.player.Position
        
        self.level_map = map.generate_map()
        
        libtcod.console_clear(0)
        libtcod.console_set_foreground_color(0, libtcod.white)
        libtcod.console_set_foreground_color(0, libtcod.black)
        libtcod.console_put_char(0, px, py, '@', libtcod.BKGND_NONE)

        for y in range(self.WINDOW_HEIGHT):
            for x in range(self.WINDOW_WIDTH):
                if self.level_map[y][x] == '=':
                    libtcod.console_put_char(0, x, y, libtcod.CHAR_DHLINE, libtcod.BKGND_NONE)
        
    def init_fov(self):
        self.fov_radius = 3
        self.fov_map = libtcod.map_new(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        for y in range(self.WINDOW_HEIGHT):
            for x in range(self.WINDOW_WIDTH):
                if self.level_map[y][x] == '.':
                    libtcod.map_set_properties(self.fov_map, x, y, True, True)
                elif self.level_map[y][x] == '=':
                    libtcod.map_set_properties(self.fov_map, x, y, True, False)
                    
        self.fov_colors = {
                           "dark wall":    libtcod.Color(0, 0, 100),
                           "light wall":   libtcod.Color(130, 110, 50),
                           "dark ground":  libtcod.Color(50, 50, 150),
                           "light ground": libtcod.Color(200, 180, 50)
                           }
        
    
    def get_key(self, key):
        if key.vk == libtcod.KEY_CHAR:
                return chr(key.c)
        else:
            return key.vk
    
    def update(self, key):
        key = self.get_key(key)
        if key in self.keys:
            type, params = self.keys[key]

            if type == "movement":
                dx, dy = params
                px, py = self.player.Position
                x, y = (dx+px, dy+py)
                
                if self.level_map[y][x] == ".":
                    libtcod.console_put_char(0, px, py, ".", libtcod.BKGND_NONE)
                    libtcod.console_put_char(0, x, y, '@', libtcod.BKGND_NONE)
                    self.player.Position = (x, y)
                    print self.player.Position
                else:
                    print "Cannot go to %d %d" % (x, y)
                
            if type == "action":
                params()
                
    def draw(self):
        px, py = self.player.Position
        libtcod.map_compute_fov(self.fov_map, px, py, self.fov_radius, True)
        for y in range(self.WINDOW_HEIGHT):
            for x in range(self.WINDOW_WIDTH):
                affect, cell = 'dark', 'ground'
            
                if libtcod.map_is_in_fov(self.fov_map, x, y): affect = 'light'
                if (self.level_map[y][x] == '#'): cell = 'wall'
                color = self.fov_colors['%s %s' % (affect, cell)]
                libtcod.console_set_back(0, x, y, color, libtcod.BKGND_SET)

def main():
    theGame = arl()
    theGame.init()
    
    while not libtcod.console_is_window_closed():
        theGame.draw()
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        theGame.update(key)
        if key.vk == libtcod.KEY_ESCAPE:
            break

if __name__ == "__main__":
    main()

