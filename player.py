from gui import Button

class PlayerCollection():
    def __init__(self, file_name, canvas_w, canvas_h, text_font, bk_img):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.text_font = text_font
        self.bk_img = bk_img
        
        self.button_vertical_space = (self.canvas_h - 100) / 10
        self.button_vertical_gap = self.button_vertical_space / 3
        self.button_height = self.button_vertical_space - self.button_vertical_gap
        
        bx = canvas_w / 2 - 250
        by = 100
        tx = canvas_w / 2 
        ty = by + self.button_height / 2
        
        self.player_names = loadStrings(file_name).tolist()
        self.players = [None for i in range(len(self.player_names))]
        for i in range(0, len(self.player_names)):
            self.players[i] = Player(self.player_names[i], 2)
            button = Button(self.player_names[i], bx, by + self.button_vertical_space * i, 500, self.button_height, 30, 0.5, 1, 
                    (200, 200, 200), (127, 127, 127), (255, 255, 255), text_font, (255, 0, 255), 30, 3)
            self.players[i].set_selection_button(button)
            
    def draw(self):
        background(self.bk_img)
        textFont(self.text_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Name", self.canvas_w / 2, 50)
        for p in self.players:
            p.draw_selection_button()
            
    def mouse_moving(self, mx, my):
        for p in self.players:
            p.check_mouse_over(mx, my)
 
    def mouse_clicked(self, mx, my):
        for p in self.players:
            if p.check_button_clicked(mx, my):
                return p
        return None
                
class Player():
    def __init__(self, name, lives):
        """
        """
        self.name = name
        self.lives = lives
        self.points = 0
        self.seconds = 0
        
    def lose_life(self):
        self.lives = self.lives - 1
        
    def update_points(self):
        self.points = self.points + 1
        
    def set_selection_button(self, button):
        self.select_button = button
        
    def draw_selection_button(self):    
        self.select_button.draw()
 
    def check_mouse_over(self, mx, my):
        self.select_button.check_mouse_over(mx, my)
            
    def check_button_clicked(self, mx, my):
        return self.select_button.check_mouse_click(mx, my)
