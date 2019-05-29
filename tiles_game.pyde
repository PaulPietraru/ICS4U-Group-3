from game import Grid

# grid instance to test the positioning and drwing of a grid in Processing
grid_size = (1200, 800)
grid = Grid(11, grid_size[0], grid_size[1])

def setup():
    # set canvas size; use same size as the one given to the grid
    global grid_size
    size(grid_size[0], grid_size[1])
    # set initial stroke for line colors
    stroke(255)
    frameRate(30)
    
def draw():
    global grid
    # reset background to black
    background(0)
    # draw the grid
    grid.draw()
    stroke(255)
