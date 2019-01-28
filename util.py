from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
# from pathfinding.finder.ida_star import IDAStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder


import time

def path_finder(cur_loc, target_loc, mental_map, grid_width, grid_height):
    grid = Grid(matrix=mental_map)
    start = grid.node(cur_loc[0], cur_loc[1])
    end = grid.node(target_loc[0], target_loc[1])

    finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)

    path, runs = finder.find_path(start, end, grid)
    # print(runs)
    # print(path)
    # print('operations:', runs, 'path length:', len(path))
    # print(grid.grid_str(path=path, start=start, end=end))
    
    # print(f"time: {step_2} {step_3}")
    return path[1:]

if __name__ == "__main__":
    path_finder((0,0), (4,5), [(1,4),(2,3),(3,3),(3,4),(3,5),(3,3)], grid_width=10, grid_height=10)
