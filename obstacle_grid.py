import itertools

from mesa.space import MultiGrid, accept_tuple_argument

from bee import Bee
from config import OBSTACLE
from food import Food
from hive import Hive


class MultiGridWithObstacles(MultiGrid):
    def __init__(self, width, height, torus, obstacle_positions, VIZUALISATION=False):
        """ Create a new grid.

        Args:
            width, height: The width and height of the grid
            torus: Boolean whether the grid wraps or not.
            obstacle_positions: A set of all locations that are not accessible.
            VIZUALISATION: Is this grid going to be shown to a UI.
        """
        self.height = height
        self.width = width
        self.torus = torus

        self.VIZUALISATION = VIZUALISATION

        # If we are not vizualizing, we only keep food on an actual grid,
        # bees and hives are accessed in other ways.
        if self.VIZUALISATION:
            self.grids = {
                Bee: [[set() for _ in range(self.height)] for _ in range(self.width)],
                Hive: [[set() for _ in range(self.height)] for _ in range(self.width)],
                Food: [[None for _ in range(self.height)] for _ in range(self.width)]
            }
        else:
            self.grids = {
                Food: [[None for _ in range(self.height)] for _ in range(self.width)]
            }

        self.obstacle_positions = obstacle_positions

        self.agents = {}

        self.radius_1_food_cache = {}

        self.accessible_cache = {}

        # Set of moore neighbours from (0, 0)
        self.moore_neighbors = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

    def warmup(self):
        """
        Warmup the caches in the grid, so all steps will be faster and more consistent.
        """
        for i in range(self.width):
            for j in range(self.height):
                self.get_accessible_neighborhood((i, j))
                self.get_food_neighbors((i, j), 1)

    def move_agent(self, agent, pos):
        """
        Move an agent from its current position to a new position.

        Args:
            agent: Agent object to move. Assumed to have its current location
                   stored in a 'pos' tuple.
            pos: Tuple of new position to move the agent to.

        Overwritten to be less safe, but faster by not checking torus
        """
        if type(agent) == Food or self.VIZUALISATION:
            self._remove_agent(agent.pos, agent)
            self._place_agent(pos, agent)

        agent.pos = pos

    def place_agent(self, agent, pos):
        """
        Position an agent on the grid, and set its pos variable.
        """
        self._place_agent(pos, agent)

        self.agents[agent.unique_id] = agent

        agent.pos = pos

    def remove_agent(self, agent):
        """
        Remove the agent from the grid and set its pos variable to None.
        """
        pos = agent.pos

        del self.agents[agent.unique_id]

        self._remove_agent(pos, agent)
        agent.pos = None

    def _place_agent(self, pos, agent):
        """
        Place the agent at the correct location.
        No empties, because they cost performance.
        """
        agent_type = type(agent)

        # Only food gets tracked if there is no vizualisation
        if agent_type == Food:
            x, y = pos
            self.grids[agent_type][x][y] = agent.unique_id
        elif self.VIZUALISATION:
            x, y = pos
            self.grids[agent_type][x][y].add(agent.unique_id)

    def _remove_agent(self, pos, agent):
        """
        Remove the agent from the given location.
        No empties, because they cost performance.
        """
        agent_type = type(agent)

        if agent_type == Food:
            x, y = pos
            self.grids[agent_type][x][y] = None
        elif self.VIZUALISATION:
            x, y = pos
            self.grids[agent_type][x][y].remove(agent.unique_id)

    def get_contents_with_obstacles_helper(self, x, y):
        """
        A helper function that add an OBSTACLE to the contents if there is one at that location.
        """
        if (x, y) in self.obstacle_positions:
            return [OBSTACLE]
        else:
            assert self.VIZUALISATION
            hive_bee_ids = itertools.chain.from_iterable([self.grids[breed][x][y] for breed in [Bee, Hive]])
            foods = [self.agents[self.grids[Food][x][y]]] if self.grids[Food][x][y] else []
            return [self.agents[z] for z in hive_bee_ids] + foods

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

    def get_accessible_neighborhood(self, pos):
        """
        Returns a list of accessible positions
        in a 1 radius Moore neighbourhood, excluding the center.
        It also returns a list of obstacles in the same neighbourhood.
        """
        if pos in self.accessible_cache:
            return self.accessible_cache[pos]

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

        self.accessible_cache[pos] = accessible, obstacles

        return accessible, obstacles

    def get_food_neighbors(self, pos, radius=1):
        """ Return a list of neighbors to a certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            At most 1 if radius==0, and 8 if radius==1.
        """
        if radius == 0:
            x, y = pos
            food_candidate = self.grids[Food][x][y]
            return [self.agents[food_candidate]] if food_candidate else []
        else:

            # Food never changes, so we cache it.
            if pos in self.radius_1_food_cache:
                return self.radius_1_food_cache[pos]

            x, y = pos

            cell_list = []
            for a, b in self.moore_neighbors:
                cand = (x+a, y+b)
                if 0 <= cand[0] < self.width and 0 <= cand[1] < self.height and cand not in self.obstacle_positions:
                    cell_list.append(cand)

            foods = [
                self.agents[z]
                for z in (
                    self.grids[Food][x][y]
                    for x, y in cell_list
                    if self.grids[Food][x][y]
                )
            ]

            self.radius_1_food_cache[pos] = foods
            return foods
