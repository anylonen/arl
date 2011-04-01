import libtcodpy as libtcod

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

class MapTile():
    """ MapTile class. Holds information about properties like visibility. """
    def __init__(self, blocks_walking = True, blocks_visibility = True):
        self.tile_property = {}
        self.tile_property["blocks_walking"] = blocks_walking
        self.tile_property["blocks_visibility"] = blocks_visibility

class MapGenerator():
    """ MapGenerator creates game map and sets the starting position. """
    
    def __init__(self, map_width, map_height, max_amount_of_rooms_in_map, room_min_size, room_max_size):
        self.map_width = map_width
        self.map_height = map_height
        self.max_amount_of_rooms_in_map = max_amount_of_rooms_in_map
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        
        self.rooms_in_map = []
        self.current_amount_of_rooms = 0
        
        self.player_start_point = (0, 0)

        self.gamemap = [[ MapTile()
                    for y in range(map_height) ]
                        for x in range(map_width) ]

    def create_map(self):
        """ Map generator. Size of map is MAP_WIDTH x MAP_HEIGHT. """
        for room in range(self.max_amount_of_rooms_in_map):
            room_candidate = self.create_room_candidate()
            
            room_can_be_created = True            
            
            for existing_room in self.rooms_in_map:
                if room_candidate.does_intersect(existing_room):
                    room_can_be_created = False
                    break
                
            if room_can_be_created:
                self.create_room(room_candidate)
                
                if self.current_amount_of_rooms == 0:
                    """ Center of the first room is the start point for the player. """
                    self.player_start_point = room_candidate.get_center()
                    
                else:
                    """ Connect two rooms together. """
                    previous_room = self.rooms_in_map[self.current_amount_of_rooms - 1]
                    self.create_horizontal_tunnel(previous_room, room_candidate)
                    self.create_vertical_tunnel(previous_room, room_candidate)

                self.add_room_to_map(room_candidate)

        # return MAP
        return self.gamemap

    def create_room_candidate(self):
        """ Create room candidate and return it's rectangle. """
        
        """ Dimensions for new room candidate. """
        room_width = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)
        room_height = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)

        """ Location for new room candidate. """
        x = libtcod.random_get_int(0, 0, self.map_width - room_width - 1)
        y = libtcod.random_get_int(0, 0, self.map_height - room_height - 1)

        return Rectangle(x, y, room_width, room_height)

    def create_room(self, room):
        """ "Carves" room into map. """
        
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.make_map_tile_passable(x, y)
    
    def add_room_to_map(self, room_rectangle):
        """ Adds room into list of rooms and increments total amount of rooms. """
        self.rooms_in_map.append(room_rectangle)
        self.current_amount_of_rooms += 1
    
    def create_horizontal_tunnel(self, previous_room, current_room):
        """ Creates horizontal tunnel between rooms. """
        
        prev_x, prev_y = previous_room.get_center()
        cur_x, cur_y = current_room.get_center()
        
        for x in range(min(prev_x, cur_x), max(prev_x, cur_x) + 1):
            self.make_map_tile_passable(x, prev_y)
    
    def create_vertical_tunnel(self, previous_room, current_room):
        """ Creates vertical tunnel between rooms. """
        prev_x, prev_y = previous_room.get_center()
        cur_x, cur_y = current_room.get_center()
        
        for y in range(min(prev_y, cur_y), max(prev_y, cur_y) + 1):
            self.make_map_tile_passable(cur_x, y)
            
    def make_map_tile_passable(self, x, y):
        self.gamemap[x][y].tile_property["blocks_walking"] = False
        self.gamemap[x][y].tile_property["blocks_visibility"] = False
    