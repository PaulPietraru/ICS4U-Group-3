# -------------------------------------------------------------------------------
# Name:           game_collection.py
#
# Purpose:        A game collection
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

from gui import GuiVisualParams
from gui import Button
from gui import TextArea
from basic_game import BasicGame
from colors_game import ColorsGame
from tile_groups_game import TileGroupsGame

# A collection of games presented to the user
# A game must be picked to continue the program
class GameCollection():
    def __init__(self, canvas_size, title_font, text_font, bk_img):
        self.canvas_w = canvas_size[0]
        self.canvas_h = canvas_size[1]
        self.title_font = title_font
        self.bk_img = bk_img
        
        # create and adjust visual parameters
        self.buttons_gvp = GuiVisualParams()
        self.buttons_gvp.text_font = title_font
        
        self.text_areas_gvp = GuiVisualParams()
        self.text_areas_gvp.text_font = text_font
        self.text_areas_gvp.text_hight_percentage = 0.16
        self.text_areas_gvp.bk_color = (230, 230, 230)
        self.text_areas_gvp.text_color = (60, 6, 60)
        
        # create all the games
        self.games = [BasicGame("Tiles", 3, self.canvas_w, self.canvas_h, title_font, text_font, bk_img),
                      ColorsGame("Colors", 3, self.canvas_w, self.canvas_h, title_font, text_font, bk_img), 
                      TileGroupsGame("Groups", 3, self.canvas_w, self.canvas_h, title_font, text_font, bk_img)]

        # calcualte starting screen positions for buttons and descriptions
        self.title_line_h = 100
        self.title_line_gap = 50
        self.game_line_h = (self.canvas_h - 100) / len(self.games)
        self.game_line_gap = self.game_line_h / 3
        self.element_h = self.game_line_h - self.game_line_gap
        
        # create all buttons and text areas for descriptions
        self.buttons = self.create_selection_buttons(self.title_line_gap, self.title_line_h, (self.canvas_w - 3 * self.title_line_gap) / 3)
        self.text_areas = self.create_descr_text_areas(self.title_line_gap, self.title_line_h)
    
    # Create all the game selection buttons
    def create_selection_buttons(self, bx, by, bw):
        bh = self.element_h
        buttons = [None for i in range(len(self.games))]
        for i in range(0, len(self.games)):
            buttons[i] = Button(self.games[i].name, bx, by + self.game_line_h * i, bw, bh, self.buttons_gvp)
        return buttons

    # Create all the text areas with game descriptions
    def create_descr_text_areas(self, bx, by):
        bw = (self.canvas_w - 150) / 3
        tx = bx + bw + 50 
        ty = by
        tw = 2 * bw
        th = self.element_h
        text_areas = [None for i in range(len(self.games))]
        for i in range(0, len(self.games)):
            text_areas[i] = TextArea(self.games[i].description, tx, ty + self.game_line_h * i, tw, th, self.text_areas_gvp)
        return text_areas
        
    # Draw the game collection screen
    def draw(self):
        background(self.bk_img)
        textFont(self.title_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Game", self.canvas_w / 2, 50)
        for i in range(0, len(self.games)):
            self.buttons[i].draw()
            self.text_areas[i].draw()
            
    # Check if the mouse is moving above the buttons
    def mouse_moving(self, mx, my):
        for b in self.buttons:
            b.check_mouse_over(mx, my)
 
    # Check if a button was clicked
    def mouse_clicked(self, mx, my):
        for i in range(0, len(self.buttons)):
            if self.buttons[i].check_mouse_click(mx, my):
                # return the corresponding game
                return self.games[i]
        return None
