from mesa import Model
from mesa import Agent
from mesa.datacollection import DataCollector

import random as rd

from food import Food
from bee import Bee
from hive import Hive
from obstacle import Obstacle
from obstacle_grid import MultiGridWithObstacles

from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height, obstacle_density, food_density):
        super().__init__()
        self.height = height
        self.width = width

        self.grid = MultiGridWithObstacles(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # # Wall
        # for obs_position in [(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)]:
        #     obstacle = Obstacle(unique_id=self.next_id(), model=self, pos=obs_position)
        #     self.grid.place_agent(obstacle, obs_position)

        if obstacle_density + food_density > 99:
            raise Exception("Food and obstacles do not fit in the grid.")

        hive_locations, food_locations, self.obstacle_locations = self.init_grid(height, width, obstacle_density, food_density)

        for hive_location in hive_locations:

            # Init Hive
            hive = Hive(self, hive_location)
            self.hive = hive
            self.add_agent(self.hive, hive_location)

            # Init Bees
            hive_id = hive.unique_id
            for i in range(0, 20):
                bee = Bee(self, self.hive.pos, self.hive, "scout", hive_id=hive_id)
                self.add_agent(bee, hive_location)

                bee_for = Bee(self, hive_location, self.hive, "rester", hive_id=hive_id)
                self.add_agent(bee_for, hive_location)

            # init babies
            for i in range(0, 3):
                bee_baby = Bee(self, hive_location, self.hive, "babee", hive_id=hive_id)
                self.add_agent(bee_baby, hive_location)

        for f_loc in food_locations:
            food = Food(self, f_loc, rd.randint(1, 4))
            self.add_agent(food, f_loc)

        # for o_loc in obstacle_locations:
        #     obstacle = Obstacle(model=self, pos=o_loc)
        #     self.grid.place_agent(obstacle, o_loc)

        self.datacollector = DataCollector({
            "Bees": lambda m: m.schedule.get_breed_count(Bee),
            "HiveFood": lambda m: m.hive.get_food_stat()/10,
            "Scout bees": lambda m: m.schedule.get_scout_count()[0],
            "Foraging bees": lambda m: m.schedule.get_scout_count()[1],
            "Rester bees": lambda m: m.schedule.get_scout_count()[2],
            "Baby bees": lambda m: m.schedule.get_scout_count()[3]
        })
        self.datacollector2 = DataCollector({
            "HiveID": lambda m: m.hive.get_hive_id(),
            "FoodLocs": lambda m: m.hive.get_food_memory(),
        })
        self.running = True

    def get_hive(self, hive_id):
        return self.schedule.agents_by_breed[Hive][hive_id]

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.datacollector2.collect(self)

    def run_model(self, n_steps):
        for i in range(n_steps):
            self.step()

    def add_agent(self, agent, pos):
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

    def remove_agent(self, agent):
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)

    def add_bee(self, pos, hive, type_bee, hive_id):
            bee = Bee(self, pos, hive, type_bee, hive_id)
            self.add_agent(bee, pos)

    def init_grid(self, height, width, obstacle_density, food_density):
        possible_locations = [
            (x, y)
            for y in range(height)
            for x in range(width)
        ]
        amount_of_possible_locations = len(possible_locations)

        amount_food = int((amount_of_possible_locations / 100) * food_density)
        amount_obstacle = int((amount_of_possible_locations / 100) * obstacle_density)

        rd.shuffle(possible_locations)

        hive_locations = [possible_locations[0]]
        food_locations = possible_locations[1:(amount_food+1)]
        obstacle_locations = set(possible_locations[(amount_food+1):((amount_obstacle)+1)])

        return hive_locations, food_locations, obstacle_locations
