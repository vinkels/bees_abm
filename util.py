# from pathfinding.core.diagonal_movement import DiagonalMovement
# from pathfinding.core.grid import Grid
# from pathfinding.finder.a_star import AStarFinder


import time

from astar import astar

def path_finder(cur_loc, target_loc, grid, grid_width, grid_height):
    # start = grid.node(cur_loc[0], cur_loc[1])
    # end = grid.node(target_loc[0], target_loc[1])

    # finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    # path, _ = finder.find_path(start, end, grid)
    # s = time.time()
    path = astar(grid, cur_loc, target_loc)
    # e = time.time()

    # if e - s > 1:
    #     print(f"{grid.tolist()}, {cur_loc}, {target_loc}")

    # print(path, e - s)

    if not path:
        print(cur_loc, target_loc, grid)

    # assert all(x[0] >= 0 and x[1] >= 0 for x in path), path

    # Pathfinding edits grid, so we need to clean it up afterwards.
    # grid.cleanup()

    return path[1:]
