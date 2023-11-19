import pygame
from engine import Player

pygame.init()
pygame.display.set_caption("Battleship")

#GLOBAL VARIABLES HERE
SQUARE_SIZE = 25
H_MARGINS = SQUARE_SIZE * 4
V_MARGINS = SQUARE_SIZE
HEIGHT = SQUARE_SIZE * 10 * 2 + 3 * V_MARGINS
WIDTH = SQUARE_SIZE * 10 * 2 + H_MARGINS
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 5

#PALLETE
GREY = (40, 50, 60)
BLUEGREY = (100, 100, 150)
WHITE = (255, 255, 255)
GREEN = (0, 200, 70)
BLUE = (0, 50, 200)

def draw_grid(left = 0, top = 0):
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE
        y = top + i // 10 * SQUARE_SIZE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 1)

#the main drawing method for ships
def draw_ships(player, left = 0, top = 0, color = GREEN):
    for ship in player.ships:
        x = left + ship.col * SQUARE_SIZE + INDENT
        y = top + ship.row * SQUARE_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size * SQUARE_SIZE - 2*INDENT
            height = SQUARE_SIZE - 2*INDENT
        else:
            width = SQUARE_SIZE - 2*INDENT
            height = ship.size * SQUARE_SIZE - 2*INDENT
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, color, rectangle, border_radius= 15)

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
        SCREEN.fill(GREY)
        draw_grid(SQUARE_SIZE, SQUARE_SIZE)
        draw_grid(WIDTH - 11 * SQUARE_SIZE, SQUARE_SIZE)
        draw_grid(SQUARE_SIZE, HEIGHT - 11 *SQUARE_SIZE)
        draw_grid(WIDTH - 11 * SQUARE_SIZE, HEIGHT - 11 * SQUARE_SIZE)

        draw_ships(player1, left = WIDTH - 10 * SQUARE_SIZE)
        draw_ships(player2, top = HEIGHT - 11 * SQUARE_SIZE, color = BLUE)


        pygame.display.flip()
