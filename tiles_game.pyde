from game import TilesGame 
from game import GameCollection 
from player import PlayerCollection

SELECTING_PLAYER = 0
SELECTING_GAME = 1
PLAYING_GAME = 2

# grid instance to test the positioning and drawing of a grid in Processing
grid_size = (1440, 800)
#grid_size = (1920, 1080)
stage = SELECTING_PLAYER
player_collection = None
current_player = None
game_collection = None
current_game = None

def setup():
    global player_collection
    global game_collection
    
    # load fonts and images
    title_font = createFont("SEASRN__.ttf", 50)
    text_font = createFont("Lato-Regular.ttf", 20)
    bk_img = loadImage("bk.jpg");
    #bk_img = loadImage("bk_hd.jpg");

    # create player and game collections used to select the current player and game
    player_collection = PlayerCollection("players.txt", grid_size[0], grid_size[1], title_font, bk_img)
    game_collection = GameCollection(grid_size[0], grid_size[1], title_font, text_font, bk_img)
    
    # set canvas size and frame rate
    size(grid_size[0], grid_size[1])
    frameRate(30)
    
def draw():
    global stage
    global player_collection
    global game_collection
    global current_game

    if stage == SELECTING_PLAYER:
        player_collection.draw()
    elif stage == SELECTING_GAME:
        game_collection.draw()
    elif stage == PLAYING_GAME:
        current_game.draw()
    stroke(255)
    
def mouseClicked():
    global stage
    global player_collection
    global game_collection
    global current_game
    global current_player
    
    if mouseButton == LEFT:
        if stage == SELECTING_PLAYER:
            current_player = player_collection.mouse_clicked(mouseX, mouseY)
            if current_player is not None:
                stage = SELECTING_GAME
        elif stage == SELECTING_GAME:
            current_game = game_collection.mouse_clicked(mouseX, mouseY)
            if current_game is not None:
                current_game.set_player(current_player)
                stage = PLAYING_GAME
        elif stage == PLAYING_GAME:
            current_game.mouse_clicked(mouseX, mouseY)

def mouseMoved():
    global stage
    global player_collection
    global game_collection
    global current_game
    
    if stage == SELECTING_PLAYER:
        player_collection.mouse_moving(mouseX, mouseY)
    elif stage == SELECTING_GAME:
        game_collection.mouse_moving(mouseX, mouseY)
    elif stage == PLAYING_GAME:
        current_game.mouse_moving(mouseX, mouseY)
