# -------------------------------------------------------------------------------
# Name:           player.py
#
# Purpose:        A player
#
# Author:         Pietraru.P
# ------------------------------------------------------------------------------

# A player used to keep the player name, lives and points
class Player():
    def __init__(self, name, lives):
        """
        """
        self.name = name
        self.lives = lives
        self.points = 0
    
    # Lose a life
    def lose_life(self):
        self.lives = self.lives - 1
    
    # Gain a point
    def update_points(self):
        self.points = self.points + 1
