# -------------------------------------------------------------------------------
# Name:           game.py
#
# Purpose:        Defines a game
#
# Author:         Pietraru.P
#
# Created:        29/05/2019
# ------------------------------------------------------------------------------
import random

class GameCollection():
    def __init__(self, canvas_w, canvas_h, title_font, text_font, bk_img):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.title_font = title_font
        self.text_font = text_font
        self.bk_img = bk_img
        
        self.button_vertical_space = (self.canvas_h - 100) / 3
        self.button_vertical_gap = self.button_vertical_space / 3
        self.button_height = self.button_vertical_space - self.button_vertical_gap
        
        bx = 50
        by = 100
        bw = (canvas_w - 150) / 3
        bh = self.button_height
        
        tx = bx + bw + 50 
        ty = by
        tw = 2 * bw
        th = bh
        
        self.games = [TilesGame("4 Tiles", 4, canvas_w, canvas_h), 
                      TilesGame("7 Tiles", 7, canvas_w, canvas_h),
                      TilesGame("9 Tiles", 9, canvas_w, canvas_h)]
        for i in range(0, len(self.games)):
            self.games[i].set_button(bx, by + self.button_vertical_space * i, bw, bh, tx, ty + self.button_vertical_space * i, tw, th, self.title_font, self.text_font)
            
    def draw(self):
        background(self.bk_img)
        textFont(self.title_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Game", self.canvas_w / 2, 50)
        for g in self.games:
            g.draw_button()
            
    def mouseMoving(self, mx, my):
        for g in self.games:
            g.check_mouse_over(mx, my)
 
    def mouseAction(self, mx, my):
        for g in self.games:
            if g.check_mouse(mx, my):
                return g
        return None
                
    
    
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
        self.level = Level(num_side_tiles, 5, canvas_w, canvas_h)
        
        self.description = """
        Check your short term memory by trying to 
        remember the position of colored tiles.
        """
        
    def draw(self):
        self.level.draw()
        
    def start(self):
        self.level.show()
        
    def mouseAction(self, mx, my):
        self.level.mouseAction(mx, my)
        
    def mouseMoving(self, mx, my):
        self.level.mouseMoving(mx, my)
        
    def show(self):
        print(self.name)
         
    def set_button(self, bx, by, bw, bh, tx, ty, tw, th, title_font, text_font):
        self.bx = bx
        self.by = by
        self.bw = bw
        self.bh = bh
        self.tx = tx
        self.ty = ty
        self.tw = tw
        self.th = th
        self.title_font = title_font
        self.text_font = text_font
        self.mouse_over = False
       
    def draw_button(self):    
        stroke(200, 200, 200)
        fill(127, 127, 127)
        rect(self.bx, self.by, self.bw, self.bh, 30)
        textFont(self.title_font, 30)
        textAlign(CENTER, CENTER);
        textSize(self.bh * 0.6)
        fill(255, 255, 255)
        text(self.name, self.bx + self.bw / 2, self.by + self.bh / 2)
        self.highlight()
        
        rect(self.tx, self.ty, self.tw, self.th, 30)
        textFont(self.text_font, 20)
        textAlign(LEFT, TOP);
        textSize(self.th * 0.2)
        fill(0, 0, 0)
        text(self.description, self.tx, self.ty)
        
    def highlight(self):
        if self.mouse_over:
            strokeWeight(3)
            fill(255, 0, 255, 30)
            rect(self.bx, self.by, self.bw, self.bh, 30)
            strokeWeight(1)
            fill(255, 255, 255)
 
    def check_mouse_over(self, mx, my):
        if self.bx < mx < self.bx + self.bw and self.by < my < self.by + self.bh:
            self.mouse_over = True
        else:
            self.mouse_over = False
            
    def check_mouse(self, mx, my):
        if self.bx < mx < self.bx + self.bw and self.by < my < self.by + self.bh:
            return True
        else:
            return False
class Level():
    """
    A level in a game
    """
    SHOW = 0
    PLAY = 1
    DONE = 2

    def __init__(self, num_side_tiles, num_tiles_set, canvas_w, canvas_h):
        """
        Initialize the game
        :param num_side_tiles: number of tiles on the side of the grid
        :param canvas_w: canvas width (for positioning)
        :param canvas_h: canvas height (for positioning)
        """
        self.num_side_tiles = num_side_tiles
        self.num_tiles_set = num_tiles_set
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.set_tiles = [[False for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        self.color_tiles = [[(127, 127, 127) for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        self.generate_level()
        self.grid = Grid(num_side_tiles, canvas_w, canvas_h, self.set_tiles, self.color_tiles)
        self.show_start_time = None
        self.play_start_time = None
        self.enable_mouse_action = False
        self.status = self.SHOW
        
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
        
    def draw(self):
        self.check_time()
        self.grid.draw()
    
    def check_time(self):
        current_time = millis()
        if self.status == self.SHOW and current_time - self.show_start_time > 3000:
            self.hide()
        elif self.status == self.PLAY and current_time - self.play_start_time > 5000:
            self.done()
    
    def show(self):
        self.status = self.SHOW
        self.show_start_time = millis()
        self.enable_mouse_action = False
        
    def hide(self):
        self.status = self.PLAY
        self.grid.hide_tiles()
        self.play_start_time = millis()
        self.enable_mouse_action = True
        
    def done(self):
        self.status = self.DONE
        self.grid.show_tiles()
        self.enable_mouse_action = False
        
    def mouseAction(self, mx, my):
        if self.enable_mouse_action:
            self.grid.mouseAction(mx, my)
        
    def mouseMoving(self, mx, my):
        self.grid.mouseMoving(mx, my)
        

class Grid():
    """
    A grid used in a game
    """
    
    def __init__(self, num_side_tiles, canvas_w, canvas_h, set_tiles, color_tiles):
        """
        Initialize the grid
        :param num_side_tiles: number of tiles on the side of the grid
        :param canvas_w: canvas width (for positioning)
        :param canvas_h: canvas height (for positioning)
        """
        self.num_side_tiles = num_side_tiles
        self.set_tiles = set_tiles
        self.color_tiles = color_tiles
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
        self.tiles = [[None for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        
        # create the tiles with computed coordinates relative to the grid coordinates
        for ln in range(0, num_side_tiles):
            for cl in range(0, num_side_tiles):
                tile_x = self.grid_x + self.tile_w * cl 
                tile_y = self.grid_y + self.tile_w * ln
                self.tiles[ln][cl] = Tile(tile_x, tile_y, self.tile_w, (0, 0, 0), color_tiles[ln][cl], set_tiles[ln][cl])
        
    def draw(self):
        """
        Draw the grid and all the tiles
        """
        rect(self.grid_x, self.grid_y, self.grid_w, self.grid_w)
        # draw each tile
        for line in self.tiles:
            for t in line:
                t.draw()

    def hide_tiles(self):
        for line in self.tiles:
            for t in line:
                t.hide()

    def show_tiles(self):
        for line in self.tiles:
            for t in line:
                t.show()

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
        self.edge_weight = 1
        self.bk_color = bk_color
        self.is_set = is_set
        self.status = self.EXPOSED
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
        strokeWeight(self.edge_weight)
        if self.status == self.EXPOSED:
            self.draw_exposed()
        elif self.status == self.HIDDEN:
            self.draw_hidden()
        elif self.status == self.CLICKED:
            self.draw_clicked()
        self.highlight()
    
    def hide(self):
        self.status = self.HIDDEN
    
    def show(self):
        if self.is_set and self.status == self.EXPOSED:
            self.edge_color = (0, 255, 0)
            self.edge_weight = 3
        
        if self.is_set and self.status == self.HIDDEN:
            self.edge_color = (255, 0, 0)
            self.edge_weight = 3
        
        if self.status == self.HIDDEN:
            self.status = self.EXPOSED
    
    def highlight(self):
        if self.mouse_over:
            strokeWeight(3)
            fill(255, 255, 255, 30)
            rect(self.x, self.y, self.w, self.w)
            strokeWeight(self.edge_weight)
    
    def check_mouse(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            if self.status == self.HIDDEN and self.is_set:
                self.status = self.EXPOSED
            elif self.status == self.HIDDEN and not self.is_set:
                self.status = self.CLICKED

    def check_mouse_over(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            self.mouse_over = True
        else:
            self.mouse_over = False
