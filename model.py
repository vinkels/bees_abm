from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random as rd

from food import Food
from bee import Bee
from hive import Hive
from obstacle import Obstacle

from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # # Wall
        # for obs_position in [(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)]:
        #     obstacle = Obstacle(unique_id=self.next_id(), model=self, pos=obs_position)
        #     self.grid.place_agent(obstacle, obs_position)

        hive_locations, food_locations, obstacle_locations = self.init_grid(height, width)

        for hive_number in range(0, len(hive_locations)):

            hive_location = hive_locations[hive_number]

            # Init Hive
            hive = Hive(self, hive_location, hive_number)
            self.hive = hive
            self.add_agent(self.hive, hive_location)

            # Init Bees
            for i in range(0, 20):
                bee = Bee(self, self.hive.pos, self.hive, "scout", hive_num = hive_number)
                self.add_agent(bee, self.hive.pos)

                bee_for = Bee(self, self.hive.pos, self.hive, "rester", hive_num = hive_number)
                self.add_agent(bee_for, self.hive.pos)

            # init babies
            for i in range(0, 3):
                bee_baby = Bee(self, self.hive.pos, self.hive, "babee", hive_num = hive_number)
                self.add_agent(bee_baby, self.hive.pos)

        for f_loc in food_locations:
            food = Food(self, f_loc, rd.randint(1, 4))
            self.add_agent(food, f_loc)

        for o_loc in obstacle_locations:
            obstacle = Obstacle(unique_id=self.next_id(), model=self, pos=o_loc)
            self.grid.place_agent(obstacle, o_loc)

        self.datacollector = DataCollector({
            "Bees": lambda m: m.schedule.get_breed_count(Bee),
            "HiveFood": lambda m: m.hive.get_food_stat()/10,
            "Scout bees": lambda m: m.schedule.get_scout_count()[0],
            "Foraging bees": lambda m: m.schedule.get_scout_count()[1],
            "Rester bees": lambda m: m.schedule.get_scout_count()[2],
            "Baby bees": lambda m: m.schedule.get_scout_count()[3]
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

    def add_bee(self, pos, hive, type_bee, hive_num):
            bee = Bee(self, pos, hive, type_bee, hive_num)
            self.add_agent(bee, pos)

    def init_grid(self, height, width):
        possible_locations = [
            (x, y)
            for y in range(height)
            for x in range(width)
        ]
        amount_of_possible_locations = len(possible_locations)

        ten_percent = int(amount_of_possible_locations / 20)

        rd.shuffle(possible_locations)

        hive_location = possible_locations[0:1]
        food_locations = possible_locations[1:(ten_percent+1)]
        obstacle_locations = possible_locations[(ten_percent+1):((ten_percent*4)+1)]
        
        return hive_location, food_locations, obstacle_locations