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

from util import path_finder

import time

class BeeForagingModel(Model):
    #TODO MODIFY HEIGHT AND WIDTH FROM CONFIG
    def __init__(self, width, height, obstacle_density, food_density,nr_hives=2, car_cap=5):
        super().__init__()
        self.height = height
        self.width = width
        self.car_cap = car_cap
        self.nr_hives = nr_hives
        self.death_count  = 0
        self.birth_count = 0
        self.death_age = []


        self.user_error = None
        if obstacle_density + food_density > FOOD_OBSTACLE_RATIO:
            raise Exception("Food and obstacles do not fit in the grid.")

        hive_locations, food_locations, self.obstacle_locations = self.init_grid(height, width, obstacle_density, food_density, self.nr_hives)
        self.grid = MultiGridWithObstacles(self.width, self.height, torus=False, obstacle_positions=set(self.obstacle_locations))
        self.schedule = RandomActivationBeeWorld(self)

        self.hives = {}

        for hive_location in hive_locations:

            # Init Hives
            r = lambda: rd.randint(0,255)
            color = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())
            hive = Hive(self, hive_location, color=color, bee_color=color)
            self.hive = hive
            self.hives[hive.unique_id] = hive
            self.add_agent(hive, hive_location)
            
            # Init Bees
            #TODO TAG BEES FOR WARM-UP PERIOD
            #TODO DEFINE THE AMOUNT OF STARTING BEES BABIES AS WELL
            hive_id = hive.unique_id
            for _ in range(0, 20):
                self.add_bee( pos=hive_location, hive=hive, type_bee="scout", hive_id=hive_id, color=hive.bee_color, age=BABYTIME)
                
                self.add_bee(pos=hive_location, hive=hive, type_bee="rester", hive_id=hive_id,color=hive.bee_color,  age=BABYTIME)
            
            # # init babies
            # for i in range(0, 3):
            #     bee_baby = Bee(self, hive_location, self.hive, "babee", hive_id=hive_id)
            #     self.add_agent(bee_baby, hive_location)

        #TODO ADD MORE ROBUST RANDOMNESS TO FOOD UTILITY
        #DONE?
        for f_loc in food_locations:
            food = Food(self, f_loc)
            self.add_agent(food, f_loc)

        # self.datacollector = DataCollector({
        #     "Bees": lambda m: m.schedule.get_breed_count(Bee),
        #     "HiveFood": lambda m: sum([hive.get_food_stat() for hive in m.hives.values()]),
        #     "Scout bees": lambda m: m.schedule.get_bee_count("scout"),
        #     "Foraging bees": lambda m: m.schedule.get_bee_count("foraging"),
        #     "Rester bees": lambda m: m.schedule.get_bee_count("rester"),
        #     "Baby bees": lambda m: m.schedule.get_bee_count("babee")
        # })
        # self.datacollector2 = DataCollector({
        #     "HiveID": lambda m: m.hives[self.hive.unique_id].get_hive_id(),
        #     "FoodLocs": lambda m: m.hives[self.hive.unique_id].get_food_memory(),
        # })
        # self.running = False

        self.total_schedule_time = 0

        self.time_by_strategy = {
            "scout": 0,
            "foraging": 0,
            "rester": 0,
            "babee": 0
        }

        self.planning_time = 0

    def get_hive(self, hive_id):
        return self.hives[hive_id]

    def step(self):

        schedule_start = time.time()

        self.schedule.step()

        schedule_end = time.time()
        self.total_schedule_time += schedule_end - schedule_start

        # self.death_count = 0
        # self.birth_count = 0
        # self.death_age = []
        print(self.schedule.step())


        # self.datacollector.collect(self)
        # self.datacollector2.collect(self)


    def get_birth_count(self):
        count = self.birth_count
        self.birth_count = 0
        return count

    def get_death_count(self):
        count = self.death_count
        self.death_count = 0
        return count

    def get_death_age(self):
        if len(self.death_age) > 0:
            mean_age = sum(self.death_age)/len(self.death_age)
            self.death_age = []
            return mean_age
        else:
            return 0

    def run_model(self, n_steps):
        for i in range(n_steps):
            self.step()        

    def add_agent(self, agent, pos):
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent)

    def remove_agent(self, agent):
        if type(agent) == Bee:
            self.death_count += 1
            self.death_age.append(agent.age)

        self.grid.remove_agent(agent)
        self.schedule.remove(agent)

    def add_bee(self, pos, hive, type_bee, hive_id, color, age=0):
            bee = Bee(self, pos=pos, hive=hive, type_bee=type_bee, hive_id=hive_id, color=color,age=age)
            if type_bee == 'babee':
                self.birth_count += 1
            self.grid.place_agent(bee, pos)
            self.schedule.add(bee)

    def init_grid(self, height, width, obstacle_density, food_density,nr_hives):
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
        

        hive_locations = possible_locations[0:nr_hives]
        
        food_locations = possible_locations[nr_hives:food_end_index]
        obstacle_locations = set(possible_locations[food_end_index:obstacle_end_index])

        return hive_locations, food_locations, obstacle_locations
