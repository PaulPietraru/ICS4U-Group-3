# -------------------------------------------------------------------------------
# Name:           player_collection.py
#
# Purpose:        A collection of players
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

from gui import GuiVisualParams
from gui import Button
from player import Player

# A collection of players loaded a file
# A player must be selected to continue the program
class PlayerCollection():
    def __init__(self, file_name, canvas_size, text_font, bk_img):
        self.canvas_w = canvas_size[0]
        self.canvas_h = canvas_size[1]
        self.bk_img = bk_img
        
        self.gvp = GuiVisualParams()
        self.gvp.text_font = text_font
        
        self.button_vertical_space = (self.canvas_h - 100) / 10
        self.button_vertical_gap = self.button_vertical_space / 3
        self.button_height = self.button_vertical_space - self.button_vertical_gap
        
        bx = self.canvas_w / 2 - 250
        by = 100
        tx = self.canvas_w / 2 
        ty = by + self.button_height / 2
        
        self.player_names = loadStrings(file_name).tolist()
        self.players = [None for i in range(len(self.player_names))]
        self.buttons = [None for i in range(len(self.player_names))]
        for i in range(0, len(self.player_names)):
            self.players[i] = Player(self.player_names[i], 2)
            self.buttons[i] = Button(self.player_names[i], bx, by + self.button_vertical_space * i, 500, self.button_height, self.gvp)

    # Draw the screen for player selection
    def draw(self):
        background(self.bk_img)
        textFont(self.gvp.text_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Name", self.canvas_w / 2, 50)
        for b in self.buttons:
            b.draw()
        
    # React to mouse movement above the buttons
    def mouse_moving(self, mx, my):
        for b in self.buttons:
            b.check_mouse_over(mx, my)

    # Check if a button was clicked
    def mouse_clicked(self, mx, my):
        for i in range(0, len(self.buttons)):
            if self.buttons[i].check_mouse_click(mx, my):
                # return the corresponding player
                return self.players[i]
        return None
