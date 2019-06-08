from game import TilesGame 
from game import GameCollection 
from player import PlayerCollection

# grid instance to test the positioning and drawing of a grid in Processing
grid_size = (1920, 1080)
status = 0
player_collection = None
current_player = None
game_collection = None
current_game = None

def setup():
    # set canvas size; use same size as the one given to the grid
    global grid_size
    global player_collection
    global game_collection
    
    title_font = createFont("SEASRN__.ttf", 50)
    text_font = createFont("Lato-Regular.ttf", 20)
    bk_img = loadImage("bk_hd.jpg");

    player_collection = PlayerCollection("players.txt", grid_size[0], grid_size[1], title_font, bk_img)
    game_collection = GameCollection(grid_size[0], grid_size[1], title_font, text_font, bk_img)
    
    size(grid_size[0], grid_size[1])
    # set initial stroke for line colors
    stroke(255)
    frameRate(30)
    
def draw():
    global status
    global player_collection
    global game_collection
    global current_game
    # reset background to black
    background(0)
    # draw 
    if status == 0:
        player_collection.draw()
    elif status == 1:
        game_collection.draw()
    elif status == 2:
        current_game.draw()
    stroke(255)
    
def mouseClicked():
    global status
    global player_collection
    global game_collection
    global current_game
    global current_player
    
    if mouseButton == LEFT:
        if status == 0:
            current_player = player_collection.mouseAction(mouseX, mouseY)
            if current_player is not None:
                current_player.show()
                status = 1
        elif status == 1:
            current_game = game_collection.mouseAction(mouseX, mouseY)
            if current_game is not None:
                current_game.show()
                status = 2
                current_game.start()
        elif status == 2:
            current_game.mouseAction(mouseX, mouseY)

def mouseMoved():
    global status
    global player_collection
    global game_collection
    global current_game
    if status == 0:
        player_collection.mouseMoving(mouseX, mouseY)
    elif status == 1:
        game_collection.mouseMoving(mouseX, mouseY)
    elif status == 2:
        current_game.mouseMoving(mouseX, mouseY)
