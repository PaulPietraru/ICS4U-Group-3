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
from gui import Button
from gui import TextArea
from gui import ScreenArea
from gui import Grid

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
        
        self.games = [TilesGame("3 Tiles", 3, canvas_w, canvas_h, title_font, text_font, bk_img), 
                      TilesGame("4 Tiles", 4, canvas_w, canvas_h, title_font, text_font, bk_img),
                      TilesGame("5 Tiles", 5, canvas_w, canvas_h, title_font, text_font, bk_img)]
        for i in range(0, len(self.games)):
            button = Button(self.games[i].name, bx, by + self.button_vertical_space * i, bw, bh, 30, 0.6, 1, 
                    (200, 200, 200), (127, 127, 127), (255, 255, 255), title_font, (255, 0, 255), 30, 3)
            text_area = TextArea(self.games[i].description, tx, ty + self.button_vertical_space * i, tw, th, 30, 0.2, 1, 
                                 self.text_font, (200, 200, 200), (240, 240, 240), (50, 50, 50))
            self.games[i].set_select_gui(button, text_area)
            
    def draw(self):
        background(self.bk_img)
        textFont(self.title_font, 50)
        textAlign(CENTER, CENTER);
        textSize(50)
        fill(255, 255, 255)
        text("Select Your Game", self.canvas_w / 2, 50)
        for g in self.games:
            g.draw_selection_gui()
            
    def mouse_moving(self, mx, my):
        for g in self.games:
            g.check_mouse_over(mx, my)
 
    def mouse_clicked(self, mx, my):
        for g in self.games:
            if g.check_mouse(mx, my):
                return g
        return None


