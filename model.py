from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random as rd

from food import Bee, Food
from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # Init bees
        bee = Bee(unique_id=self.next_id(), model=self)
        self.grid.place_agent(bee, (0, 0))
        self.schedule.add(bee)

        food = Food(id = self.next_id(), model = self, pos = (3,3), util = 5)
        self.grid.place_agent(food, (3, 3))

        self.datacollector = DataCollector({"Bees": lambda m: m.schedule.get_breed_count(Bee)})
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
