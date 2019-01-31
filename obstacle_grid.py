from mesa.space import MultiGrid, accept_tuple_argument

import itertools


from config import OBSTACLE

import time

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
        self.agents = {}

        self.timings = {
            'move': 0,
            'place': 0,
            'remove': 0
        }

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
        self.grid[x][y].add(agent.unique_id)

    def _remove_agent(self, pos, agent):
        """ 
        Remove the agent from the given location. 
        No empties, because they cost performance.
        """
        x, y = pos
        self.grid[x][y].remove(agent.unique_id)

    def get_contents_with_obstacles_helper(self, x, y):
        """
        A helper function that add an OBSTACLE to the contents if there is one at that location.
        """
        if (x, y) in self.obstacle_positions:
            return [OBSTACLE]
        else:
            return [self.agents[z] for z in self[x][y]]

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
        x, y = pos

        accessible = []
        obstacles = []

        # Moore's neighbourhood
        for a in [1, 0, -1]:
            for b in [1, 0, -1]:

                # Don't check you own position
                if a != 0 or b != 0:
                    cand = (x+a, y+b)

                    # Don't go out of bounds here.
                    if 0 <= cand[0] < self.width and 0 <= cand[1] < self.height:
                        if cand not in self.obstacle_positions:
                            accessible.append(cand)
                        else:
                            obstacles.append(cand)

        return accessible, obstacles
