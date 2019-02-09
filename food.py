from mesa import Agent
import random as rd

import numpy as np

from config import CARRYING_CAPACITY, FOOD_MEAN, FOOD_STD_DEV, FOOD_INCR


class Food(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)

        self.pos = pos

        # TODO GENERATE RANDOMNESS BETWEEN 1 AND MAX_UTIL CHANGE THIS IN MODEL.PY
        self.max_util = abs(int(round(np.random.normal(FOOD_MEAN, FOOD_STD_DEV)))) + 1

        self.util = rd.randint(1, self.max_util)
        self.steps = 0

    def step(self):
        # TODO CHANGE STEPCOUNT  AND ADD THIS VARIABLE IN CONFIG
        if self.steps % FOOD_INCR == 0:
            if self.util < self.max_util:
                self.util += 1

        self.steps += 1

    def get_eaten(self):
        self.util -= CARRYING_CAPACITY

    def can_be_eaten(self):
        return self.util >= CARRYING_CAPACITY
