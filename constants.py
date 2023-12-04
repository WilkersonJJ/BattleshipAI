from ai import *

#Game Speed
TICKRATE = 0

#these variables here determine if we are doing human vs comper or human vs human
HUMAN1 = False
HUMAN2 = False

#Cover the bottom boards
HIDEBOARD = False

#automatically restart the game on win
AUTORESTART = True

#results file
RESULTFILE = "result.csv"

SHIPSIZES = [5, 4, 3, 3, 2]

#these variables here determine the type of AI used by the computer
#Options: Ai.pairitySmartHuntMove, Ai.randomMove, Ai.randomHuntMove, Ai.randomSmartHuntMove
moveType = {"Random": Ai.randomMove, 
            "RandomHunt": Ai.randomHuntMove, 
            "RandomSmartHunt": Ai.randomSmartHuntMove, 
            "Parity": Ai.pairitySmartHuntMove,
            "Heat": Ai.heatMove}
COMPUTER1 = moveType["Random"]
COMPUTER2 = moveType["Heat"]

#Variables for board size
SQUARE_SIZE = 25
BUFFER = 30
BOARDHEIGHT = SQUARE_SIZE * 10
HEIGHT = 3 * BUFFER + 2*BOARDHEIGHT
WIDTH = 3 * BUFFER + 2*BOARDHEIGHT
INDENT = 5

#PALLETES
GREY = (40, 50, 60)
BLUEGREY = (100, 100, 150)
WHITE = (255, 255, 255)
GREEN = (0, 200, 70)
BLUE = (0, 50, 200)

#Pink pallete
BOARDCOLOR = (255, 169, 188)
PLAYER1COLOR = (251, 111, 146)
PLAYER2COLOR = (152, 182, 218)
BACKGROUNDCOLOR = (255, 229, 236)
HITCOLOR = (255, 100, 100)
MISSCOLOR = (255, 230, 255)
SUNKCOLOR = (140, 60, 120)
MISSILECOLORS = {"U": BACKGROUNDCOLOR, "H": HITCOLOR, "M": MISSCOLOR, "S": SUNKCOLOR}