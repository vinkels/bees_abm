from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random as rd

from food import Bee, Food, Hive, Obstacle
from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # Init Hive
        hive = Hive(self, (0,0))
        self.hive = hive
        self.add_agent(self.hive, (0, 0))

        # Init Bees
        for i in range(0, 4):
            bee = Bee(self, hive.pos, hive, "scout")
            self.add_agent(bee, hive.pos)

            # bee_for = Bee(unique_id=self.next_id(), model=self, type_bee = "rester")
            bee_for = Bee(self, hive.pos, hive, "rester")
            self.grid.place_agent(bee_for, (0, 0))
            self.schedule.add(bee_for)
            self.add_agent(bee_for, hive.pos)

            # Init Food
        for i in range(0, 10):
            loc1 = rd.randint(0, width - 1)
            loc2 = rd.randint(0, height - 1)
            food = Food(self, (loc1,loc2), rd.randint(1, 4))
            self.add_agent(food, (loc1, loc2))

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