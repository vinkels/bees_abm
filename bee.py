import numpy
from mesa import Agent

from config import LIFESPAN, ENERGY_MEAN, ENERGY_STD_DEV
from strategy import BEE_STRATEGIES
from astar import astar


class Bee(Agent):
    def __init__(self, model, pos, hive, type_bee, hive_id, color, age=0):
        super().__init__(model.next_id(), model)

        self.loaded = False
        self.food_location = None
        self.hive_location = hive.pos
        self.hive_id = hive_id
        self.pos = pos
        self.type_bee = type_bee
        self.age = age
        self.color = color

        # random threshold of energy required per bee to go foraging
        self.max_energy = numpy.random.normal(ENERGY_MEAN, ENERGY_STD_DEV)
        self.energy = self.max_energy

        self.planned_route = []

        self._internal_map = numpy.zeros((self.model.height, self.model.width))

        self._visited_squares = set()

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

    def move(self, loc):
        neighborhood = self.get_accessible_neighbourhood()

        if not self.planned_route or not self.planned_route[0] in neighborhood:
            self.planned_route = astar(self._internal_map, self.pos, loc)

        nxt_loc = self.planned_route.pop(0)
        self.model.grid.move_agent(self, nxt_loc)

    def arrive_at_hive(self, hive):
        """
        Arrive at the hive, and become a rester to gain energy.
        If carrying any food, unload this food at the hive.
        """
        if self.loaded:
            self.loaded = False
            hive.receive_food(self.food_location)

        self.type_bee = "rester"

    def relax_at_hive(self, hive):
        """
        Eat while at hive and gain energy.
        If there is no food left, become a scout if old enough.
        """
        if hive.food < hive.bite:
            if self.type_bee != "babee":
                self.type_bee = "scout"
        elif self.type_bee == "babee":
            self.energy += 0.5
            hive.food -= 0.5
        else:
            self.energy += hive.bite
            hive.food -= hive.bite

    def step(self):
        self.age += 1

        # lose energy proportional to age
        age_penalty = (self.age / LIFESPAN) / 10
        self.energy -= min(age_penalty, 1)

        # if out of energy, die
        if self.energy <= 0:
            self.model.remove_agent(self)
            return

        BEE_STRATEGIES[self.type_bee](self)
