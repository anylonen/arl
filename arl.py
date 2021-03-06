#!/usr/bin/env python

import os

import tcod
import tcod.console
import tcod.event

from engine import UI, character, gamemap, utils


class ARL(object):
    """The main class to handle stuff."""
    def __init__(self):
        """ Constants """
        resource_loader = utils.ResourceLoader("arl.cfg")

        self.window_width = resource_loader.settings["window_width"]
        self.window_height = resource_loader.settings["window_height"]

        self.map_width = resource_loader.settings["map_width"]
        self.map_height = resource_loader.settings["map_height"]
        self.max_amount_of_rooms_in_map = resource_loader.settings[
            "max_amount_of_rooms_in_map"]

        self.message_panel = UI.Panel()

        self.do_movement = {}
        self.do_action = {}

        self.key_bindings = {}
        self.keys = {}

        self.player = None
        self.monsters = []

        self.level_map = None
        self.level_map_spawn_points = []
        self.fov_map = None
        self.fov_radius = 0
        self.fov_colors = {}

        self.colors = {
            "dark wall": tcod.Color(10, 10, 10),
            "light wall": tcod.Color(60, 35, 0),
            "dark ground": tcod.Color(100, 100, 100),
            "light ground": tcod.Color(145, 120, 90)
        }

        self.fov_algorithm = 0  # default FOV algorithm
        self.fov_radius = 10
        self.fov_light_walls = True  # light walls or not

        self.font = None
        self.console_map = None
        self.console_panel = None

    def init_player(self):
        self.player = character.Player(self.level_map_spawn_points[0], "@",
                                       tcod.Color(200, 200, 200))

    def init_monsters(self):
        # TODO: Change spawn point to random, now it's the second room
        self.monsters.append(
            character.Monster(self.level_map_spawn_points[1], "m",
                              tcod.Color(0, 0, 255)))

    def initialize(self):
        """ General initialization. """
        self.font = os.path.join("data/fonts", "arial12x12.png")
        tcod.console_set_custom_font(
            self.font, tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE)
        tcod.console_init_root(self.window_width,
                               self.window_height,
                               "Anylo's RogueLike",
                               renderer=tcod.RENDERER_SDL2)

        self.init_movement()
        self.init_action()
        self.init_bindings()
        self.init_map()
        self.init_panel()
        self.init_fov()

        self.init_player()
        self.init_monsters()

    def do_nothing(self):
        print("Doing nothing")

    def do_fullscreen(self):
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    def init_movement(self):
        self.do_movement = {
            "north": (0, -1),
            "northeast": (1, -1),
            "east": (1, 0),
            "southeast": (1, 1),
            "south": (0, 1),
            "southwest": (-1, 1),
            "west": (-1, 0),
            "northwest": (-1, -1)
        }

    def init_action(self):
        self.do_action = {
            "nothing": self.do_nothing,
            "fullscreen": self.do_fullscreen
        }

    def init_bindings(self):
        self.keys = {
            tcod.KEY_KP8: ("movement", self.do_movement["north"]),
            tcod.KEY_KP9: ("movement", self.do_movement["northeast"]),
            tcod.KEY_KP6: ("movement", self.do_movement["east"]),
            tcod.KEY_KP3: ("movement", self.do_movement["southeast"]),
            tcod.KEY_KP2: ("movement", self.do_movement["south"]),
            tcod.KEY_KP1: ("movement", self.do_movement["southwest"]),
            tcod.KEY_KP4: ("movement", self.do_movement["west"]),
            tcod.KEY_KP7: ("movement", self.do_movement["northwest"]),
            tcod.KEY_KP5: ("action", self.do_action["nothing"]),
            tcod.KEY_F11: ("action", self.do_action["fullscreen"])
        }

    def init_panel(self):
        panel_height = 5

        self.message_panel.x = 0
        self.message_panel.y = self.window_height - (self.window_height -
                                                     self.map_height)
        self.message_panel.width = self.window_width
        self.message_panel.height = panel_height

        self.console_panel = tcod.console.Console(self.message_panel.width,
                                                  self.message_panel.height)

    def init_map(self):

        room_min_size = 5
        room_max_size = 12

        self.console_map = tcod.console.Console(self.map_width,
                                                self.map_height)

        level_map = gamemap.MapGenerator(self.map_width, self.map_height,
                                         self.max_amount_of_rooms_in_map,
                                         room_min_size, room_max_size)

        self.level_map = level_map.create_map()
        self.level_map_spawn_points = level_map.spawn_points

    def init_fov(self):
        self.fov_map = tcod.map.Map(self.map_width, self.map_height)

        for y in range(self.map_height):
            for x in range(self.map_width):
                tcod.map_set_properties(
                    self.fov_map, x, y,
                    not self.level_map[x][y].tile_property["blocks_walking"],
                    not self.level_map[x][y].tile_property["blocks_visibility"]
                )

    def get_key(self, key):
        if key.vk == tcod.KEY_CHAR:
            return chr(key.c)
        else:
            return key.vk

    def is_wall_in_way(self, x, y):
        return self.level_map[x][y].tile_property["blocks_walking"]

    def is_object_in_way(self, x, y):
        for monster in self.monsters:
            if monster.position == (x, y):
                return True
        return False

    def is_player_in_way(self, x, y):
        return self.player.position == (x, y)

    def update_player_movement(
        self,
        movement_direction,
    ):
        dx, dy = movement_direction
        px, py = self.player.position
        x, y = dx + px, dy + py

        if self.is_wall_in_way(x, y) or self.is_object_in_way(x, y):
            self.message_panel.add_message("Cannot go to %d %d" % (x, y))
        else:
            tcod.console_put_char(self.console_map, px, py, ' ',
                                  tcod.BKGND_NONE)
            self.player.position = (x, y)
            self.message_panel.add_message(
                "Current player position is (%d, %d)" % self.player.position)

    def update(self, key):
        key = self.get_key(key)
        if key in self.keys:
            do_type, params = self.keys[key]

            if do_type == "movement":
                self.update_player_movement(params)

            if do_type == "action":
                params()

    def update_monsters(self):
        for monster in self.monsters:
            monster.update(self)

    def draw_panel(self):
        # TODO: Change background color back to black after testing
        tcod.console_set_default_background(self.console_panel, tcod.dark_gray)
        tcod.console_clear(self.console_panel)

        for index in range(len(self.message_panel.messages)):
            tcod.console_print(self.console_panel, 0, index,
                               self.message_panel.messages[index])

        tcod.console_blit(self.console_panel, 0, 0, self.message_panel.width,
                          self.message_panel.height, 0, self.message_panel.x,
                          self.message_panel.y)

    def draw_unseen_tiles(self, y, x):
        if self.level_map[x][y].tile_property["is_explored"]:
            if self.level_map[x][y].tile_property["blocks_walking"]:
                tcod.console_set_char_background(self.console_map, x, y,
                                                 self.colors["dark wall"],
                                                 tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(self.console_map, x, y,
                                                 self.colors["dark ground"],
                                                 tcod.BKGND_SET)

    def draw_seen_tiles(self, y, x):
        if self.level_map[x][y].tile_property["blocks_walking"]:
            tcod.console_set_char_background(self.console_map, x, y,
                                             self.colors["light wall"],
                                             tcod.BKGND_SET)
        else:
            tcod.console_set_char_background(self.console_map, x, y,
                                             self.colors["light ground"],
                                             tcod.BKGND_SET)
        self.level_map[x][y].tile_property["is_explored"] = True

    def draw_tiles(self, y, x):
        if tcod.map_is_in_fov(self.fov_map, x, y):
            self.draw_seen_tiles(y, x)
        else:
            self.draw_unseen_tiles(y, x)

    def draw_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.draw_tiles(y, x)

        # TODO: draw_player is in wrong place. fix it
        self.draw_player()
        self.draw_monsters()

        tcod.console_blit(self.console_map, 0, 0, self.map_width,
                          self.map_height, 0, 0, 0)

    def draw_player(self):
        self.player.draw(self.console_map)

    def draw_monsters(self):
        for monster in self.monsters:
            x, y = monster.position
            if tcod.map_is_in_fov(self.fov_map, x, y):
                monster.draw(self.console_map)
            else:
                tcod.console_put_char(self.console_map, x, y, ' ',
                                      tcod.BKGND_NONE)

    def draw(self):
        # FIXME: recompute_fov is called always (even when it's not necessary.
        self.recompute_field_of_vision()

        self.draw_map()

        self.draw_panel()

        tcod.console_flush()

    def recompute_field_of_vision(self):
        px, py = self.player.position
        tcod.map_compute_fov(self.fov_map, px, py, self.fov_radius,
                             self.fov_light_walls, self.fov_algorithm)


def main():
    the_game = ARL()
    the_game.initialize()

    key = tcod.Key()
    mouse = tcod.Mouse()

    running = True

    while not tcod.console_is_window_closed() and running:
        the_game.draw()

        while tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True):
            if key.vk == tcod.KEY_ESCAPE:
                running = False
                break
            else:
                the_game.update(key)
                the_game.update_monsters()
                the_game.draw()


if __name__ == "__main__":
    main()
