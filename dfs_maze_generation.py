import pygame
import random

# =========================================================
# BUILDING AND RUNNING MAZES
# Assignment Solution
# Student: Israel Shimeles
# =========================================================

# -----------------------------
# CONFIGURATION
# -----------------------------
ROWS = 15
COLS = 20
CELL_SIZE = 40

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# ---------------------------------------------------------
# WALL DATA STRUCTURES (AS REQUIRED IN ASSIGNMENT)
#
# northWall[r][c]
#   = 1 if the TOP wall of cell (r,c) exists
#   = 0 if removed
#
# eastWall[r][c]
#   = 1 if the RIGHT wall of cell (r,c) exists
#   = 0 if removed
#
# Extra row/column are used for boundary handling.
# ---------------------------------------------------------

northWall = [[1 for _ in range(COLS)] for _ in range(ROWS + 1)]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS)]

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (220, 20, 60)       # Solver current path
BLUE = (30, 144, 255)     # Dead ends
GREEN = (50, 205, 50)     # Generator mouse

TEXT_COLOR = (40, 40, 40)

# -----------------------------
# PYGAME SETUP
# -----------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH + CELL_SIZE, HEIGHT))
pygame.display.set_caption("Maze Assignment - Israel Shimeles")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22, bold=True)

current_phase = "STARTING..."

# =========================================================
# DRAW MAZE
# =========================================================
def draw_maze(path=None, dead_ends=None):

    screen.fill(WHITE)

    # -----------------------------
    # DRAW WALLS
    # -----------------------------
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

    # -----------------------------
    # DRAW DEAD ENDS (BLUE)
    # -----------------------------
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

    # -----------------------------
    # DRAW CURRENT PATH (RED)
    # -----------------------------
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

    # -----------------------------
    # PHASE TEXT
    # -----------------------------
    text_surface = font.render(current_phase, True, TEXT_COLOR)
    screen.blit(text_surface, (10, 10))


# =========================================================
# GENERATE MAZE USING DFS + STACK
# =========================================================
def generate_maze():

    global current_phase

    current_phase = "PHASE A: GENERATING MAZE"

    # Stack for DFS backtracking
    stack = []

    # Start cell
    current = (0, 0)

    visited = set()
    visited.add(current)

    while len(visited) < ROWS * COLS:

        # -----------------------------------------
        # HANDLE WINDOW EVENTS
        # -----------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        r, c = current

        neighbors = []

        # -----------------------------------------
        # CHECK ALL FOUR NEIGHBORS
        # -----------------------------------------

        # UP
        if r > 0 and (r - 1, c) not in visited:
            neighbors.append((r - 1, c, "N", r, c))

        # DOWN
        if r < ROWS - 1 and (r + 1, c) not in visited:
            neighbors.append((r + 1, c, "N", r + 1, c))

        # LEFT
        if c > 0 and (r, c - 1) not in visited:
            neighbors.append((r, c - 1, "E", r, c))

        # RIGHT
        if c < COLS - 1 and (r, c + 1) not in visited:
            neighbors.append((r, c + 1, "E", r, c + 1))

        # -----------------------------------------
        # IF THERE ARE AVAILABLE NEIGHBORS
        # -----------------------------------------
        if neighbors:

            nr, nc, wall_type, wr, wc = random.choice(neighbors)

            # Remove wall
            if wall_type == "N":
                northWall[wr][wc] = 0
            else:
                eastWall[wr][wc] = 0

            # BONUS:
            # Randomly remove extra walls to create cycles
            if random.randint(1, 20) == 1:

                rr = random.randint(1, ROWS - 1)
                cc = random.randint(1, COLS - 1)

                northWall[rr][cc] = 0

            stack.append(current)

            current = (nr, nc)

            visited.add(current)

        # -----------------------------------------
        # DEAD END -> BACKTRACK
        # -----------------------------------------
        elif stack:
            current = stack.pop()

        # -----------------------------------------
        # DRAW GENERATION
        # -----------------------------------------
        draw_maze()

        # Draw green generator mouse
        pygame.draw.rect(
            screen,
            GREEN,
            (
                current[1] * CELL_SIZE + 8,
                current[0] * CELL_SIZE + 8,
                CELL_SIZE - 16,
                CELL_SIZE - 16
            )
        )

        pygame.display.flip()

        clock.tick(30)

    return True


# =========================================================
# CREATE ENTRANCE AND EXIT
# =========================================================
def create_openings():

    # Entrance at left side
    start_row = random.randint(0, ROWS - 1)
    eastWall[start_row][0] = 0

    # Exit at right side
    end_row = random.randint(0, ROWS - 1)
    eastWall[end_row][COLS] = 0

    return (start_row, 0), (end_row, COLS - 1)


# =========================================================
# SOLVE MAZE USING BACKTRACKING
# =========================================================
def solve_maze(start, end):

    global current_phase

    current_phase = "PHASE B: SOLVING MAZE"

    stack = [start]

    visited = set()
    visited.add(start)

    dead_ends = set()

    while stack:

        # -----------------------------------------
        # HANDLE EVENTS
        # -----------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current = stack[-1]

        # -----------------------------------------
        # MAZE SOLVED
        # -----------------------------------------
        if current == end:

            current_phase = "MAZE SOLVED!"

            draw_maze(stack, dead_ends)

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

            return

        r, c = current

        moves = []

        # -----------------------------------------
        # CHECK POSSIBLE MOVES
        # -----------------------------------------

        # UP
        if r > 0:
            if northWall[r][c] == 0:
                if (r - 1, c) not in visited:
                    moves.append((r - 1, c))

        # DOWN
        if r < ROWS - 1:
            if northWall[r + 1][c] == 0:
                if (r + 1, c) not in visited:
                    moves.append((r + 1, c))

        # LEFT
        if c > 0:
            if eastWall[r][c] == 0:
                if (r, c - 1) not in visited:
                    moves.append((r, c - 1))

        # RIGHT
        if c < COLS - 1:
            if eastWall[r][c + 1] == 0:
                if (r, c + 1) not in visited:
                    moves.append((r, c + 1))

        # -----------------------------------------
        # MOVE FORWARD
        # -----------------------------------------
        if moves:

            next_cell = random.choice(moves)

            stack.append(next_cell)

            visited.add(next_cell)

        # -----------------------------------------
        # DEAD END -> BACKTRACK
        # -----------------------------------------
        else:

            dead_ends.add(stack.pop())

        # -----------------------------------------
        # DRAW SOLVER
        # -----------------------------------------
        draw_maze(stack, dead_ends)

        pygame.display.flip()

        clock.tick(15)


# =========================================================
# MAIN PROGRAM
# =========================================================
running = generate_maze()

if running:

    pygame.time.delay(1000)

    start_cell, end_cell = create_openings()

    solve_maze(start_cell, end_cell)

# =========================================================
# KEEP WINDOW OPEN
# =========================================================
game_running = True

while game_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_running = False

pygame.quit()