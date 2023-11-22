#this class defines all the ai functions we will be using
import random

class Ai:
    def __init__(self, player):
        self.search = player.search
        self.playerNum = player

    def makeMove(self):
        randomMove = self.randomMove()
        return randomMove

    def randomMove(self):
        unknowns = [i for i, square in enumerate(self.search) if square == "U"]
        randomChoice = random.choice(unknowns)
        return randomChoice