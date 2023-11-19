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
        self.indexes

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

p = Player()
