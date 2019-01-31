from astar import astar

def path_finder(cur_loc, target_loc, grid, grid_width, grid_height):
    path = astar(grid, cur_loc, target_loc)
    return path[1:]
