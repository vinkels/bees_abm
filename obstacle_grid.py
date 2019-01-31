from mesa.space import MultiGrid, accept_tuple_argument

import itertools


from config import OBSTACLE

import time

from hive import Hive
from bee import Bee
from food import Food


class MultiGridWithObstacles(MultiGrid):
    def __init__(self, width, height, torus, obstacle_positions):
        """ Create a new grid.

        Args:
            width, height: The width and height of the grid
            torus: Boolean whether the grid wraps or not.
            obstacle_positions: A set of all locations that are not accessible.
        """
        self.height = height
        self.width = width
        self.torus = torus

        self.grids = {
            Bee: [[set() for _ in range(self.height)] for _ in range(self.width)],
            Hive: [[set() for _ in range(self.height)] for _ in range(self.width)],
            Food: [[set() for _ in range(self.height)] for _ in range(self.width)]
        }

        self.obstacle_positions = obstacle_positions
        # print(self.obstacle_positions)
        self.agents = {}

        self.timings = {
            'move': 0,
            'place': 0,
            'remove': 0
        }

        self.moore_neighbors = set([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        assert len(self.moore_neighbors) == 8

    def move_agent(self, agent, pos):
        """
        Move an agent from its current position to a new position.

        Args:
            agent: Agent object to move. Assumed to have its current location
                   stored in a 'pos' tuple.
            pos: Tuple of new position to move the agent to.

        Overwritten to be less safe, but faster by not checking torus
        """
        start = time.time()

        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)
        agent.pos = pos

        end = time.time()
        self.timings['move'] += end - start

    def place_agent(self, agent, pos):
        """ Position an agent on the grid, and set its pos variable. """
        start = time.time()
        self._place_agent(pos, agent)

        self.agents[agent.unique_id] = agent

        agent.pos = pos
        
        end = time.time()
        self.timings['place'] += end - start

    def remove_agent(self, agent):
        """ Remove the agent from the grid and set its pos variable to None. """
        start = time.time()
        pos = agent.pos

        del self.agents[agent.unique_id]

        self._remove_agent(pos, agent)
        agent.pos = None

        end = time.time()
        self.timings['remove'] += end - start

    def _place_agent(self, pos, agent):
        """ 
        Place the agent at the correct location.
        No empties, because they cost performance.
        """
        x, y = pos
        self.grids[type(agent)][x][y].add(agent.unique_id)

    def _remove_agent(self, pos, agent):
        """ 
        Remove the agent from the given location. 
        No empties, because they cost performance.
        """
        x, y = pos
        self.grids[type(agent)][x][y].remove(agent.unique_id)

    def get_contents_with_obstacles_helper(self, x, y):
        """
        A helper function that add an OBSTACLE to the contents if there is one at that location.
        """
        if (x, y) in self.obstacle_positions:
            return [OBSTACLE]
        else:
            agent_ids = itertools.chain.from_iterable([self.grids[breed][x][y] for breed in [Bee, Food, Hive]])
            return [self.agents[z] for z in agent_ids]

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
            for x, y in cell_list
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
        x, y = pos

        accessible = []
        obstacles = []

        # Moore's neighbourhood
        for a, b in self.moore_neighbors:
            cand = (x+a, y+b)

            # Don't go out of bounds here.
            if 0 <= cand[0] < self.width and 0 <= cand[1] < self.height:
                if cand not in self.obstacle_positions:
                    accessible.append(cand)
                else:
                    obstacles.append(cand)

        return accessible, obstacles

    def get_neighbors_by_breed(self, breed, pos, moore, include_center=False, radius=1):
        """ Return a list of neighbors to a certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).

        """
        if radius == 1:
            x, y = pos

            cell_list = [] 
            for a, b in self.moore_neighbors:
                cand = (x+a, y+b)
                if 0 <= cand[0] < self.width and 0 <= cand[1] < self.height and cand not in self.obstacle_positions:
                    cell_list.append(cand)
        else:
            cell_list = [pos]

        return  (
            self.agents[z] 
            for z in itertools.chain.from_iterable(
                self.grids[breed][x][y]
                for x, y in cell_list
            )
        )
        
