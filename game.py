# -------------------------------------------------------------------------------
# Name:           game.py
#
# Purpose:        Defines a game
#
# Author:         Pietraru.P
#
# Created:        29/05/2019
# ------------------------------------------------------------------------------

class TilesGame():
    """
    A tile game
    """
    
    def __init__(self, name, num_side_tiles, canvas_w, canvas_h):
        """
        Initialize the game
        :param name: name of the game
        :param num_side_tiles: number of tiles on the side of the grid
        :param canvas_w: canvas width (for positioning)
        :param canvas_h: canvas height (for positioning)
        """
        self.name = name
        self.num_side_tiles = num_side_tiles
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.grid = Grid(num_side_tiles, canvas_w, canvas_h)
        
    def draw(self):
        self.grid.draw()
        
    def mouseAction(self, mx, my):
        self.grid.mouseAction(mx, my)
        
    def mouseMoving(self, mx, my):
        self.grid.mouseMoving(mx, my)


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
                self.tiles[ln][cl] = Tile(tile_x, tile_y, self.tile_w, (0, 0, 0), (tile_x % 255, tile_y % 255, tile_x * tile_y % 255), True)
        
    def draw(self):
        """
        Draw the grid and all the tiles
        """
        rect(self.grid_x, self.grid_y, self.grid_w, self.grid_w)
        # draw each tile
        for line in self.tiles:
            for t in line:
                t.draw()

    def mouseAction(self, mx, my):
        if self.grid_x < mx < self.grid_x + self.grid_w and self.grid_y < my < self.grid_y + self.grid_w:
            for line in self.tiles:
                for t in line:
                    t.check_mouse(mx, my)
    def mouseMoving(self, mx, my):
        for line in self.tiles:
            for t in line:
                t.check_mouse_over(mx, my)


class Tile():
    """
    A tile used in a grid
    """
    hidden_color = (127, 127, 127)
    EXPOSED = 0
    HIDDEN = 1
    CLICKED = 2

    def __init__(self, x, y, w, edge_color, bk_color, is_set):
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
        self.is_set = is_set
        self.status = self.HIDDEN
        self.mouse_over = False
    
    def draw_exposed(self):
        """
        Draw the tile exposed
        """
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x, self.y, self.w, self.w)
        
    def draw_hidden(self):
        """
        Draw the tile hidden
        """
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.hidden_color[0], self.hidden_color[1], self.hidden_color[2])
        rect(self.x, self.y, self.w, self.w)
        
    def draw_clicked(self):
        """
        Draw the tile clicked
        """
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.hidden_color[0], self.hidden_color[1], self.hidden_color[2])
        rect(self.x, self.y, self.w, self.w)
        adjust = 0.3
        x1 = self.x + self.w * adjust
        y1 = self.y + self.w * adjust
        x2 = self.x + self.w - self.w * adjust
        y2 = self.y + self.w - self.w * adjust
        line(x1, y1, x2, y2)
        line(x2, y1, x1, y2)
    
    def draw(self):
        if self.status == self.EXPOSED:
            self.draw_exposed()
        elif self.status == self.HIDDEN:
            self.draw_hidden()
        elif self.status == self.CLICKED:
            self.draw_clicked()
        self.highlight()
    
    def highlight(self):
        if self.mouse_over:
            strokeWeight(3)
            fill(255, 255, 255, 30)
            rect(self.x, self.y, self.w, self.w)
            strokeWeight(1)
    
    def check_mouse(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            if self.status == self.EXPOSED:
                self.status = self.HIDDEN
            elif self.status == self.HIDDEN:
                self.status = self.CLICKED
            elif self.status == self.CLICKED:
                self.status = self.EXPOSED

    def check_mouse_over(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            self.mouse_over = True
        else:
            self.mouse_over = False
