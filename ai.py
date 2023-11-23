#this class defines all the ai functions we will be using
import random

class Ai:
    def __init__(self, player, move):
        self.search = player.search
        self.player = player
        self.move = move

    def makeMove(self):
        randomMove = self.move(self)
        return randomMove

    # Fires at a random untouched square
    def randomMove(self):
        unknowns = [i for i, square in enumerate(self.search) if square == "U"]
        randomChoice = random.choice(unknowns)
        return randomChoice

    # Fires at a random untouched square until it gets a hit, then shoots only adjacent to hits until the ship is sunk
    def randomHuntMove(self):
        unsunk = [i for i, square in enumerate(self.search) if square == "H"]
        if len(unsunk) == 0:
            return self.randomMove()
        return self.hunt(unsunk)
    
    def hunt(self, unsunk):
        for square in unsunk:
            for neighbor in self.adjacentSquares(square):
                if self.search[neighbor] == "U":
                    return neighbor
        return 0
    
    def adjacentSquares(self, square):
        adjacent = []
        if square < 90:
            adjacent.append(square + 10)
        if square > 9:
            adjacent.append(square - 10)
        if square%10 < 9:
            adjacent.append(square + 1)
        if square%10 > 0:
            adjacent.append(square - 1)
        return adjacent