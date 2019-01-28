from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


import time

def path_finder(cur_loc, target_loc, mental_map, grid_width, grid_height):
    grid = Grid(matrix=mental_map)
    start = grid.node(cur_loc[0], cur_loc[1])
    end = grid.node(target_loc[0], target_loc[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    path, _ = finder.find_path(start, end, grid)

    return path[1:]

if __name__ == "__main__":
    path_finder((0,0), (4,5), [(1,4),(2,3),(3,3),(3,4),(3,5),(3,3)], grid_width=10, grid_height=10)
