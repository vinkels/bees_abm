from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random as rd

from food import Bee, Food, Hive
from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # Init Hive
        self.hive = Hive(self, (0,0))
        self.add_agent(self.hive, (0, 0))

        # Init Bees
        bee = Bee(self, self.hive.pos, self.hive, "scout")
        self.add_agent(bee, self.hive.pos)

        bee_for = Bee(self, self.hive.pos, self.hive, "foraging")
        self.add_agent(bee_for, self.hive.pos)

        # Init Food
        food = Food(self, (3,3), 5)
        self.add_agent(food, (3, 3))

        self.datacollector = DataCollector({
            "Bees": lambda m: m.schedule.get_breed_count(Bee), 
            "HiveFood": lambda m: m.hive.get_food_stat()
        })
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def add_agent(self, agent, pos):
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

    def remove_agent(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)