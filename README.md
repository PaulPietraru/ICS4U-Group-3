# ICS4U-Group-3

This is the repository for the tiles_game project.

Clone this project into a local folder named tiles_game. This is required by Processing.
Ideally this folder should be under the sketchbook location folder configured in Processing preferences.

The initial commit was done on branch master. 
Each member of the project should create a branch with his own name (example: PaulPietraru) and work on that branch.

We will decide when to merge each work branch in the master branch based on the evolution of the project.

June 5th, 2019

Paul: I merged my branch into master. At this moment the master branch code behaves like this:
	- On run it generates a random game level
	- The level is shown for 5 seconds; during this time the mouse is inactive
	- After 5 seconds the tiles are turned (hidden) and the game can be played for 10 seconds
	- Each click is either a failed guess (x) or a good guess (tile color is shown)
	- After 10 seconds the level ends and the status is shown with guessed tiles marked green and the rest marked red

June 8th, 2019

Paul: Latest changes include:
	- Selecting the player name from a list of maximum 10 players.
	  The list is in the data/players.txt file.
	  I limited the list to 10 to keep the screen simple.
	- Selecting a game from a list of maximum 3 games.
	  At the moment the 3 games are just different instances of the one game we have just with different number of tiles.