class TilesGame():
    """
    A tile game
    """
    
    SELECTING = 0
    BEFORE_LEVEL = 1
    PLAY_LEVEL = 2
    AFTER_LEVEL = 3
    GAME_OVER = 4
    
    def __init__(self, name, num_side_tiles, canvas_w, canvas_h, title_font, text_font, bk_img):
        """
        Initialize the game
        :param name: name of the game
        :param num_side_tiles: number of tiles on the side of the grid
        :param canvas_w: canvas width (for positioning)
        :param canvas_h: canvas height (for positioning)
        """
        
        self.description = """
        Check your short term memory by trying to 
        remember the position of tiles while difficulty
        gradually increases.
        """
        self.bk_img = bk_img
        self.title_font = title_font
        self.text_font = text_font
        
        self.status = self.SELECTING
        self.name = name
        self.num_side_tiles = num_side_tiles
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        
        # compute the size of screen parts
        self.compute_screen_areas()
        
        self.num_tiles_set = 5
        self.current_level = Level(self, 1, self.num_side_tiles, self.num_tiles_set, 3000, 3, self.level_x, self.level_y, self.level_w)

    def compute_screen_areas(self):
        self.level_w = min(self.canvas_w, self.canvas_h)
        self.level_x = (self.canvas_w / 2) - (self.level_w / 2)
        self.level_y = 0
        
        self.player_w = (self.canvas_w - self.level_w) / 2
        self.player_h = self.canvas_h / 3
        self.player_x = 0
        self.player_y = 0
        
        self.game_w = (self.canvas_w - self.level_w) / 2
        self.game_x = 0
        self.game_y = self.player_h
        self.game_h = self.player_h * 2
        
        self.top_w = self.player_w
        self.top_x = self.player_w + self.level_w
        self.top_y = 0
        self.top_h = self.canvas_h

    def set_player(self, player):
        self.status = self.BEFORE_LEVEL
        self.player = player
        self.divide_screen()

    def divide_screen(self):
        c1 = 20
        c2 = c1 / 2
        c3 = c1 + c2
        
        self.player_area = ScreenArea(3, self.player_x + c1, self.player_y + c1, self.player_w - c3, self.player_h - c3, 30,
                            (0, 0, 0), 100, 1, (200, 200, 200), (255, 255, 255), self.title_font)
        self.player_area.add_text_element(self.player.name)
        self.lives_element = self.player_area.add_text_element("Lives: " + str(self.player.lives))
        self.score_element = self.player_area.add_text_element("Score: " + str(self.player.points))
        
        self.game_area = ScreenArea(6, self.game_x + c1, self.game_y + c2, self.game_w - c3, self.game_h - c3, 30,
                            (0, 0, 0), 100, 1, (200, 200, 200), (255, 255, 255), self.title_font)
        self.game_area.add_text_element(self.name)
        self.level_element = self.game_area.add_text_element("Level: " + str(self.current_level.level_number))
        self.time_element = self.game_area.add_text_element("Time Playing: " + str(0))
        self.clicks_element = self.game_area.add_text_element("Clicks Left: " + str(0))
        self.level_button = self.game_area.add_button_element("Start Level", 30, 0.3, 1, (200, 200, 200), (127, 127, 127), (255, 255, 255), (255, 0, 255), 30, 3)
        self.quit_button = self.game_area.add_button_element("Quit Game", 30, 0.3, 1, (200, 200, 200), (127, 127, 127), (255, 255, 255), (255, 0, 255), 30, 3)
        
        self.level_area = ScreenArea(1, self.level_x + c2, self.level_y + c1, self.level_w - 2 * c2, self.canvas_h - 2 * c1, 30,
                            (0, 0, 0), 100, 1, (200, 200, 200), (255, 255, 255), self.title_font)
        self.top_area = ScreenArea(10, self.top_x + c2, self.top_y + c1, self.top_w - c3, self.canvas_h - 2 * c1, 30,
                            (0, 0, 0), 100, 1, (200, 200, 200), (255, 255, 255), self.title_font)
        self.top_area.add_text_element("Top Scores")
        
    def draw(self):
        background(self.bk_img)
        self.player_area.draw()
        self.game_area.draw()
        self.level_area.draw()
        self.top_area.draw()
        if self.status == self.SELECTING:
            None
        elif self.status == self.BEFORE_LEVEL:
            None
        elif self.status == self.PLAY_LEVEL or self.status == self.AFTER_LEVEL:
            self.current_level.draw()
        elif self.status == self.GAME_OVER:
            self.current_level.draw()
            textFont(self.title_font, 30)
            textAlign(CENTER, CENTER);
            textSize(120)
            fill(255, 127, 127)
            text("GAME OVER", self.canvas_w / 2, self.canvas_h / 2)
            
    def mouse_clicked(self, mx, my):
        self.current_level.mouseAction(mx, my)
        if self.status == self.BEFORE_LEVEL and self.level_button.check_mouse_click(mx, my):
            self.status = self.PLAY_LEVEL
            self.current_level.show()
            self.clicks_element.update("Clicks Left: " + str(self.current_level.clicks_left))
        elif self.status == self.AFTER_LEVEL and self.level_button.check_mouse_click(mx, my):
            self.current_level = Level(self, 1, self.num_side_tiles, self.num_tiles_set, 3000, 3, self.level_x, self.level_y, self.level_w)
            self.status = self.PLAY_LEVEL
            self.current_level.show()
            self.clicks_element.update("Clicks Left: " + str(self.current_level.clicks_left))

        if self.quit_button.check_mouse_click(mx, my):
            exit()
    
    def mouse_moving(self, mx, my):
        self.current_level.mouseMoving(mx, my)
        self.level_button.check_mouse_over(mx, my)
        self.quit_button.check_mouse_over(mx, my)
    
    def set_select_gui(self, button, text_area):
        self.select_button = button
        self.select_text_area = text_area 
       
    def draw_selection_gui(self):    
        self.select_button.draw()
        self.select_text_area.draw()
        
    def check_mouse_over(self, mx, my):
        self.select_button.check_mouse_over(mx, my)
            
    def check_mouse(self, mx, my):
        return self.select_button.check_mouse_click(mx, my)

    def set_level_clicks_left(self, clicks_left):
        self.clicks_element.update("Clicks Left: " + str(clicks_left))
    
    def set_time_played(self, time_played):
        self.time_element.update("Time Playing: " + str(time_played / 1000))
        
    def current_level_done(self, status):
        if status == Level.FAILED:
            self.player.lose_life()
            self.lives_element.update("Lives: " + str(self.player.lives))
        
        if status == Level.SUCCESS:
            self.player.update_points()
            self.score_element.update("Score: " + str(self.player.points))
            self.num_tiles_set = self.num_tiles_set + 1
            self.num_side_tiles = self.num_side_tiles + 1
        
        if self.player.lives == 0:
            self.status = self.GAME_OVER
        else:
            self.status = self.AFTER_LEVEL

