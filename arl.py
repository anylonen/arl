#!/usr/bin/env python

import os
import libtcodpy as libtcod
from game import gamemap
from game import player

class ARL(object):
    """The main class to handle stuff."""
    
    def __init__(self):
        """ Constants """
        self.window_width = 80
        self.window_height = 50
        
        self.map_width = 80
        self.map_height = 50
        self.max_amount_of_rooms_in_map = 10
    
        self.do_movement = {}
        self.do_action = {}
    
        self.key_bindings = {}
        self.keys = {}
        
        self.player = player.Player((1, 1))
        
        self.level_map = None
        self.fov_map = None
        self.fov_radius = 0
        self.fov_colors = {}

        self.fov_algorithm = 0  #default FOV algorithm
        self.fov_radius = 10
        self.fov_light_walls = True  #light walls or not

        self.font = None
        self.console = None

    def initialize(self):
        """ General initialization. """
        self.font = os.path.join("data/fonts", "arial12x12.png")
        libtcod.console_set_custom_font(self.font, libtcod.FONT_LAYOUT_TCOD | libtcod.FONT_TYPE_GREYSCALE)
        libtcod.console_init_root(self.map_width, self.map_height, "Anylo's RogueLike", False)
        self.console = libtcod.console_new(self.map_width, self.map_height)
        
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
        
        """ Creating map, 80x50, max 25 rooms with min room size 5 and max size 12 """ 
        gen = gamemap.MapGenerator(self.window_width, self.window_height, self.max_amount_of_rooms_in_map, 5, 12)
        
        self.level_map = gen.create_map()
        self.player.position = gen.player_start_point
        px, py = self.player.position
        
        libtcod.console_clear(0)
        libtcod.console_set_foreground_color(0, libtcod.white)
        libtcod.console_set_foreground_color(0, libtcod.black)
        libtcod.console_put_char(0, px, py, '@', libtcod.BKGND_NONE)

        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.level_map[x][y] == '=':
                    libtcod.console_put_char(0, x, y, libtcod.CHAR_DHLINE, libtcod.BKGND_NONE)
        
    def init_fov(self):
        self.fov_map = libtcod.map_new(self.map_width, self.map_height)
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                libtcod.map_set_properties(self.fov_map, x, y, 
                                           not self.level_map[x][y].tile_property["blocks_walking"], 
                                           not self.level_map[x][y].tile_property["blocks_visibility"])
                    
        self.fov_colors = {
                           "dark wall":    libtcod.Color(10, 10, 10),
                           "light wall":   libtcod.Color(60, 35, 0),
                           "dark ground":  libtcod.Color(100, 100, 100),
                           "light ground": libtcod.Color(145, 120, 90)
                           }
        
    
    def get_key(self, key):
        if key.vk == libtcod.KEY_CHAR:
            return chr(key.c)
        else:
            return key.vk
    
    def update(self, key):
        key = self.get_key(key)
        if key in self.keys:
            do_type, params = self.keys[key]

            if do_type == "movement":
                dx, dy = params
                px, py = self.player.position
                x, y = (dx+px, dy+py)
                
                if not self.level_map[x][y].tile_property["blocks_walking"]:
                    libtcod.console_put_char(self.console, px, py, ' ', libtcod.BKGND_NONE)
                    self.player.position = (x, y)
                    print self.player.position
                else:
                    print "Cannot go to %d %d" % (x, y)
                
            if do_type == "action":
                params()
                
    def draw(self):
        self.recompute_field_of_vision()
        
        for y in range(self.window_height):
            for x in range(self.window_width):
                affect, cell = 'dark', 'ground'
            
                if libtcod.map_is_in_fov(self.fov_map, x, y): 
                    affect = 'light'
                if self.level_map[x][y].tile_property["blocks_walking"]:
                    cell = 'wall'
                
                color = self.fov_colors['%s %s' % (affect, cell)]
                libtcod.console_set_back(self.console, x, y, color, libtcod.BKGND_SET)
        
        px, py = self.player.position
        libtcod.console_set_foreground_color(self.console, libtcod.Color(200, 200, 200))
        libtcod.console_put_char(self.console, px, py, "@", libtcod.BKGND_NONE)
        
        libtcod.console_blit(self.console, 0, 0, self.window_width, self.window_height, 0, 0, 0)
        
    def recompute_field_of_vision(self):
        px, py = self.player.position
        libtcod.map_compute_fov(self.fov_map, px, py, self.fov_radius, self.fov_light_walls, self.fov_algorithm)

def main():
    # TODO: Check main loop
    
    theGame = ARL()
    theGame.initialize()
    
    while not libtcod.console_is_window_closed():
        theGame.draw()
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        theGame.update(key)
        if key.vk == libtcod.KEY_ESCAPE:
            break

if __name__ == "__main__":
    main()

