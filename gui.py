# -------------------------------------------------------------------------------
# Name:           gui.py
#
# Purpose:        GUI elements
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

# Most used GUI parameters
# Used by all GUI to keep the look consistent
class GuiVisualParams():
    def __init__(self):
        # weight and color parameters
        self.stroke_weight = 1
        self.stroke_color = (200, 200, 200)
        self.bk_color = (127, 127, 127)
        self.bk_transparency = 100
        # highlight parameters
        self.hl_stroke_weight = 3
        self.hl_stroke_color = (200, 200, 200)
        self.hl_bk_color = (255, 0, 255)
        self.hl_transparency = 30
        # text parameters
        self.text_color = (255, 255, 255)
        self.text_hight_percentage = 0.5
        self.text_font = None
        # shape parameters
        self.corner_radius = 30

# A button able to react to clicks and mouse moving over it
class Button():
    def __init__(self, label, x, y, w, h, gvp):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.gvp = gvp
        self.mouse_over = False

    # Draw the button
    def draw(self):
        strokeWeight(self.gvp.stroke_weight)
        stroke(self.gvp.stroke_color[0], self.gvp.stroke_color[1], self.gvp.stroke_color[2])
        fill(self.gvp.bk_color[0], self.gvp.bk_color[1], self.gvp.bk_color[2])
        rect(self.x, self.y, self.w, self.h, self.gvp.corner_radius)
        textFont(self.gvp.text_font, 20)
        textAlign(CENTER, CENTER);
        textSize(self.h * self.gvp.text_hight_percentage)
        fill(self.gvp.text_color[0], self.gvp.text_color[1], self.gvp.text_color[2])
        text(self.label, self.x + self.w / 2, self.y + self.h / 2)
        self.highlight()
        
    # Highlight the button when the mouse is above it
    def highlight(self):
        if self.mouse_over:
            strokeWeight(self.gvp.hl_stroke_weight)
            fill(self.gvp.hl_bk_color[0], self.gvp.hl_bk_color[1], self.gvp.hl_bk_color[2], self.gvp.hl_transparency)
            rect(self.x, self.y, self.w, self.h, self.gvp.corner_radius)
            strokeWeight(self.gvp.stroke_weight)

    # Check if the mouse is over the button
    def check_mouse_over(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.h:
            self.mouse_over = True
        else:
            self.mouse_over = False
    
    # Check if the button was clicked
    def check_mouse_click(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.h:
            return True
        else:
            return False  

# A text area used to display a text in a rectangle
class TextArea():
    def __init__(self, text, x, y, w, h, gvp):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.gvp = gvp

    # Draw the text area
    def draw(self):
        strokeWeight(self.gvp.stroke_weight)
        stroke(self.gvp.stroke_color[0], self.gvp.stroke_color[1], self.gvp.stroke_color[2])
        fill(self.gvp.bk_color[0], self.gvp.bk_color[1], self.gvp.bk_color[2])
        rect(self.x, self.y, self.w, self.h, self.gvp.corner_radius)
        textFont(self.gvp.text_font, 20)
        textAlign(LEFT, TOP);
        textSize(self.h * self.gvp.text_hight_percentage)
        fill(self.gvp.text_color[0], self.gvp.text_color[1], self.gvp.text_color[2])
        text(self.text, self.x, self.y)

# A screen area marked with a rectabgle and used to keep lines of texts and buttons
class ScreenArea():
    def __init__(self, num_lines, x, y, w, h, gvp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.gvp = gvp
        self.num_lines = num_lines
        self.elements = [None for i in range(self.num_lines)]
        self.crt_element_idx = 0

    # Draw the text area and its elements
    def draw(self):
        strokeWeight(self.gvp.stroke_weight)
        stroke(self.gvp.stroke_color[0], self.gvp.stroke_color[1], self.gvp.stroke_color[2])
        fill(self.gvp.bk_color[0], self.gvp.bk_color[1], self.gvp.bk_color[2], self.gvp.bk_transparency)
        rect(self.x, self.y, self.w, self.h, self.gvp.corner_radius)
        
        for e in self.elements:
            if e is not None:
                e.draw()

    # Add a text element to this screen area
    def add_text_element(self, text):
        if self.crt_element_idx == self.num_lines:
            return None
        
        x = self.x + self.w / 2
        lh = self.h / self.num_lines
        y = self.y + lh * self.crt_element_idx + lh / 2
        element = TextElement(text, x, y, lh * self.gvp.text_hight_percentage, self.gvp)
        self.elements[self.crt_element_idx] = element
        self.crt_element_idx = self.crt_element_idx + 1
        return element
        
    # Add a button to this screen area
    def add_button_element(self, label, buttons_gvp):
        if self.crt_element_idx == self.num_lines:
            return None
        cx = 20
        cy = 10
        lh = self.h / self.num_lines
        x = self.x + cx
        y = self.y + lh * self.crt_element_idx + cy
        w = self.w - 2 * cx
        h = lh - 2 * cy
        element = Button(label, x, y, w, h, buttons_gvp)
        self.elements[self.crt_element_idx] = element
        self.crt_element_idx = self.crt_element_idx + 1
        return element
        
# A text element at a specified position on the screen
class TextElement():
    def __init__(self, text, x, y, text_height, gvp):
        self.text = text
        self.x = x
        self.y = y
        self.text_height = text_height
        self.gvp = gvp
    
    # Change the text
    def update(self, text):
        self.text = text
    
    # Draw the text
    def draw(self):
        textFont(self.gvp.text_font, 30)
        textAlign(CENTER, CENTER);
        textSize(self.text_height)
        fill(self.gvp.text_color[0], self.gvp.text_color[1], self.gvp.text_color[2])
        text(self.text, self.x, self.y)


# A grid of tiles used in a tiles game
class Grid():
    def __init__(self, num_side_tiles, grid_x, grid_y, grid_w, set_tiles, color_tiles):
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
    
    # Draw the grid
    def draw(self):
        """
        Draw the grid and all the tiles
        """
        rect(self.grid_x, self.grid_y, self.grid_w, self.grid_w)
        # draw each tile
        for line in self.tiles:
            for t in line:
                t.draw()

    # Hide all tiles
    def hide_tiles(self):
        for line in self.tiles:
            for t in line:
                t.hide()

    # Show all tiles
    def show_tiles(self):
        for line in self.tiles:
            for t in line:
                t.show()

    # React to a mouse click
    def mouseAction(self, mx, my):
        if self.grid_x < mx < self.grid_x + self.grid_w and self.grid_y < my < self.grid_y + self.grid_w:
            for line in self.tiles:
                for t in line:
                    t.check_mouse(mx, my)
        return self.compute_current_grid_state()

    # Compute the current state of the grid.
    def compute_current_grid_state(self):
        current_grid_state = [[False for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.tiles[ln][cl].status == Tile.EXPOSED or self.tiles[ln][cl].status == Tile.CLICKED:
                    current_grid_state[ln][cl] = True
        return current_grid_state

    # React to mouse moving over the grid
    def mouse_moving(self, mx, my):
        for line in self.tiles:
            for t in line:
                t.check_mouse_over(mx, my)


# A tile in a grid
# It hase 3 states: EXPOSED, HIDDEN, CLICKED
class Tile():
    """
    A tile used in a grid
    """
    hidden_color = (127, 127, 127)
    EXPOSED = 0
    HIDDEN = 1
    CLICKED = 2

    def __init__(self, x, y, w, edge_color, bk_color, is_set):
        self.x = x
        self.y = y
        self.w = w
        self.edge_color = edge_color
        self.edge_weight = 1
        self.bk_color = bk_color
        self.is_set = is_set
        self.status = self.EXPOSED
        self.mouse_over = False
    
    # Draw the tile exposed (color visible)
    def draw_exposed(self):
        c = self.edge_weight - 1
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x + c, self.y + c, self.w - 2 * c, self.w - 2 * c)
        
    # Draw the tile hidden (color hidden)
    def draw_hidden(self):
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.hidden_color[0], self.hidden_color[1], self.hidden_color[2])
        rect(self.x, self.y, self.w, self.w)
        
    # Draw the tile clicked (with an X)
    def draw_clicked(self):
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
    
    # Draw the tile based on its status
    def draw(self):
        strokeWeight(self.edge_weight)
        if self.status == self.EXPOSED:
            self.draw_exposed()
        elif self.status == self.HIDDEN:
            self.draw_hidden()
        elif self.status == self.CLICKED:
            self.draw_clicked()
        self.highlight()
    
    # Mark a tile as hidden
    def hide(self):
        self.status = self.HIDDEN
    
    # Mark a tile as shown
    def show(self):
        if self.is_set and self.status == self.EXPOSED:
            self.edge_color = (0, 255, 0)
            self.edge_weight = 3
        
        if self.is_set and self.status == self.HIDDEN:
            self.edge_color = (255, 0, 0)
            self.edge_weight = 3
        
        if self.status == self.HIDDEN:
            self.status = self.EXPOSED
    
    # Highlight a tile when the mouse is above it
    def highlight(self):
        if self.mouse_over:
            strokeWeight(3)
            fill(255, 255, 255, 30)
            rect(self.x + 2, self.y + 2, self.w - 4, self.w - 4)
            strokeWeight(self.edge_weight)
    
    # Check if the tile was clciked
    def check_mouse(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            if self.status == self.HIDDEN and self.is_set:
                self.status = self.EXPOSED
            elif self.status == self.HIDDEN and not self.is_set:
                self.status = self.CLICKED

    # Check if the mouse is above the tile
    def check_mouse_over(self, mx, my):
        if self.x < mx < self.x + self.w and self.y < my < self.y + self.w:
            self.mouse_over = True
        else:
            self.mouse_over = False
