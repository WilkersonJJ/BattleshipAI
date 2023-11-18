import pygame

pygame.init()
pygame.display.set_caption("Battleship")

#GLOBAL VARIABLES HERE
SQUARE_SIZE = 25
H_MARGINS = SQUARE_SIZE * 4
V_MARGINS = SQUARE_SIZE
HEIGHT = SQUARE_SIZE * 10 * 2 + 3 * V_MARGINS
WIDTH = SQUARE_SIZE * 10 * 2 + H_MARGINS
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

#PALLETE
GREY = (40, 50, 60)
BLUEGREY = (100, 100, 150)
WHITE = (255, 255, 255)

def draw_grid(left = 0, top = 0):
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE
        y = top + i // 10 * SQUARE_SIZE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 1)

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

        pygame.display.flip()
