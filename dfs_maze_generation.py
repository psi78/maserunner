import pygame
import random

ROWS = 15
COLS = 20
CELL_SIZE = 40
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

northWall = [[1 for _ in range(COLS)] for _ in range(ROWS + 1)]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generation")
clock = pygame.time.Clock()

# ----------------------------
# DRAW MAZE
# ----------------------------
def draw_maze():
    screen.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            if northWall[r][c] == 1:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (c * CELL_SIZE, r * CELL_SIZE),
                    ((c + 1) * CELL_SIZE, r * CELL_SIZE),
                    3
                )
            if eastWall[r][c + 1] == 1:
                pygame.draw.line(
                    screen,
                    BLACK,
                    ((c + 1) * CELL_SIZE, r * CELL_SIZE),
                    ((c + 1) * CELL_SIZE, (r + 1) * CELL_SIZE),
                    3
                )
    pygame.draw.line(screen, BLACK, (0, ROWS * CELL_SIZE), (COLS * CELL_SIZE, ROWS * CELL_SIZE), 3)
    pygame.draw.line(screen, BLACK, (0, 0), (0, ROWS * CELL_SIZE), 3)

# ----------------------------
# GENERATE MAZE
# ----------------------------
def generate_maze():
    stack = []
    current = (0, 0)
    visited = set()
    visited.add(current)

    while len(visited) < ROWS * COLS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        r, c = current
        neighbors = []
        if r > 0 and (r-1, c) not in visited:
            neighbors.append((r-1, c, "N", r, c))
        if r < ROWS-1 and (r + 1, c) not in visited:
            neighbors.append((r + 1, c, "N", r + 1, c))
        if c > 0 and (r, c-1) not in visited:
            neighbors.append((r, c-1, "E", r, c))
        if c < COLS-1 and (r, c + 1) not in visited:
            neighbors.append((r, c + 1, "E", r, c + 1))

        if neighbors:
            nr, nc, wall_type, wr, wc = random.choice(neighbors)
            if wall_type == "N":
                northWall[wr][wc] = 0
            else:
                eastWall[wr][wc] = 0

            stack.append(current)
            current = (nr, nc)
            visited.add(current)
        elif stack:
            current = stack.pop()

        draw_maze()
        pygame.draw.rect(
            screen,
            GREEN,
            (
                current[1] * CELL_SIZE + 8,
                current[0] * CELL_SIZE + 8,
                CELL_SIZE- 16,
                CELL_SIZE- 16
            )
        )
        pygame.display.flip()
        clock.tick(30)

generate_maze()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()