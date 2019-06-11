class Button():
    def __init__(self, label, x, y, w, h, r, thp, sw, edge_color, bk_color, text_color, text_font, hl_color, hl_transparency, hl_sw):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.thp = thp
        self.sw = sw
        self.hl_sw = hl_sw
        self.edge_color = edge_color
        self.bk_color = bk_color
        self.text_color = text_color
        self.text_font = text_font
        self.hl_color = hl_color
        self.hl_transparency = hl_transparency
        self.mouse_over = False

    def draw(self):
        strokeWeight(self.sw)
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x, self.y, self.w, self.h, self.r)
        textFont(self.text_font, 20)
        textAlign(CENTER, CENTER);
        textSize(self.h * self.thp)
        fill(self.text_color[0], self.text_color[1], self.text_color[2])
        text(self.label, self.x + self.w / 2, self.y + self.h / 2)
        self.highlight()
        
    def highlight(self):
        if self.mouse_over:
            strokeWeight(self.hl_sw)
            fill(self.hl_color[0], self.hl_color[1], self.hl_color[2], self.hl_transparency)
            rect(self.x, self.y, self.w, self.h, self.r)
            strokeWeight(self.sw)
 
    def check_mouse_over(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.h:
            self.mouse_over = True
        else:
            self.mouse_over = False
            
    def check_mouse_click(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.h:
            return True
        else:
            return False  
        
class TextArea():
    def __init__(self, text, x, y, w, h, r, thp, sw, text_font, edge_color, bk_color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.thp = thp
        self.sw = sw
        self.text_font = text_font
        self.edge_color = edge_color
        self.bk_color = bk_color
        self.text_color = text_color

    def draw(self):
        strokeWeight(self.sw)
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x, self.y, self.w, self.h, self.r)
        textFont(self.text_font, 20)
        textAlign(LEFT, TOP);
        textSize(self.h * self.thp)
        fill(self.text_color[0], self.text_color[1], self.text_color[2])
        text(self.text, self.x, self.y)

class ScreenArea():
    def __init__(self, num_lines, x, y, w, h, r, bk_color, bk_transparency, sw, edge_color, text_color, text_font):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.num_lines = num_lines
        self.bk_color = bk_color
        self.bk_transparency = bk_transparency
        self.sw = sw
        self.edge_color = edge_color
        self.text_font = text_font
        self.text_color = text_color
        self.elements = [None for i in range(self.num_lines)]
        self.crt_element = 0

    def draw(self):
        strokeWeight(self.sw)
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2], self.bk_transparency)
        rect(self.x, self.y, self.w, self.h, self.r)
        
        for e in self.elements:
            if e is not None:
                e.draw()

    def add_text_element(self, text):
        if self.crt_element == self.num_lines:
            return None
        
        x = self.x + self.w / 2
        lh = self.h / self.num_lines
        y = self.y + lh * self.crt_element + lh / 2
        element = TextElement(text, x, y, self.text_color, self.text_font)
        self.elements[self.crt_element] = element
        self.crt_element = self.crt_element + 1
        return element
        
    def add_button_element(self, label, r, thp, sw, edge_color, bk_color, text_color, hl_color, hl_transparency, hl_sw):
        if self.crt_element == self.num_lines:
            return None
        cx = 20
        cy = 10
        lh = self.h / self.num_lines
        x = self.x + cx
        y = self.y + lh * self.crt_element + cy
        w = self.w - 2 * cx
        h = lh - 2 * cy
        element = Button(label, x, y, w, h, r, thp, sw, edge_color, bk_color, text_color, self.text_font, hl_color, hl_transparency, hl_sw)
        self.elements[self.crt_element] = element
        self.crt_element = self.crt_element + 1
        return element
        
class TextElement():
    def __init__(self, text, x, y, text_color, text_font):
        self.text = text
        self.x = x
        self.y = y
        self.text_color = text_color
        self.text_font = text_font
    
    def update(self, text):
        self.text = text
    
    def draw(self):
        textFont(self.text_font, 30)
        textAlign(CENTER, CENTER);
        textSize(30)
        fill(self.text_color[0], self.text_color[1], self.text_color[2])
        text(self.text, self.x, self.y)

        
class Grid():
    """
    A grid used in a game
    """
    
    def __init__(self, num_side_tiles, grid_x, grid_y, grid_w, set_tiles, color_tiles):
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
        self.grid_w = grid_w
        self.grid_x = grid_x
        self.grid_y = grid_y
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
        fill(0, 0, 0)
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
        return self.compute_current_grid_state()

    def compute_current_grid_state(self):
        current_grid_state = [[False for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.tiles[ln][cl].status == Tile.EXPOSED or self.tiles[ln][cl].status == Tile.CLICKED:
                    current_grid_state[ln][cl] = True
        return current_grid_state

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
        c = self.edge_weight - 1
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x + c, self.y + c, self.w - 2 * c, self.w - 2 * c)
        
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
            rect(self.x + 2, self.y + 2, self.w - 4, self.w - 4)
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
