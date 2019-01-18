from mesa import Agent
import random as rd


class Food(Agent):
    def __init__(self, model, pos, util):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.max_util = rd.randint(1, 10)
        self.util = util
        self.steps = 0

    def step(self):
        if self.steps % 3 == 0:
            if self.util < self.max_util:
                self.util += 1

        self.steps += 1


    def get_eaten(self):
        self.util -= 1
