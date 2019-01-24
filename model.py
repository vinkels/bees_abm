from mesa import Model
from mesa import Agent
from mesa.datacollection import DataCollector

import random as rd

from config import *
from food import Food
from bee import Bee
from hive import Hive
from obstacle_grid import MultiGridWithObstacles

from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    #TODO MODIFY HEIGHT AND WIDTH FROM CONFIG
    def __init__(self, width, height, obstacle_density, food_density):
        super().__init__()
        self.height = height
        self.width = width

        self.user_error = None
        if obstacle_density + food_density > FOOD_OBSTACLE_RATIO:
            raise Exception("Food and obstacles do not fit in the grid.")

        hive_locations, food_locations, self.obstacle_locations = self.init_grid(height, width, obstacle_density, food_density)

        self.grid = MultiGridWithObstacles(self.width, self.height, torus=False, obstacle_positions=set(self.obstacle_locations))

        self.schedule = RandomActivationBeeWorld(self)

        self.hives = {}

        for hive_location in hive_locations:

            # Init Hive
            #TODO INITIALISE AMOUNT OF HIVES 
            hive = Hive(self, hive_location)
            self.hive = hive
            self.add_agent(self.hive, hive_location)
            self.hives[hive.unique_id] = hive

            # Init Bees
            #TODO TAG BEES FOR WARM-UP PERIOD
            #TODO DEFINE THE AMOUNT OF STARTING BEES BABIES AS WELL
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

        #TODO ADD MORE ROBUST RANDOMNESS TO FOOD UTILITY
        for f_loc in food_locations:
            food = Food(self, f_loc)
            self.add_agent(food, f_loc)

        self.datacollector = DataCollector({
            "Bees": lambda m: m.schedule.get_breed_count(Bee),
            "HiveFood": lambda m: m.hive.get_food_stat()/10,
            "Scout bees": lambda m: m.schedule.get_bee_count("scout"),
            "Foraging bees": lambda m: m.schedule.get_bee_count("foraging"),
            "Rester bees": lambda m: m.schedule.get_bee_count("rester"),
            "Baby bees": lambda m: m.schedule.get_bee_count("babee")
        })
        self.datacollector2 = DataCollector({
            "HiveID": lambda m: m.hive.get_hive_id(),
            "FoodLocs": lambda m: m.hive.get_food_memory(),
        })
        self.running = True

    def get_hive(self, hive_id):
        return self.hives[hive_id]

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

        food_end_index = amount_food + 1
        obstacle_end_index = food_end_index + amount_obstacle
        
        hive_locations = [possible_locations[0]]
        food_locations = possible_locations[1:food_end_index]
        obstacle_locations = set(possible_locations[food_end_index:obstacle_end_index])

        return hive_locations, food_locations, obstacle_locations
