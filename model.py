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
        hive = Hive(unique_id=self.next_id(), model=self, pos=(0,0))
        self.grid.place_agent(hive, (0, 0))
        self.schedule.add(hive)

        # Init bees
        bee = Bee(unique_id=self.next_id(), model=self, type_bee = "scout")
        self.grid.place_agent(bee, (0, 0))
        self.schedule.add(bee)

        #Init obstacle
        obs_position = (rd.randrange(self.width),rd.randrange(self.height))
        obstacle = Obstacle(unique_id=self.next_id(), model=self, pos=obs_position)
        self.grid.place_agent(obstacle, obs_position)

        bee_for = Bee(unique_id=self.next_id(), model=self, type_bee = "foraging")
        self.grid.place_agent(bee_for, (0, 0))
        self.schedule.add(bee_for)

        food = Food(id = self.next_id(), model = self, pos = (3,3), util = 5)
        self.grid.place_agent(food, (3, 3))

        self.datacollector = DataCollector({"Bees": lambda m: m.schedule.get_breed_count(Bee)})
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
