import random

class Ship:
    def __init__(self, size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["h", "v"])
        self.indexes = self.compute_indexes()

    def __str__(self):
        string = "Ship Object, Position: " + str(self.col) + str(self.row) + " Size: " + str(self.size)
        return string
    
    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i*10 for i in range(self.size)]
        
class Player:
    def __init__(self):
        self.ships = []
        self.search = ["U" for i in range(100)]
        self.place_ships(sizes = [5, 4, 3, 3, 2])
        self.indexes = []
        #get our indexes in one neat list
        for ship in self.ships:
            for i in ship.indexes:
                self.indexes.append(i)

    def place_ships(self, sizes):
        #for each ship in our list, randomly place it on the board
        for size in sizes:
            placed = False
            while not placed:
                ship = Ship(size)
                possible = True
                for i in ship.indexes:
                    if i > 99: #off of board
                        possible = False
                        break
                    #make sure ships arent looping around
                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        possible = False
                        break
                    #check intersections
                    for otherShip in self.ships:
                        if i in otherShip.indexes:
                            possible = False
                            break
                #if its possible, lets place the ship then
                if possible == True:
                    self.ships.append(ship)
                    placed = True

class Game:
    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1Turn = True
        self.gameOver = False
        self.winner = None #stores who won the game
        self.computerTurn = True if not self.human1 else False
    
    def makeMove(self, i):
        player = self.player1 if self.player1Turn == True else self.player2
        opponent = self.player2 if self.player1Turn == True else self.player1

        #if i is a ship
        if i in opponent.indexes:
            player.search[i] = "H"
            #check if the ship has been sunk
            for ship in opponent.ships:
                sunk = True
                for index in ship.indexes:
                    if player.search[index] == "U":
                        sunk = False
                if sunk:
                    for index in ship.indexes:
                        player.search[index] = "S"
        else:
            #miss
            player.search[i] = "M"
        #check if the game is over
        self.gameOver = True
        for i in opponent.indexes:
            if player.search[i] == "U":
                self.gameOver = False
        if self.gameOver:
            self.winner = "Player 1" if self.player1Turn else "Player 2"
        
        self.player1Turn = not self.player1Turn

        #if there is exactly one human playing, switch computer turn
        if (self.human1 ^ self.human2):
            self.computerTurn = not self.computerTurn
        