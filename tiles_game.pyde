from game import TilesGame

# grid instance to test the positioning and drwing of a grid in Processing
grid_size = (1200, 800)
game = TilesGame("memory_test", 9, grid_size[0], grid_size[1])

def setup():
    # set canvas size; use same size as the one given to the grid
    global grid_size
    global game
    size(grid_size[0], grid_size[1])
    # set initial stroke for line colors
    stroke(255)
    frameRate(30)
    game.start()
    
    
def draw():
    global game
    # reset background to black
    background(0)
    # draw the grid
    game.draw()
    stroke(255)
    
def mouseClicked():
    global game
    if mouseButton == LEFT:
        game.mouseAction(mouseX, mouseY)

def mouseMoved():
    global game
    game.mouseMoving(mouseX, mouseY)
