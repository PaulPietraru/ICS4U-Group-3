from game import TilesGame 
from player import PlayerCollection

# grid instance to test the positioning and drawing of a grid in Processing
grid_size = (1440, 800)
status = 0
game = None
player_collection = None
current_player = None

def setup():
    # set canvas size; use same size as the one given to the grid
    global grid_size
    global game
    global player_collection
    
    pc_font = createFont("SEASRN__.ttf", 50)
    pc_bk_img = loadImage("bk.jpg");

    player_collection = PlayerCollection("players.txt", grid_size[0], grid_size[1], pc_font, pc_bk_img)
    game = TilesGame("memory_test", 4, grid_size[0], grid_size[1])
    size(grid_size[0], grid_size[1])
    # set initial stroke for line colors
    stroke(255)
    frameRate(30)
    
def draw():
    global game
    global status
    global player_collection
    # reset background to black
    background(0)
    # draw 
    if status == 0:
        player_collection.draw()
    elif status == 2:
        game.draw()
    stroke(255)
    
def mouseClicked():
    global game
    global status
    global current_player
    if mouseButton == LEFT:
        if status == 0:
            current_player = player_collection.mouseAction(mouseX, mouseY)
            if current_player is not None:
                current_player.show()
                status = 2
                game.start()
        elif status == 2:
            game.mouseAction(mouseX, mouseY)

def mouseMoved():
    global game
    global status
    if status == 0:
        player_collection.mouseMoving(mouseX, mouseY)
    elif status == 2:
        game.mouseMoving(mouseX, mouseY)