class Level():
    """
    A level in a game
    """
    SHOW = 0
    PLAY = 1
    FAILED = 2
    SUCCESS = 3

    def __init__(self, parent_game, level_number, num_side_tiles, num_tiles_set, show_time, extra_clicks, level_x, level_y, level_w):
        """
        Initialize the game
        """
        self.parent_game = parent_game
        self.level_number = level_number
        self.num_side_tiles = num_side_tiles
        self.num_tiles_set = num_tiles_set
        self.show_time = show_time
        self.extra_clicks = extra_clicks
        self.clicks_left = self.num_tiles_set + self.extra_clicks
        
        self.level_x = level_x
        self.level_y = level_y
        self.level_w = level_w
        
        self.set_tiles = [[False for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        self.color_tiles = [[(127, 127, 127) for cl in range(self.num_side_tiles)] for ln in range(self.num_side_tiles)]
        self.generate_level()
        
        grid_x = level_x + level_w * 0.05
        grid_y = level_y + level_w * 0.05
        grid_w = level_w * 0.9
        self.grid = Grid(num_side_tiles, grid_x, grid_y, grid_w, self.set_tiles, self.color_tiles)
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
        if self.status == self.SHOW and current_time - self.show_start_time > self.show_time:
            self.hide()
        elif self.status == self.PLAY:
            self.parent_game.set_time_played(current_time - self.play_start_time)
            
    
    def show(self):
        self.status = self.SHOW
        self.show_start_time = millis()
        self.enable_mouse_action = False
        
    def hide(self):
        self.status = self.PLAY
        self.grid.hide_tiles()
        self.tiles_status = self.grid.compute_current_grid_state()
        self.play_start_time = millis()
        self.enable_mouse_action = True
        
    def done(self, done_status):
        self.status = done_status
        self.grid.show_tiles()
        self.enable_mouse_action = False
        self.parent_game.current_level_done(self.status)
        
    def mouseAction(self, mx, my):
        if self.enable_mouse_action:
            res_tile_status = self.grid.mouseAction(mx, my)
            self.evaluate_level(res_tile_status)

    def evaluate_level(self, latest_tile_status):
        if self.grid_status_changed(latest_tile_status):
            self.clicks_left = self.clicks_left - 1
            if self.all_tiles_exposed():
                self.done(self.SUCCESS) # win level
            elif self.clicks_left < self.count_hidden_tiles():
                self.done(self.FAILED) # lose level
            elif self.clicks_left == 0:
                self.done(self.FAILED) # lose level
        self.parent_game.set_level_clicks_left(self.clicks_left)
        
    def grid_status_changed(self, latest_tile_status):
        prev_tile_status = self.tiles_status
        self.tiles_status = latest_tile_status
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if prev_tile_status[ln][cl] != latest_tile_status[ln][cl]:
                    return True
        return False

    def count_hidden_tiles(self):
        hidden_tiles = 0
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.set_tiles[ln][cl] and not self.tiles_status[ln][cl]:
                    hidden_tiles = hidden_tiles + 1
        return hidden_tiles
        
    def all_tiles_exposed(self):
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.set_tiles[ln][cl] and not self.tiles_status[ln][cl]:
                    return False
        return True
        
    def mouseMoving(self, mx, my):
        self.grid.mouseMoving(mx, my)
