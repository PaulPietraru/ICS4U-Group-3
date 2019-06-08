class PlayerCollection():
    def __init__(self, file_name, canvas_w, canvas_h, pc_font, pc_bk_img):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.pc_font = pc_font
        self.pc_bk_img = pc_bk_img
        
        self.button_vertical_space = (self.canvas_h - 100) / 10
        self.button_vertical_gap = self.button_vertical_space / 3
        self.button_height = self.button_vertical_space - self.button_vertical_gap
        
        bx = canvas_w / 2 - 250
        by = 100
        tx = canvas_w / 2 
        ty = by + self.button_height / 2
        
        self.player_names = loadStrings(file_name).tolist()
        #print(self.player_names)
        self.players = [None for i in range(len(self.player_names))]
        for i in range(0, len(self.player_names)):
            self.players[i] = Player(self.player_names[i], 5)
            self.players[i].set_button(bx, by + self.button_vertical_space * i, 500, self.button_height, tx, ty + self.button_vertical_space * i, self.button_height * 0.5)
            
    def draw(self):
        background(self.pc_bk_img)
        textFont(self.pc_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Name", self.canvas_w / 2, 50)
        for p in self.players:
            p.draw_button()
            
    def mouseMoving(self, mx, my):
        for p in self.players:
            p.check_mouse_over(mx, my)
 
    def mouseAction(self, mx, my):
        for p in self.players:
            if p.check_mouse(mx, my):
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
        
    def show(self):
        print(self.name, self.lives)
        
    def set_button(self, bx, by, bw, bh, tx, ty, th):
        self.bx = bx
        self.by = by
        self.bw = bw
        self.bh = bh
        self.tx = tx
        self.ty = ty
        self.th = th
        self.mouse_over = False
        
    def draw_button(self):    
        stroke(200, 200, 200)
        fill(127, 127, 127)
        rect(self.bx, self.by, self.bw, self.bh, 30)
        textAlign(CENTER, CENTER);
        textSize(self.th)
        fill(255, 255, 255)
        text(self.name, self.tx, self.ty)
        self.highlight()
        
    def highlight(self):
        if self.mouse_over:
            strokeWeight(3)
            fill(255, 0, 255, 30)
            rect(self.bx, self.by, self.bw, self.bh, 30)
            strokeWeight(1)
 
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
