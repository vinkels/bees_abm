import numpy
from mesa import Agent

from config import LIFESPAN, ENERGY_MEAN, ENERGY_STD_DEV
from strategy import BEE_STRATEGIES
from astar import astar


class Bee(Agent):
    def __init__(self, model, pos, hive, type_bee, hive_id, color, age=0):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.age = age
        self.type_bee = type_bee
        self.is_carrying_food = False

        # A bee knows where its hive is.
        self._hive_location = hive.pos
        self._hive_id = hive_id

        # A bee can remember a food location
        self.food_location = None

        # Color is used for vizualisation.
        self.color = color

        # random maximum of energy level required per bee to go foraging
        self.max_energy = numpy.random.normal(ENERGY_MEAN, ENERGY_STD_DEV)
        self.energy = self.max_energy

        # A bee can have a route planned out.
        self.planned_route = []

        # A bee remembers a map of the area, and where it has been before.
        self._internal_map = numpy.zeros((self.model.height, self.model.width))
        self._visited_squares = set()

    @property
    def is_tired(self):
        """
        Returns if the bee is tired and should stop scouting.
        """
        return self.energy < 0.5 * self.max_energy

    @property
    def at_hive(self):
        """
        Returns if the bee is currently at its hive location.
        """
        return self.pos == self._hive_location

    @property
    def hive(self):
        """
        Returns the hive object that this bee relates to.
        """
        return self.model.get_hive(self._hive_id)

    def move_to_hive(self):
        """
        Move towards the hive, and if the hive is reached arrive there.
        """
        self.move(self._hive_location)

        if self.at_hive:
            self.arrive_at_hive()

    def get_accessible_neighbourhood(self):
        """
        Determine which neighbours are accessible by looking at obstacles.
        Save all obstacles in neighbourhood in memory, and return accessible neighbours.
        """
        neighbourhood, obstacles = self.model.grid.get_accessible_neighborhood(self.pos)

        if self.pos not in self._visited_squares:
            self._visited_squares.add(self.pos)
            for obstacle in obstacles:
                self._internal_map[obstacle[0]][obstacle[1]] = 1

        return neighbourhood

    def move(self, target_location):
        """
        Make a move towards target_location.
        If the current route is no longer viable make a new plan.
        """
        neighborhood = self.get_accessible_neighbourhood()

        if not self.planned_route or not self.planned_route[0] in neighborhood:
            self.planned_route = astar(self._internal_map,
                                       self.pos,
                                       target_location)

        next_location = self.planned_route.pop(0)
        self.model.grid.move_agent(self, next_location)

    def arrive_at_hive(self):
        """
        Arrive at the hive, and become a rester to gain energy.
        If carrying any food, unload this food at the hive.
        """
        assert self.at_hive, "A bee can only arrive if at hive."

        if self.is_carrying_food:
            self.is_carrying_food = False
            self.hive.receive_food(self.food_location)

        self.type_bee = "rester"

    def step(self):
        """
        A bee step consists of 4 steps:
        1. Age the bee.
        2. Lose energy proportional to age.
        3. Remove bee if out of energy.
        4. Execute bee strategy.
        """
        self.age += 1

        age_penalty = (self.age / LIFESPAN) / 10
        self.energy -= min(age_penalty, 1)

        if self.energy <= 0:
            self.model.remove_agent(self)
        else:
            BEE_STRATEGIES[self.type_bee](self)
