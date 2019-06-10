class Button():
    def __init__(self, label, x, y, w, h, r, thp, sw, edge_color, bk_color, text_color, hl_color, hl_transparency):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.thp = thp
        self.sw = sw
        self.hsw = hsw
        self.edge_color = edge_color
        self.bk_color = bk_color
        self.text_color = text_color
        self.hl_color = hl_color
        self.hl_transparency = hl_transparency
        self.mouse_over = False

    def draw(self):
        strokeWeight(self.sw)
        stroke(self.edge_color[0], self.edge_color[1], self.edge_color[2])
        fill(self.bk_color[0], self.bk_color[1], self.bk_color[2])
        rect(self.x, self.y, self.w, self.h, self.r)
        textAlign(CENTER, CENTER);
        textSize(self.h * self.thp)
        fill(self.text_color[0], self.text_color[1], self.text_color[2])
        text(self.label, self.x + self.w / 2, self.y + self.h / 2)
        self.highlight()
        
    def highlight(self):
        if self.mouse_over:
            strokeWeight(self.hsw)
            fill(self.hl_color[0], self.hl_color[1], self.hl_color[2], hl_transparency)
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
