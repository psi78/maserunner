import pygame

ROWS = 15
COLS = 20
CELL_SIZE = 40
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

northWall = [[1 for _ in range(COLS)] for _ in range(ROWS + 1)]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Assignment")
clock = pygame.time.Clock()

# ----------------------------
# DRAW MAZE
# ----------------------------
def draw_maze():
    screen.fill(WHITE)

    for r in range(ROWS):
        for c in range(COLS):
            # TOP WALL
            if northWall[r][c] == 1:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (c * CELL_SIZE, r * CELL_SIZE),
                    ((c + 1) * CELL_SIZE, r * CELL_SIZE),
                    3
                )

            # RIGHT WALL
            if eastWall[r][c + 1] == 1:
                pygame.draw.line(
                    screen,
                    BLACK,
                    ((c + 1) * CELL_SIZE, r * CELL_SIZE),
                    ((c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE),
                    3
                )

    # BOTTOM BORDER
    pygame.draw.line(
        screen,
        BLACK,
        (0, ROWS * CELL_SIZE),
        (COLS * CELL_SIZE, ROWS * CELL_SIZE),
        3
    )

    # LEFT BORDER
    pygame.draw.line(
        screen,
        BLACK,
        (0, 0),
        (0, ROWS * CELL_SIZE),
        3
    )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_maze()
    pygame.display.flip()

pygame.quit()