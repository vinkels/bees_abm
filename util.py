from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.ida_star import IDAStarFinder


def path_finder(cur_loc, target_loc, obstacles, grid_width, grid_height):
    grid_map = [[1 if (x, y) not in obstacles else 0 for x in range(grid_width)]
                for y in range(grid_height)]
    grid = Grid(matrix=grid_map)
    start = grid.node(cur_loc[0], cur_loc[1])
    end = grid.node(target_loc[0], target_loc[1])
    finder = IDAStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    # print(path)
    # print('operations:', runs, 'path length:', len(path))
    # print(grid.grid_str(path=path, start=start, end=end))
    return path[1:]

if __name__ == "__main__":
    path_finder((0,0), (4,5), [(1,4),(2,3),(3,3),(3,4),(3,5),(3,3)], grid_width=10, grid_height=10)
