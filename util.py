from astar import astar


def path_finder(cur_loc, target_loc, grid):
    path = astar(grid, cur_loc, target_loc)
    return path[1:]
