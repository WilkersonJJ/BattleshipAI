import pygame
from engine import *
from ai import Ai
from constants import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
font = pygame.font.SysFont("fresansttf", 50)
smallfont = pygame.font.SysFont("fresansttf", 15)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

global recorded
global p1Label
global p2Label

recorded = False
p1Label = ""
p2Label = ""

def draw_grid(boardNum):
    left = BUFFER
    top = BUFFER
    #top right and bot right boards
    if boardNum == 2 or boardNum == 4:
        left = 2* BUFFER + BOARDHEIGHT
    #bot left and bot right boards
    if boardNum == 3 or boardNum == 4:
        top = 2*BUFFER + BOARDHEIGHT
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE
        y = top + i // 10 * SQUARE_SIZE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, BOARDCOLOR, square, width = 1)

def draw_missiles(player, left = BUFFER):
    #loop through and update all hits and misses
    #every square has a circle in it, some are just invisible
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE + (SQUARE_SIZE // 2)
        y = BUFFER + i // 10 * SQUARE_SIZE + (SQUARE_SIZE // 2)
        pygame.draw.circle(SCREEN, MISSILECOLORS[player.search[i]], (x, y), radius=SQUARE_SIZE/3)
        if player.search[i] == "M":
            pygame.draw.circle(SCREEN, BOARDCOLOR, (x, y), radius=SQUARE_SIZE/3, width=2)


#the main drawing method for ships
def draw_ships(player, left = BUFFER, color = PLAYER1COLOR):
    top = BUFFER * 2 + BOARDHEIGHT
    for ship in player.ships:
        x = left + (ship.col * SQUARE_SIZE) + INDENT
        y = top + (ship.row * SQUARE_SIZE) + INDENT
        if ship.orientation == "h":
            width = ship.size * SQUARE_SIZE - 2*INDENT
            height = SQUARE_SIZE - 2*INDENT
        else:
            width = SQUARE_SIZE - 2*INDENT
            height = ship.size * SQUARE_SIZE - 2*INDENT
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, color, rectangle, border_radius = 15)

def draw_labels():
    global p1Label
    global p2Label
    p1Label = "Player 1: "
    p2Label = "Player 2: "
    if HUMAN1:
        p1Label += "Human"
    else:
        p1Label += "AI "
        p1Label += list(moveType.keys())[list(moveType.values()).index(COMPUTER1)]
    if HUMAN2:
        p2Label += "Human"
    else:
        p2Label += "AI "
        p2Label += list(moveType.keys())[list(moveType.values()).index(COMPUTER2)]

    txt1 = smallfont.render(p1Label, False, BOARDCOLOR, BACKGROUNDCOLOR)
    txt2 = smallfont.render(p2Label, False, BOARDCOLOR, BACKGROUNDCOLOR)
    SCREEN.blit(txt1, (BUFFER, BUFFER - 15))
    SCREEN.blit(txt2, (2*BUFFER + BOARDHEIGHT, BUFFER -15))

#writes our results to a csv
def appendResults(winner, moves, p1, p2, recorded):
    p1Str = p1.split(": ")[1]
    p2Str = p2.split(": ")[1]
    if not recorded:
        string = p1Str + "," + p2Str + "," + str(winner) + "," + moves
        f = open(RESULTFILE, 'a')
        f.write(string + "\n")
        f.close()
    recorded = True

game = Game(HUMAN1, HUMAN2)
ai1 = Ai(game.player1, COMPUTER1)
ai2 = Ai(game.player2, COMPUTER2)
runCounter = 0

#this is the main loop of pygame
running = True
pausing = False
while running:
    for event in pygame.event.get():
        #if we close the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Adjust mouse cords for lines
            x -= 5
            y += 5
            leftSide1 = BUFFER
            rightSide1 = BUFFER + BOARDHEIGHT
            leftSide2 = BUFFER * 2 + BOARDHEIGHT
            rightSide2 = 2*BUFFER + 2* BOARDHEIGHT
            topSide = BUFFER
            botSide = BUFFER + BOARDHEIGHT
            #if its player 1's turn and they clicked correctly
            if game.player1Turn and x < rightSide1 and x > leftSide1 and y < botSide and y > topSide:
                row = (y - BUFFER) // SQUARE_SIZE
                col = x // SQUARE_SIZE
                index = row * 10 + col - 1
                if index >= 0 and index <= 99 and game.player1.search[index] == "U":
                    game.makeMove(index)
            #if its player 2's turn and they clicked correctly
            if (not game.player1Turn) and x < rightSide2 and x > leftSide2 and y < botSide and y > topSide:
                row = (y - 2*BUFFER) // SQUARE_SIZE
                col = (x - BUFFER) // SQUARE_SIZE
                index = row * 10 + col - 1
                if index >= 0 and index <= 99 and game.player2.search[index] == "U":
                    game.makeMove(index)

        #on keypress
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                pausing = not pausing
    if not pausing:
        SCREEN.fill(BACKGROUNDCOLOR)
        #draws boards 1 through 4
        for i in range(4):
            draw_grid(i+1)
        draw_missiles(game.player1)
        draw_missiles(game.player2, left = 2*BUFFER + BOARDHEIGHT)

        draw_labels()

        if not HIDEBOARD:
            draw_ships(game.player1, color = PLAYER1COLOR)
            draw_ships(game.player2, left = (BOARDHEIGHT + 2*BUFFER), color = PLAYER2COLOR)

        #if its the computer's turn
        if not game.gameOver and game.computerTurn:
            if game.player1Turn:
                aiMove = ai1.makeMove()
                game.makeMove(aiMove)
            else:
                aiMove = ai2.makeMove()
                game.makeMove(aiMove)

        #game over
        if game.gameOver:
            #final draw ships, just in case the board was covered
            draw_ships(game.player1, color = PLAYER1COLOR)
            draw_ships(game.player2, left = (BOARDHEIGHT + 2*BUFFER), color = PLAYER2COLOR)
            #final draw missiles
            draw_missiles(game.player1)
            draw_missiles(game.player2, left = 2*BUFFER + BOARDHEIGHT)
            movesString = str(game.player1.moves) if game.player1Turn else str(game.player2.moves)
            string = game.winner + " Wins!" + " Moves: " + movesString
            textbox = font.render(string, False, BOARDCOLOR, WHITE)
            appendResults(game.winner, movesString, p1Label, p2Label, recorded)
            SCREEN.blit(textbox, (WIDTH//2 - 250, HEIGHT//4))
            pausing = True

            if AUTORESTART and runCounter < NUMOFRUNS:
                #make a new game and play infinitely
                game = Game(HUMAN1, HUMAN2)
                ai1 = Ai(game.player1, COMPUTER1)
                ai2 = Ai(game.player2, COMPUTER2)
                pausing = False
                runCounter += 1
            
        pygame.time.wait(TICKRATE)
        pygame.display.flip()