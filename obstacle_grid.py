from mesa.space import MultiGrid, accept_tuple_argument

import itertools


from config import OBSTACLE

class MultiGridWithObstacles(MultiGrid):
    def __init__(self, width, height, torus, obstacle_positions):
        """ Create a new grid.

        Args:
            width, height: The width and height of the grid
            torus: Boolean whether the grid wraps or not.
            obstacle_positions: A set of all locations that are not accessible.
        """
        super().__init__(width, height, torus)
        self.obstacle_positions = obstacle_positions
        # print(self.obstacle_positions)

    def get_contents_with_obstacles_helper(self, x, y):
        """
        A helper function that add an OBSTACLE to the contents if there is one at that location.
        """
        position_set = self[x][y]

        if (x, y) in self.obstacle_positions:
            obstacle_set = {OBSTACLE}
            obstacle_set.update(position_set)
            return obstacle_set
        else:
            return position_set

    @accept_tuple_argument
    def iter_cell_list_contents(self, cell_list):
        """
        Args:
            cell_list: Array-like of (x, y) tuples, or single tuple.

        Returns:
            A iterator of the contents of the cells identified in cell_list

        """
        return itertools.chain.from_iterable(
            self.get_contents_with_obstacles_helper(x, y) 
            for x, y in cell_list if not self.is_cell_empty((x, y))
        )

    def is_cell_empty(self, pos):
        """
        Returns a bool of the contents of a cell.
        """
        x, y = pos
        return pos not in self.obstacle_positions and self.grid[x][y] == self.default_val()

    def get_accessible_neighborhood(self, pos, moore, include_center=False, radius=1):
        """
        Returns only the accessible spots in the neighbourhood.
        """
        neighborhood = set(self.get_neighborhood(pos, moore, include_center, radius))
        return neighborhood - self.obstacle_positions, neighborhood & self.obstacle_positions