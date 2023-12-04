#this class defines all the ai functions we will be using
import random
import itertools

class Ai:
    def __init__(self, player, move):
        self.search = player.search
        self.player = player
        self.unsunkOppShips = player.unsunkOppShips
        self.move = move
        self.spiral = [44, 35, 56, 65, 53, 47, 74, 62, 32, 23, 26, 77, 41, 14, 38, 68, 86, 83, 71, 17, 59, 95, 50, 5, 11, 29, 92, 20, 2, 8, 89, 98, 80]
        self.boards = {}

    def makeMove(self):
        move = self.move(self)
        return move

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

    # Generates a heat map of all possible ship locations and fires at the most likely spot
    def heatMove(self):

        # Start by engaging in a spiral pattern until achieving the first hit (Rodin 1988)
        unsunk = [i for i, square in enumerate(self.search) if square == "H"]

        
        # Opener to sink one ship
        if len(self.unsunkOppShips) == 5 and len(unsunk) == 0:

            # Fire on spiral
            return self.spiral[self.player.moves - 1]
            
        # Randomize unsunk list
        random.shuffle(unsunk)
        
        # One hit
        if len(unsunk) == 1:
            return self.hunt(unsunk)
        
        # Multiple hits
        if len(unsunk) > 1:
            return self.smartHunt(unsunk)
        
        # No hits use heatmap
        # NOTES: only look at unkown squares to generate coordinate permutations
        # goal here is to generate every coordinate list that represents a possible placement of the remaining ships
        # look at every U square, generate every combination of ship coordinates with 2 orientations per and check their validity
        # is valid should return the list of squares, making the validity lists dictionaries that take in board descriptions and return
        # the squares occupied by the ships if it is valid and None if it isn't

        # Generate lists of ship placements, one for each size, checked against the state of the board
        ships = [[], [], [], []]
        freeSquares = [i for i, square in enumerate(self.search) if square == "U"]
        occupiedSquares = [i for i, square in enumerate(self.search) if square != "U"]
        for square in freeSquares:

            # Ship that we're checking
            ship = [square]

            # Horizontal orientation case
            for index in range(1, 5):

                # Check if the next square is over the edge or already occupied
                if (square % 10) + index > 9 or square + index in occupiedSquares:
                    break
                
                # If the placable zone is longer than one, add it to the appropriate list
                ship.append(square + index)
                ships[index - 1].append(tuple(ship))

            # Ship that we're checking
            ship = [square]

            # Vertical orientation case
            for index in range(1, 5):

                # If the square is over the edge or already occupied
                if square + (index * 10) > 99 or square + (index * 10) in occupiedSquares:
                    break
                
                # If the placable zone is longer than one, add it to the appropriate list
                ship.append(square + (index * 10))
                ships[index - 1].append(tuple(ship))

        # Iterate through all of the placement combinations for the unsunk ships
        heatMap = [0] * 100
        unsunkShips = []
        for num in self.unsunkOppShips:
            unsunkShips.append(ships[num - 2])
        length = sum(self.unsunkOppShips)
        counter = 0
        for config in itertools.product(*unsunkShips):
            #counter += 1
            configSquares = set(itertools.chain.from_iterable(config))
            # If there is an overlap, then the lengths will not match up
            #if counter % 10000000 == 0:
                #print(configSquares)
            if length == len(configSquares):
                for square in configSquares:
                    heatMap[square] += 1
                        
        #print(heatMap)

        highest = max(heatMap)
        bestMoves = [i for i, square in enumerate(heatMap) if square == highest]

        return random.choice(bestMoves)
    
    # Valid board sub-method
    def isValid(self, coordinates, orientations, ships):
        
        # Tuple key
        tupleKey = (tuple(coordinates), tuple(orientations), tuple(ships))

        # Check if we've previously calculated the validity
        if tupleKey in self.boards:
            print("Already Seen", coordinates, orientations, ships)
            return self.boards[tupleKey]
        
        # Calculate the validity
        else:
            # print("Testing config", coordinates, orientations, ships, "for the first time")

            # Squares that cannot be hiding ships
            occupiedSquares = [i for i, square in enumerate(self.search) if square != "U"]

            # Output of ship occupied spaces in this board
            shipSquares = []

            # Loop through the ships in the board
            for shipNum in range(len(ships)):

                # Horizontal orientation case
                if orientations[shipNum] == 0:

                    # Loop through each square this ship occupies
                    for index in range(ships[shipNum] - 1):

                        # If the square is over the edge or already occupied
                        if (coordinates[shipNum] % 10) + index > 9 or coordinates[shipNum] + index in occupiedSquares or coordinates[shipNum] + index in shipSquares:

                            # Mark as invalid
                            self.boards[tupleKey] = None
                            return None
                        
                        # Add to ship squares
                        shipSquares.append(coordinates[shipNum] + index)

                # Vertical orientation case
                else:

                    # Loop through each square this ship occupies
                    for index in range(ships[shipNum] - 1):

                        # If the square is over the edge or already occupied
                        if coordinates[shipNum] + (index * 10) > 99 or coordinates[shipNum] + (index * 10) in occupiedSquares or coordinates[shipNum] + (index * 10) in shipSquares:

                            # Mark as invalid
                            self.boards[tupleKey] = None
                            return None
                        
                        # Add to ship squares
                        occupiedSquares.append(coordinates[shipNum] + (index * 10))
            
            # If we found no conflicts append to valid boards and return true
            self.boards[tupleKey] = shipSquares
            return shipSquares   

    
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