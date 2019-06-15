# -------------------------------------------------------------------------------
# Name:           game.py
#
# Purpose:        Defines a game and a level
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------
import random
from gui import GuiVisualParams
from gui import Button
from gui import ScreenArea
from gui import Grid

# A basic tiles game
# Presents a grid with tiles based on a level class
# The purpose of the game is to remember the position of each tile in each level
# This class is the base for other games. By itself it doesn't do anything.
#
# !!! A game has to inherit from this class and implement generate_level and update_level_parameters methods
class TilesGame(object):
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
        """
        self.scores_file_name = "scores_" + self.__class__.__name__ + ".txt"
        self.top_scores = []
        self.load_top_scores()
        
        self.description = ""
        self.bk_img = bk_img
        self.title_font = title_font
        self.text_font = text_font
        
        self.status = self.SELECTING
        self.name = name
        self.num_side_tiles = num_side_tiles
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        
        self.buttons_gvp = GuiVisualParams()
        self.buttons_gvp.text_font = title_font
        
        self.sa_gvp = GuiVisualParams()
        self.sa_gvp.text_font = title_font
        self.sa_gvp.bk_color = (20, 20, 20)
        self.sa_gvp.text_hight_percentage = 0.35
        
        # compute the size of screen parts
        self.compute_screen_areas()
        
        self.num_tiles_set = 5
        self.crt_level_num = 1
        self.show_time = 3000
        self.extra_clicks = 3
        self.current_level = self.generate_level()


    # Create the level instance
    def generate_level(self):
        return None

    # Update the level parameters
    def update_level_parameters(self):
        pass

    # Load the top scores from a file
    def load_top_scores(self):
        self.lines = loadStrings(self.scores_file_name)
        if self.lines != None:
            self.lines = list(l for l in self.lines if l.strip())
            for i in range(len(self.lines)):
                if i == 10:
                    break
                record = self.lines[i].split(',')
                self.top_scores.append((record[0], int(record[1])))
        self.top_scores = sorted(self.top_scores, key=lambda t: t[1], reverse=True)

    def save_top_scores(self):
        self.top_scores = sorted(self.top_scores, key=lambda t: t[1], reverse=True)
        lines = []
        for i in range(len(self.top_scores)):
            if i == 10:
                break
            lines.append(self.top_scores[i][0] + "," + str(self.top_scores[i][1]))
        saveStrings("data/" + self.scores_file_name, lines)

    def set_player(self, player):
        self.status = self.BEFORE_LEVEL
        self.player = player
        self.divide_screen()


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


    def divide_screen(self):
        c1 = 20
        c2 = c1 / 2
        c3 = c1 + c2
        
        self.player_area = ScreenArea(3, self.player_x + c1, self.player_y + c1, self.player_w - c3, self.player_h - c3, self.sa_gvp)
        self.player_area.add_text_element(self.player.name)
        self.lives_element = self.player_area.add_text_element("Lives: " + str(self.player.lives))
        self.score_element = self.player_area.add_text_element("Score: " + str(self.player.points))
        
        self.game_area = ScreenArea(7, self.game_x + c1, self.game_y + c2, self.game_w - c3, self.game_h - c3, self.sa_gvp)
        self.game_area.add_text_element(self.name)
        self.level_element = self.game_area.add_text_element("Level: " + str(self.current_level.level_number))
        self.time_element = self.game_area.add_text_element("Time Playing: " + str(0))
        self.clicks_element = self.game_area.add_text_element("Clicks Left: " + str(0))
        self.tiles_element = self.game_area.add_text_element("Tiles Left: " + str(0))
        self.level_button = self.game_area.add_button_element("Start Level", self.buttons_gvp)
        self.quit_button = self.game_area.add_button_element("Quit Game", self.buttons_gvp)
        
        self.level_area = ScreenArea(1, self.level_x + c2, self.level_y + c1, self.level_w - 2 * c2, self.canvas_h - 2 * c1, self.sa_gvp)
        
        tsa_gvp = GuiVisualParams()
        tsa_gvp.text_font = self.sa_gvp.text_font
        tsa_gvp.bk_color = self.sa_gvp.bk_color
        tsa_gvp.text_hight_percentage = 0.3
        self.top_area = ScreenArea(11, self.top_x + c2, self.top_y + c1, self.top_w - c3, self.canvas_h - 2 * c1, tsa_gvp)
        self.top_area.add_text_element("Top Scores")
        for i in range(len(self.top_scores)):
            if i == 10:
                break
            self.top_area.add_text_element(self.top_scores[i][0] + ": " + str(self.top_scores[i][1]))
                
    def draw(self):
        background(self.bk_img)
        self.player_area.draw()
        self.game_area.draw()
        self.level_area.draw()
        self.top_area.draw()
        if self.status == self.SELECTING or self.status == self.BEFORE_LEVEL:
            pass
        elif self.status == self.PLAY_LEVEL or self.status == self.AFTER_LEVEL:
            self.current_level.draw()
        elif self.status == self.GAME_OVER:
            self.current_level.draw()
            self.draw_game_over_message()
            
        if self.status == self.AFTER_LEVEL:
            self.draw_level_end_message()


    def draw_game_over_message(self):
        textFont(self.title_font, 30)
        textAlign(CENTER, CENTER)
        textSize(120)
        fill(255, 127, 127)
        text("GAME OVER", self.canvas_w / 2, self.canvas_h / 2)


    def draw_level_end_message(self):
        textFont(self.title_font, 30)
        textAlign(CENTER, CENTER)
        textSize(90)
        if self.level_status:
            fill(127, 255, 127)
            text("Well Done", self.canvas_w / 2, self.canvas_h / 2)
        else:
            fill(255, 127, 127)
            text("Try Again", self.canvas_w / 2, self.canvas_h / 2)


    def mouse_clicked(self, mx, my):
        self.current_level.mouseAction(mx, my)
        if self.status == self.BEFORE_LEVEL and self.level_button.check_mouse_click(mx, my):
            self.status = self.PLAY_LEVEL
            self.current_level.show()
            self.clicks_element.update("Clicks Left: " + str(self.current_level.clicks_left))
        elif self.status == self.AFTER_LEVEL and self.level_button.check_mouse_click(mx, my):
            self.current_level = self.generate_level()
            self.status = self.PLAY_LEVEL
            self.current_level.show()
            self.level_element.update("Level: " + str(self.crt_level_num))
            self.clicks_element.update("Clicks Left: " + str(self.current_level.clicks_left))

        if self.quit_button.check_mouse_click(mx, my):
            exit()


    def mouse_moving(self, mx, my):
        self.current_level.mouse_moving(mx, my)
        self.level_button.check_mouse_over(mx, my)
        self.quit_button.check_mouse_over(mx, my)


    def set_level_clicks_left(self, clicks_left):
        self.clicks_element.update("Clicks Left: " + str(clicks_left))


    def set_level_tiles_left(self, tiles_left):
        self.tiles_element.update("Tiles Left: " + str(tiles_left))


    def set_time_played(self, time_played):
        self.time_element.update("Time Playing: " + str(time_played / 1000))


    def current_level_done(self, status):
        if status == Level.FAILED:
            self.player.lose_life()
            self.lives_element.update("Lives: " + str(self.player.lives))
            self.level_status = False
        
        if status == Level.SUCCESS:
            self.player.update_points()
            self.score_element.update("Score: " + str(self.player.points))
            self.update_level_parameters()
            self.level_status = True
        
        if self.player.lives == 0:
            self.top_scores.append((self.player.name, self.player.points))
            self.save_top_scores()
            self.status = self.GAME_OVER
        else:
            self.status = self.AFTER_LEVEL


# A basic level in a game
# Presents a grid with tiles based on a generated layout
# The level implements the rules of the game.
# This class is the base for other games levels. By itself it doesn't do anything.
# A level has these states: SHOW, PLAY, FAILED, SUCCESS
#
# !!! A game level has to inherit from this class and implement: generate_level and evaluate_level methods
class Level(object):
    SHOW = 0
    PLAY = 1
    FAILED = 2
    SUCCESS = 3

    def __init__(self, parent_game, level_number, num_side_tiles, num_tiles_set, show_time, extra_clicks, level_x, level_y, level_w):
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
        
    # Generate a level's tiles positions and colors
    def generate_level(self):
        # Actual levels have to implement this
        pass

    # Evaluate a level status after each click
    def evaluate_level(self, latest_tile_status):
        # Actual levels have to implement this
        pass
    
    # Draw the level in its current status
    def draw(self):
        self.check_time()
        self.grid.draw()
    
    # Check the current time
    def check_time(self):
        current_time = millis()
        if self.status == self.SHOW and current_time - self.show_start_time > self.show_time:
            # hide the level after a number of seconds
            self.hide()
        elif self.status == self.PLAY:
            # set the time played
            self.parent_game.set_time_played(current_time - self.play_start_time)
    
    # Set status to show
    def show(self):
        self.status = self.SHOW
        self.show_start_time = millis()
        self.enable_mouse_action = False
    
    # Set status to play
    def hide(self):
        self.status = self.PLAY
        self.grid.hide_tiles()
        self.tiles_status = self.grid.compute_current_grid_state()
        self.count_hidden_tiles()
        self.play_start_time = millis()
        self.enable_mouse_action = True
    
    # Set status to a done state
    def done(self, done_status):
        self.status = done_status
        self.grid.show_tiles()
        self.count_hidden_tiles()
        self.enable_mouse_action = False
        self.parent_game.current_level_done(self.status)
    
    # React to mouse clicks
    def mouseAction(self, mx, my):
        if self.enable_mouse_action:
            res_tile_status = self.grid.mouseAction(mx, my)
            self.evaluate_level(res_tile_status)
    
    # Check if the grid status has changed
    def grid_status_changed(self, latest_tile_status):
        prev_tile_status = self.tiles_status
        self.tiles_status = latest_tile_status
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if prev_tile_status[ln][cl] != latest_tile_status[ln][cl]:
                    return True
        return False

    # Count the number of hidden tiles
    def count_hidden_tiles(self):
        hidden_tiles = 0
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.set_tiles[ln][cl] and not self.tiles_status[ln][cl]:
                    hidden_tiles = hidden_tiles + 1
        self.parent_game.set_level_tiles_left(hidden_tiles)
        return hidden_tiles
    
    # Check if all the tiles are exposed
    def all_tiles_exposed(self):
        for ln in range(0, self.num_side_tiles):
            for cl in range(0, self.num_side_tiles):
                if self.set_tiles[ln][cl] and not self.tiles_status[ln][cl]:
                    return False
        return True

    # Check if the mouse is moving above the grid
    def mouse_moving(self, mx, my):
        self.grid.mouse_moving(mx, my)
