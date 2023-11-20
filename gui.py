import pygame
from engine import Player

pygame.init()
pygame.display.set_caption("Battleship")

#GLOBAL VARIABLES HERE
SQUARE_SIZE = 25
BUFFER = 30
BOARDHEIGHT = SQUARE_SIZE * 10
HEIGHT = 3 * BUFFER + 2*BOARDHEIGHT
WIDTH = 3 * BUFFER + 2*BOARDHEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 5

#PALLETE
GREY = (40, 50, 60)
BLUEGREY = (100, 100, 150)
WHITE = (255, 255, 255)
GREEN = (0, 200, 70)
BLUE = (0, 50, 200)
#Girlypop pallete
BOARDCOLOR = (255, 179, 198)
PLAYER1COLOR = (251, 111, 146)
PLAYER2COLOR = (152, 182, 218)
BACKGROUNDCOLOR = (255, 229, 236)



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

#the main drawing method for ships
def draw_ships(player, left = BUFFER, top = BUFFER, color = PLAYER1COLOR):
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

player1 = Player()
player2 = Player()

#this is the main loop of pygame
running = True
pausing = False
while running:
    for event in pygame.event.get():
        #if we close the window
        if event.type == pygame.QUIT:
            running = False
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

        draw_ships(player1, left = (BOARDHEIGHT + 2*BUFFER), color = PLAYER1COLOR)
        draw_ships(player2, top = (BOARDHEIGHT + 2*BUFFER), color = PLAYER2COLOR)

        pygame.display.flip()
