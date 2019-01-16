from mesa import Agent
import random as rd


class Hive(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.food_locs = []

        self.food = 0

    def receive_info(self, info):
        if info not in self.food_locs:
            self.food_locs.append(info)

    def step(self):

        # Make random new bees
        # TODO make this actually depend on queen, drones and food resources.
        print(self.food_locs)

        if rd.random() > 0.90:
            self.model.add_bee(self.pos, self, "rester")

    def unload_food(self, food=1):
        self.food += 1

    def get_food_stat(self):
        return self.food
