# name: Israel Shimeles id:ugr/7570/16 section:1

# CONFIGURATION
ROWS = 15
COLS = 20
CELL_SIZE = 40

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# WALL DATA STRUCTURES
# northWall[r][c] = 1 if the TOP wall of cell (r,c) exists, 0 if removed
# eastWall[r][c] = 1 if the RIGHT wall of cell (r,c) exists, 0 if removed
# Extra row/column are used for boundary handling.
northWall = [[1 for _ in range(COLS)] for _ in range(ROWS + 1)]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS)]

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Assignment")
clock = pygame.time.Clock()

# MAIN LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    pygame.display.flip()
pygame.quit()