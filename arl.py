#!/usr/bin/env python

import os
import libtcodpy as libtcod
from game import gamemap
from game import player

class Panel(object):
    def __init__(self, x = 0, y = 0, width = 80, height = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.maximum_amount_of_messages = 5
        self.messages = []
        
    def add_message(self, message):
        if len(self.messages) >= self.maximum_amount_of_messages:
            self.messages.pop(0)
        self.messages.append(message)

class ARL(object):
    """The main class to handle stuff."""
    
    def __init__(self):
        """ Constants """
        self.window_width = 80
        self.window_height = 50
        
        self.map_width = 80
        self.map_height = 45
        self.max_amount_of_rooms_in_map = 10
    
        self.message_panel = Panel()
    
        self.do_movement = {}
        self.do_action = {}
    
        self.key_bindings = {}
        self.keys = {}
        
        self.player = player.Player((1, 1))
        
        self.level_map = None
        self.fov_map = None
        self.fov_radius = 0
        self.fov_colors = {}
        
        self.colors =   {
                        "dark wall":    libtcod.Color(10, 10, 10),
                        "light wall":   libtcod.Color(60, 35, 0),
                        "dark ground":  libtcod.Color(100, 100, 100),
                        "light ground": libtcod.Color(145, 120, 90)
                        }


        self.fov_algorithm = 0  #default FOV algorithm
        self.fov_radius = 10
        self.fov_light_walls = True  #light walls or not

        self.font = None
        self.console_map = None
        self.console_panel = None

    def initialize(self):
        """ General initialization. """
        self.font = os.path.join("data/fonts", "arial12x12.png")
        libtcod.console_set_custom_font(self.font, libtcod.FONT_LAYOUT_TCOD | libtcod.FONT_TYPE_GREYSCALE)
        libtcod.console_init_root(self.window_width, self.window_height, "Anylo's RogueLike", False)
        
        self.init_movement()
        self.init_action()
        self.init_bindings()
        self.init_map()
        self.init_panel()
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
        
        
    def init_panel(self):
        panel_height = 5
        
        self.message_panel.x = 0
        self.message_panel.y = self.window_height - (self.window_height - self.map_height)
        self.message_panel.width = self.window_width
        self.message_panel.height = panel_height
        
        self.console_panel = libtcod.console_new(self.message_panel.width, self.message_panel.height)
    
    def init_map(self):
        
        """ Creating map, 80x50, max 25 rooms with min room size 5 and max size 12 """
        room_min_size = 5
        room_max_size = 12

        self.console_map = libtcod.console_new(self.map_width, self.map_height)
         
        gen = gamemap.MapGenerator(self.map_width, self.map_height, self.max_amount_of_rooms_in_map, room_min_size, room_max_size)
        
        self.level_map = gen.create_map()
        self.player.position = gen.player_start_point
        px, py = self.player.position
        
        libtcod.console_clear(self.console_map)
        libtcod.console_set_foreground_color(self.console_map, libtcod.white)
        libtcod.console_set_foreground_color(self.console_map, libtcod.black)
        libtcod.console_put_char(self.console_map, px, py, '@', libtcod.BKGND_NONE)

        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.level_map[x][y] == '=':
                    libtcod.console_put_char(self.console_map, x, y, libtcod.CHAR_DHLINE, libtcod.BKGND_NONE)
        
    def init_fov(self):
        self.fov_map = libtcod.map_new(self.map_width, self.map_height)
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                libtcod.map_set_properties(self.fov_map, x, y, 
                                           not self.level_map[x][y].tile_property["blocks_walking"], 
                                           not self.level_map[x][y].tile_property["blocks_visibility"])
                    
    
    def get_key(self, key):
        if key.vk == libtcod.KEY_CHAR:
            return chr(key.c)
        else:
            return key.vk
    

    def update_movement(self, movement_direction):
        dx, dy = movement_direction
        px, py = self.player.position
        x, y = dx + px, dy + py
        
        if not self.level_map[x][y].tile_property["blocks_walking"]:
            libtcod.console_put_char(self.console_map, px, py, ' ', libtcod.BKGND_NONE)
            self.player.position = x, y
            self.message_panel.add_message("Current player position is (%d, %d)" % self.player.position)
        else:
            self.message_panel.add_message("Cannot go to %d %d" % (x, y))

    def update(self, key):
        key = self.get_key(key)
        if key in self.keys:
            do_type, params = self.keys[key]

            if do_type == "movement":
                self.update_movement(params)
                
            if do_type == "action":
                params()
                

    def draw_panel(self):
        # TODO: Change background color back to black after testing
        libtcod.console_set_background_color(self.console_panel, libtcod.dark_gray)
        libtcod.console_clear(self.console_panel)
        
        for index in range(len(self.message_panel.messages)):
            libtcod.console_print_left(self.console_panel, 0, index, libtcod.BKGND_NONE, self.message_panel.messages[index])
            
        libtcod.console_blit(self.console_panel, 0, 0, self.message_panel.width, self.message_panel.height, 0, self.message_panel.x, self.message_panel.y)


    def draw_unseen_tiles(self, y, x):
        if self.level_map[x][y].tile_property["is_explored"]:
            if self.level_map[x][y].tile_property["blocks_walking"]:
                libtcod.console_set_back(self.console_map, x, y, self.colors["dark wall"], libtcod.BKGND_SET)
            else:
                libtcod.console_set_back(self.console_map, x, y, self.colors["dark ground"], libtcod.BKGND_SET)


    def draw_seen_tiles(self, y, x):
        if self.level_map[x][y].tile_property["blocks_walking"]:
            libtcod.console_set_back(self.console_map, x, y, self.colors["light wall"], libtcod.BKGND_SET)
        else:
            libtcod.console_set_back(self.console_map, x, y, self.colors["light ground"], libtcod.BKGND_SET)
        self.level_map[x][y].tile_property["is_explored"] = True


    def draw_tiles(self, y, x):
        if libtcod.map_is_in_fov(self.fov_map, x, y):
            self.draw_seen_tiles(y, x)
        else:
            self.draw_unseen_tiles(y, x)


    def draw_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.draw_tiles(y, x)

        # TODO: draw_player is in wrong place. fix it
        self.draw_player()
        libtcod.console_blit(self.console_map, 0, 0, self.map_width, self.map_height, 0, 0, 0)


    def draw_player(self):
        px, py = self.player.position
        libtcod.console_set_foreground_color(self.console_map, libtcod.Color(200, 200, 200))
        libtcod.console_put_char(self.console_map, px, py, "@", libtcod.BKGND_NONE)

    def draw(self):
        # FIXME: recompute_fov is called always (even when it's not necessary.
        self.recompute_field_of_vision()
        
        self.draw_map()
        
        self.draw_panel()
        
        libtcod.console_flush()
        
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

