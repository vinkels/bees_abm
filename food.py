from mesa import Agent


class Food(Agent):
    def __init__(self, model, pos, util):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.util = util

    def step(self):
        self.util += 1

    def get_eaten(self):
        self.util -= 1
