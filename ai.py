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

        # List of hit but not sunk ships
        unsunk = [i for i, square in enumerate(self.search) if square == "H"]

        # If all ships hit are sunk (no sunk ships is also valid)
        if len(unsunk) == 0:

            # Fire randomly
            return self.randomMove()
        
        # Randomize unsunk list
        random.shuffle(unsunk)
        
        # Else, begin hunting
        return self.hunt(unsunk)

    # Fires at a random untouched square until it gets a hit, then shoots only adjacent to hits until the ship is sunk
    def randomSmartHuntMove(self):

        # List of hit but not sunk ships
        unsunk = [i for i, square in enumerate(self.search) if square == "H"]

        # If all ships hit are sunk (no sunk ships is also valid)
        if len(unsunk) == 0:

            # Fire randomly
            return self.randomMove()
        
        # Randomize unsunk list
        random.shuffle(unsunk)
        
        # If there is only one hit, no need for smart hunt
        if len(unsunk) == 1:
            return self.hunt(unsunk)
        
        # There is more than one hit, use smart hunt
        return self.smartHunt(unsunk)

    # Fires at a random untouched square on an even row until it gets a hit, then shoots only adjacent to hits until the ship is sunk
    def pairitySmartHuntMove(self):

        # List of hit but not sunk ships
        unsunk = [i for i, square in enumerate(self.search) if square == "H"]

        # If all ships hit are sunk (no sunk ships is also valid)
        if len(unsunk) == 0:

            # Fire on pairity
            return self.pairityMove()
        
        # Randomize unsunk list
        random.shuffle(unsunk)
        
        # If there is only one hit, no need for smart hunt
        if len(unsunk) == 1:
            return self.hunt(unsunk)
        
        # There is more than one hit, use smart hunt
        return self.smartHunt(unsunk)
    
    # Hunting mode sub-method
    def hunt(self, unsunk):

        # Loop through hits
        for square in unsunk:

            # Loop through hits in matrix
            for neighbor in self.adjacentSquares(square):

                # If the neighbor is unknown, fire at it
                if self.search[neighbor] == "U":
                    return neighbor
                
        # Should never be reached
        return -1
    
    # Intelligent hunting mode sub-method
    def smartHunt(self, unsunk):

        # Loop through hits
        for square in unsunk:

            # Loop through hits in matrix to determine ship orientation
            for neighbor in self.adjacentSquares(square):

                # If the neighbor is also a hit, fire along orientation
                if self.search[neighbor] == "H":

                    # Move along sequence until we can fire or reach the end
                    prev = square
                    next = neighbor
                    while True:
                        prev, next = self.nextInSequence(prev, next)
                        if next == None:
                            break
                        elif self.search[next] == "H":
                            continue
                        elif self.search[next] == "U":
                            return next
                        else:
                            break
                
        # None of the hits were adjacdent, revert to normal hunt
        return self.hunt(unsunk)

    # Pairity firing sub-method
    def pairityMove(self):
        unknowns = [i for i, square in enumerate(self.search) if square == "U" and (int(i/10) + (i % 10)) % 2 == 0]
        randomChoice = random.choice(unknowns)
        return randomChoice
    
    # Helper method that returns the adjacent squares given a square's coordinates
    def adjacentSquares(self, square):

        # Start with empty adjacency list
        adjacent = []

        # Add neighbors if constraints are not violated
        if square < 90:
            adjacent.append(square + 10)
        if square > 9:
            adjacent.append(square - 10)
        if square % 10 < 9:
            adjacent.append(square + 1)
        if square % 10 > 0:
            adjacent.append(square - 1)
        
        # Randomize adjacency list and return
        random.shuffle(adjacent)
        return adjacent
    
    # Helper method that takes in two adjacent squares and return the next adjacent square in sequence
    def nextInSequence(self, prev, next):

        # Difference can be negative or positive
        difference = next - prev

        # If out of bounds return None
        if (abs(difference) == 1 and ((next % 10) + difference > 9 or (next % 10) + difference < 0)) or (next + difference > 99 or next + difference < 0):
            return next, None
        
        # Return next and new previous
        return next, next + difference