import pandas as pd
import sys


#the way the logic will work for this:
#☐ means empty water
#1 means unhit ship
#X means previous hit ship
#O means previous miss

#TODO:
#set up dual battleship logic

box = "☐"
row = [box for i in range(10)]
letters = ["A", 'B', 'C', "D", "E", "F", 'G', 'H', 'I', 'J']
shipLengths = [2, 3, 3, 4, 5]
shipNames = ["Destroyer", "Cruiser", "Submarine", "Battleship", "Aircraft Carrier"]

#for each key, there is an array with all locations of the ships and a status, 1 for unsunk
shipStatus = {"Destroyer": ([], True), "Cruiser": ([], True), "Submarine": ([], True), 
              "Battleship": ([], True), "Aircraft Carrier": ([], True)} 

boardHeight = 10
isRunning = True
shipSetupMode = True
d = {}

#setting up the empty frame
for _, element in enumerate(letters):
    d[element] = row
df = pd.DataFrame(data = d)

print(df)

#this function checks if we have already tried to fire a missile at this coordinate, 
def isUntouched(x, y):
    value = df.at[y, x]
    #if we have previously hit or missed this coodinate
    if value == 'X' or value == 'O':
        return False
    else:
        return True

#this function returns 1 if there is a ship at the coordinate
def isShip(x, y):
    value = df.at[y, x]
    if value == 1:
        return True #if there is a ship here
    else:
        return False

def setValue(x, y, newValue):
    df.at[y, x] = newValue

def getValue(x, y):
    return df.at[y, x]

#this function simply checks the status of a coordinate, and returns based on that
def sendMissile(x, y):
    if isUntouched(x, y) == 0:
        print("YOU HAVE ALREADY HIT THIS SPOT")
    else:
        if isShip(x, y):
            setValue(x, y, 'X')
            print(df)
            print("HIT!")

            shipName = getShipName(x, y)
            if isShipSank(shipName):
                print("SHIP SANK!", shipName.upper())
            if isGameOver():
                print("YOU HAVE WON!")
                return -1
        else:
            setValue(x, y, 'O')
            print(df)
            print("MISS!")

#this function checks if proposed ship places intersects with other ships or walls
def isLegalShipPlacement(x, y, orientation, length):
    for i in range(length):
        newX = x
        newY = y
        if orientation == "H":
            nextIndex = letters.index(x) + i
            if nextIndex < 0 or nextIndex >= boardHeight:
                return False
            newX = letters[nextIndex]
        if orientation == "V":
            newY = y + i
        if newY < 0 or newY >= boardHeight:
            return False
        if getValue(newX, newY) == 1:
            return False
    return True

#this function actually places the ships
def placeShip(x, y, orientation, length, shipName):
    for i in range(length):
        newX = x
        newY = y
        if orientation == "H":
            nextIndex = letters.index(x) + i
            newX = letters[nextIndex]
        if orientation == "V":
            newY = y + i
        setValue(newX, newY, 1)
        shipStatus[shipName][0].append(newX + str(newY))
    print(df)
    print("Ship Status: ", shipStatus)

#Use this AFTER firing missile, to check if the missile sank the ship
def isShipSank(shipName):
    #if this ship has already been sank
    if shipStatus[shipName][1] == False:
        return True
    for coord in shipStatus[shipName][0]:
        #if any part here is unhit, it is not sank
        if getValue(coord[0], int(coord[1])) == 1:
            return False
    #then set this ship as sank
    shipStatus[shipName] = (shipStatus[shipName][0], False)
    return True

#gets the ship name from the coordinate
def getShipName(x, y):
    string = x + str(y)
    for name in shipNames:
        for coord in shipStatus[name][0]:
            if coord == string:
                return name
    return None

#checks each ship's status
def isGameOver():
    for name in (shipNames):
        #if any ship is still alive, return false
        if shipStatus[name][1] == True:
            return False
    return True

#this function handles the overall part of placing ships
def placeShips():
    print("Place the ships by typing the leftmost or topmost coordinate, followed by H for horizontal and V for vertical placement")
    print("Example: B2H")
    for index in range(len(shipLengths)):
        ship = shipLengths[index]
        shipName = shipNames[index]
        print("Your ship is: ", ship, shipName)
        shipPlaced = False
        while shipPlaced == False:
            input1 = input()
            input1 = input1.upper()
            xInput = input1[0]
            yInput = int(input1[1])
            orientation = input1[2]
            if isLegalShipPlacement(xInput, yInput, orientation, ship):
                shipPlaced = True
                placeShip(xInput, yInput, orientation, ship, shipName)
            else:
                print("That is not a legal placement")

#this begins the main gameplay loop

while (isRunning == True):
    if (shipSetupMode):
        placeShips()
        shipSetupMode = False
        print("All Ships Placed! Begin Firing!")
    input1 = input()
    input1 = input1.upper()
    if (input1 == "STOP"):
        isRunning = False
        continue
    xInput = input1[0]
    yInput = input1[1]
    i = sendMissile(xInput, int(yInput))
    if i == -1:
        isRunning = False