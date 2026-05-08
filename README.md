# Maze Generator and Solver

This project implements a maze generator and solver using Python and Pygame. The maze is generated using a stack-based Depth-First Search (DFS) algorithm, where a "mouse" explores the grid, carving out paths and backtracking when necessary. The solver uses a similar backtracking approach to find a path from the entrance to the exit.

## Features
- **Maze Generation**: The maze is generated using DFS, with random wall removals to create cycles.
- **Maze Solving**: The solver uses backtracking to find a path from the entrance to the exit.
- **Visual Representation**: The maze is displayed using Pygame, with different colors for the generator, solver path, and dead ends.
- THE LOOM RECORDING IS HERE AS FOLLOWS: https://www.loom.com/share/e8b7697471f247d2af5bb36f75a2ae2b

## How It Works
1. **Maze Generation**:
   - The maze starts as a grid with all walls intact.
   - The "mouse" starts at the top-left corner and explores the grid using DFS.
   - Walls are removed to create paths, and random walls are removed to introduce cycles.
2. **Maze Solving**:
   - The solver starts at the entrance and uses backtracking to find a path to the exit.
   - Dead ends are marked in blue, and the solution path is marked in red.

## Data Structures
- **northWall[r][c]**:
  - `1` if the top wall of cell `(r, c)` exists.
  - `0` if the top wall is removed.
- **eastWall[r][c]**:
  - `1` if the right wall of cell `(r, c)` exists.
  - `0` if the right wall is removed.

## Commit History
The commit history reflects the evolution of the project:
1. **Initial grid setup**: Defined the grid and wall data structures.
2. **Implemented mouse movement**: Added the DFS-based maze generation logic.
3. **Added backtracking**: Enhanced the generator and solver with backtracking.
4. **Added cycles and final polish**: Introduced random cycles and improved the visual representation.

## How to Run
1. Install Python and Pygame.
2. Run the script `dfs_maze_generation.py`.
3. Watch the maze being generated and solved in real-time!
