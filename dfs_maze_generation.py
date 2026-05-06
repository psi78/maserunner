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
RED = (220, 20, 60)
BLUE = (30, 144, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH + CELL_SIZE, HEIGHT))
pygame.display.set_caption("Maze Generation")
clock = pygame.time.Clock()

# ----------------------------
# DRAW MAZE
# ----------------------------
def draw_maze(path=None, dead_ends=None):
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

    if dead_ends:
        for r, c in dead_ends:
            pygame.draw.circle(
                screen,
                BLUE,
                (
                    c * CELL_SIZE + CELL_SIZE // 2,
                    r * CELL_SIZE + CELL_SIZE // 2
                ),
                CELL_SIZE // 6
            )

    if path:
        for r, c in path:
            pygame.draw.circle(
                screen,
                RED,
                (
                    c * CELL_SIZE + CELL_SIZE // 2,
                    r * CELL_SIZE + CELL_SIZE // 2
                ),
                CELL_SIZE // 4
            )

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

    # BONUS FEATURE:
    # Randomly remove extra walls to create cycles
    if random.randint(1, 20) == 1:
        rr = random.randint(1, ROWS - 1)
        cc = random.randint(1, COLS - 1)
        northWall[rr][cc] = 0

# ----------------------------
# CREATE OPENINGS
# ----------------------------
def create_openings():
    start_row = random.randint(0, ROWS - 1)
    end_row = random.randint(0, ROWS - 1)
    # Entrance
    eastWall[start_row][0] = 0
    # Exit
    eastWall[end_row][COLS] = 0
    return (start_row, 0), (end_row, COLS - 1)

start_cell, end_cell = create_openings()

generate_maze()
create_openings()

# ----------------------------
# SOLVE MAZE
# ----------------------------
def solve_maze(start, end):
    stack = [start]
    visited = set()
    visited.add(start)
    dead_ends = set()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current = stack[-1]
        if current == end:
            draw_maze(stack, dead_ends)
            pygame.display.flip()
            return

        r, c = current
        moves = []
        if r > 0:
            if northWall[r][c] == 0:
                if (r-1, c) not in visited:
                    moves.append((r-1, c))
        if r < ROWS-1:
            if northWall[r + 1][c] == 0:
                if (r + 1, c) not in visited:
                    moves.append((r + 1, c))
        if c > 0:
            if eastWall[r][c] == 0:
                if (r, c-1) not in visited:
                    moves.append((r, c-1))
        if c < COLS-1:
            if eastWall[r][c + 1] == 0:
                if (r, c + 1) not in visited:
                    moves.append((r, c + 1))

        if moves:
            next_cell = random.choice(moves)
            stack.append(next_cell)
            visited.add(next_cell)
        else:
            dead_ends.add(stack.pop())

        draw_maze(stack, dead_ends)
        pygame.display.flip()
        clock.tick(15)

# Draw final red dot exiting maze
exit_x = COLS * CELL_SIZE + CELL_SIZE // 4
exit_y = end[0] * CELL_SIZE + CELL_SIZE // 2
pygame.draw.circle(
    screen,
    RED,
    (exit_x, exit_y),
    CELL_SIZE // 4
)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()