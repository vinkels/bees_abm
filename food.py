from random import randint

from mesa import Agent
from numpy.random import normal

from config import CARRYING_CAPACITY, FOOD_INCR, FOOD_MEAN, FOOD_STD_DEV


class Food(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.steps = 0

        # Max util is a random value from a normal distribution
        # WARNING: max_util can be lower than CARRYING_CAPACITY,
        #          making the food unharvestable.
        self.max_util = abs(int(round(normal(FOOD_MEAN, FOOD_STD_DEV)))) + 1
        self.util = randint(1, self.max_util)

    def step(self):
        """
        If util is less than max_util increase util.
        Only increase util once every FOOD_INCR steps.
        """
        if self.util < self.max_util and self.steps % FOOD_INCR == 0:
            self.util += 1

        self.steps += 1

    def harvest(self):
        """
        Every bee can gather CARRYING_CAPACITY of food.
        """
        self.util -= CARRYING_CAPACITY

    @property
    def can_be_harvested(self):
        """
        Only food that can yield at least CARRYING_CAPACITY food can be eaten.
        """
        return self.util >= CARRYING_CAPACITY
