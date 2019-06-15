# -------------------------------------------------------------------------------
# Name:           basic_game.py
#
# Purpose:        Defines the basic game
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

import random
from game import TilesGame
from game import Level

# A basic tiles game where each tile has the same color
class BasicGame(TilesGame):
    def __init__(self, name, num_side_tiles, canvas_w, canvas_h, title_font, text_font, bk_img):
        super(BasicGame, self).__init__(name, num_side_tiles, canvas_w, canvas_h, title_font, text_font, bk_img)
        self.description = """
        Check your short term memory by trying to remember the position of a
        number of presented tiles while difficulty gradually increases each level.
        """
    
    # Create the level instance
    def generate_level(self):
        return BasicLevel(self, self.crt_level_num, self.num_side_tiles, self.num_tiles_set, self.show_time, self.extra_clicks, self.level_x, self.level_y, self.level_w)

    # Update the level parameters
    def update_level_parameters(self):
        self.num_tiles_set = self.num_tiles_set + 1
        self.num_side_tiles = self.num_side_tiles + 1
        self.crt_level_num = self.crt_level_num + 1


# A level where the number of still hidden tiles and the number of available clicks is checked
class BasicLevel(Level):
    def __init__(self, parent_game, level_number, num_side_tiles, num_tiles_set, show_time, extra_clicks, level_x, level_y, level_w):
        super(BasicLevel, self).__init__(parent_game, level_number, num_side_tiles, num_tiles_set, show_time, extra_clicks, level_x, level_y, level_w)
    
    # Evaluate the level status after each click    
    def generate_level(self):
        tile_color = (random.randrange(256), random.randrange(256), random.randrange(256))
        count = self.num_tiles_set
        while count != 0:
            l = random.randrange(self.num_side_tiles)
            c = random.randrange(self.num_side_tiles)
            if not self.set_tiles[l][c]:
                self.set_tiles[l][c] = True
                self.color_tiles[l][c] = tile_color
                count = count - 1

    # Check if the level is done
    def evaluate_level(self, latest_tile_status):
        if self.grid_status_changed(latest_tile_status):
            self.clicks_left = self.clicks_left - 1
            if self.all_tiles_exposed():
                self.done(self.SUCCESS) # win level
            elif self.clicks_left < self.count_hidden_tiles():
                self.done(self.FAILED) # lose level
            elif self.clicks_left == 0:
                self.done(self.FAILED) # lose level
        self.parent_game.set_level_clicks_left(self.clicks_left)
