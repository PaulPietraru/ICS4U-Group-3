# -------------------------------------------------------------------------------
# Name:           tile_groups_game.py
#
# Purpose:        A game with groups of tiles
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

import random
from game import TilesGame
from game import Level

# A tiles game where pairs of tiles with the same color are generated and each 
# group have to be discovered completely before another group is startred
class TileGroupsGame(TilesGame):
    def __init__(self, name, num_side_tiles, canvas_w, canvas_h, title_font, text_font, bk_img):
        self.tiles_in_group = 2
        self.num_groups = 2
        super(TileGroupsGame, self).__init__(name, num_side_tiles, canvas_w, canvas_h, title_font, text_font, bk_img)
        self.num_tiles_set = self.num_groups * self.tiles_in_group
        self.description = """
        A tiles game where pairs of tiles have the same color. 
        Each group have to be discovered before next group
        """
    
    # Create the level instance
    def generate_level(self):
        return TileGroupsLevel(self, self.crt_level_num, 
                           self.num_side_tiles, self.num_groups, self.tiles_in_group, self.show_time, self.extra_clicks, 
                           self.level_x, self.level_y, self.level_w)

    # Update the level parameters
    def update_level_parameters(self):
        self.num_groups = self.num_groups + 1
        self.num_side_tiles = self.num_side_tiles + 1
        self.crt_level_num = self.crt_level_num + 1
        self.extra_clicks = self.extra_clicks + 1


# A level where pairs of tiles with the same color are generated and each 
# group have to be discovered completely before another group is startred
class TileGroupsLevel(Level):
    def __init__(self, parent_game, level_number, num_side_tiles, num_groups, tiles_in_group, show_time, extra_clicks, level_x, level_y, level_w):
        self.num_groups = num_groups
        self.tiles_in_group = tiles_in_group
        super(TileGroupsLevel, self).__init__(parent_game, level_number, num_side_tiles, num_groups * tiles_in_group, show_time, extra_clicks, level_x, level_y, level_w)
       
   # Generate a level layout
    def generate_level(self):
        count_g = self.num_groups
        while count_g != 0:
            color_g = (random.randrange(140, 256), random.randrange(140, 256), random.randrange(140, 256))
            count_t = self.tiles_in_group
            while count_t != 0:
                l = random.randrange(self.num_side_tiles)
                c = random.randrange(self.num_side_tiles)
                if not self.set_tiles[l][c]:
                    self.set_tiles[l][c] = True
                    self.color_tiles[l][c] = color_g
                    count_t = count_t - 1
            count_g = count_g - 1
    
    # Evaluate the level status after each click
    def evaluate_level(self, latest_tile_status):
        if self.grid_status_changed(latest_tile_status):
            self.clicks_left = self.clicks_left - 1
            if self.all_tiles_exposed():
                self.done(self.SUCCESS) # win level
            elif self.check_incomplete_groups(latest_tile_status):
                self.done(self.FAILED) # lose level
            elif self.clicks_left < self.count_hidden_tiles():
                self.done(self.FAILED) # lose level
            elif self.clicks_left == 0:
                self.done(self.FAILED) # lose level
        self.parent_game.set_level_clicks_left(self.clicks_left)
    
    # Check if there are 2 incomplete goups of tiles exposed after
    def check_incomplete_groups(self, latest_tile_status):
        # TO BE DONE !!!
        return False
