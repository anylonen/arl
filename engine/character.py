
import libtcodpy as libtcod
from utils import GameObject


class Player(GameObject):
    """Player class. At this point only moving around is supported. """
    
    def __init__(self, position, character, color):
        GameObject.__init__(self, position, character, color, True)

class Monster(GameObject):
    """Monster class. """
    
    def __init__(self, position, character, color):
        GameObject.__init__(self, position, character, color, True)

        self.movement_direction = []

        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                self.movement_direction.append((x, y))

    def get_new_position(self, direction):
        current_x, current_y = self.position
        dx, dy = direction
        return (current_x + dx, current_y + dy)
    
    def update(self, the_game):
        free_space_available = False
        
        while not free_space_available:
            index = libtcod.random_get_int(0, 0, len(self.movement_direction) - 1)
            x, y = self.get_new_position(self.movement_direction[index])
            if not the_game.is_wall_in_way(x, y) and not the_game.is_player_in_way(x, y):
                old_x, old_y = self.position
                libtcod.console_put_char(the_game.console_map, old_x, old_y, ' ', libtcod.BKGND_NONE)
                self.position = (x, y)
                free_space_available = True
                
             
            
