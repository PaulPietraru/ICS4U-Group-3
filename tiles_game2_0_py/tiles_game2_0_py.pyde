

# grid instance to test the positioning and drwing of a grid in Processing
# -------------------------------------------------------------------------------
# Name:           game.py
#
# Purpose:        Defines a game
#
# Author:         Pietraru.P
#
# Created:        29/05/2019
# ------------------------------------------------------------------------------

class TileGame():
    """
    A tile game
    """
    
    def __init__(self, name):
        """
        Initialize the game
        :param name: name of the game
        """
        self.name = name
    

class Grid():
    """
    A grid used in a game
    """
    
    def __init__(self, num_side_tiles, canvas_w, canvas_h):
        """
        Initialize the grid
        :param num_side_tiles: number of tiles on the side of the grid
        :param canvas_w: canvas width (for positioning)
        :param canvas_h: canvas height (for positioning)
        """
        self.num_side_tiles = num_side_tiles
        # compute grid width and position on the canvas
        self.grid_w = min(canvas_w, canvas_h) * 0.9
        self.grid_x = (canvas_w / 2) - (self.grid_w / 2)
        self.grid_y = (canvas_h / 2) - (self.grid_w / 2)
        
        # compute tile size
        self.tile_w = self.grid_w / num_side_tiles
        
        # initialize a list of tiles organized as a list of lines with a tile per column
        # [[Tile(), Tile(), Tile()],
        #  [Tile(), Tile(), Tile()],
        #  [Tile(), Tile(), Tile()]]
        self.tiles = [[0 for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        
        # create the tiles with computed coordinates relative to the grid coordinates
        for ln in range(0, num_side_tiles):
            for cl in range(0, num_side_tiles):
                tile_x = self.grid_x + self.tile_w * cl 
                tile_y = self.grid_y + self.tile_w * ln
                self.tiles[ln][cl] = Tile(tile_x, tile_y, self.tile_w, (0, 0, 0), (tile_x % 255, tile_y % 255, tile_x * tile_y % 255))
        
    def draw(self):
        """
        Draw the grid and all the tiles
        """
        rect(self.grid_x, self.grid_y, self.grid_w, self.grid_w)
        # draw each tile
        for line in self.tiles:
            for t in line:
                t.draw()


class Tile():
    """
    A tile used in a grid
    """

    def __init__(self, x, y, w, edge_color, bk_color):
        """
        Initialize the tile
        :param x: the x coordinate
        :param x: the y coordinate
        :param x: the width
        :param edge_color: color of the edge as a tuple
        :param bk_color: color of the background as a tuple
        """
        self.x = x
        self.y = y
        self.w = w
        self.edge_color = edge_color
        self.bk_color = bk_color
    
    def draw(self):
        """
        Draw the tile
        """
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x, self.y, self.w, self.w)
        
grid_size = (1200, 800)
grid = Grid(11, grid_size[0], grid_size[1])
        
def setup():
            # set canvas size; use same size as the one given to the grid
    global grid_size
    size(grid_size[0], grid_size[1])
            # set initial stroke for line colors
    stroke(255)
    frameRate(30)
            
def draw():
    global grid
            # reset background to black
    background(0)
            # draw the grid
    grid.draw()
    stroke(255)
