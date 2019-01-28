from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.ida_star import IDAStarFinder


import time

def path_finder(cur_loc, target_loc, obstacles, grid_width, grid_height):
    start_time = time.time()
    grid_map = [[1 if (x, y) not in obstacles else 0 for x in range(grid_width)]
                for y in range(grid_height)]
    end_time = time.time()
    step_1 = end_time  - start_time

    grid = Grid(matrix=grid_map)
    start = grid.node(cur_loc[0], cur_loc[1])
    end = grid.node(target_loc[0], target_loc[1])

    start_time = time.time()
    finder = IDAStarFinder(diagonal_movement=DiagonalMovement.always)
    end_time = time.time()
    step_2 = end_time  - start_time
    # print(f"finding path from ({start.x}, {start.y}) to ({end.x}, {end.y})")
    start_time = time.time()
    path, runs = finder.find_path(start, end, grid)
    end_time = time.time()
    step_3 = end_time  - start_time
    # print(path)
    # print('operations:', runs, 'path length:', len(path))
    # print(grid.grid_str(path=path, start=start, end=end))
    
    print(f"time: {step_1} {step_2} {step_3}")
    return path[1:]

if __name__ == "__main__":
    path_finder((0,0), (4,5), [(1,4),(2,3),(3,3),(3,4),(3,5),(3,3)], grid_width=10, grid_height=10)
