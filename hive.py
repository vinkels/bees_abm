from mesa import Agent
import random as rd


class Hive(Agent):
    def __init__(self, model, pos, hive_num):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.hive_num = hive_num
        self.food_locs = []
        self.food = 0
        self.n_bees = 0
        self.hungry = False
        self.energy_level_critical = 10
        self.energy_level_optimal = 0
        self.energy_level_minimum = 25
        self.bees_hive = []
        self.bite = 1
        self.reproduction_rate = 0.1

    def receive_info(self, info):
        self.food_locs.append(info)

    def step(self):

        # determine number of bees in hive
        self.bees_hive = self.model.grid.get_neighbors(self.pos, moore=True, include_center = True, radius = 0)
        self.n_bees = len(self.bees_hive)

        # determine optimal and critical amount of food
        self.energy_level_optimal = self.n_bees * 20
        self.energy_level_critical = self.n_bees

        # chance of babies
        if rd.random() < self.reproduction_rate:
            self.model.add_bee(self.pos, self, "babee", hive_num = self.hive_num)
            self.n_bees += 1

        # forget (maybe) 10% of food locations when too many to remember
        #TODO the amount of number to forget and the randomness should be tuned
        if len(self.food_locs) > 10:
            if rd.random() < 0.5:
                self.food_locs = self.food_locs[int(len(self.food_locs)/10):len(self.food_locs)]

        # adjust parameters of hive based on food in hive
        self.balance_hive()

    def unload_food(self, food=1):
        self.food += 5

    def get_food_stat(self):
        return self.food

    def get_hive_id(self):
        return self.hive_num

    def get_food_memory(self):
        return self.food_locs

    def balance_hive(self):

        # if food is available
        if self.food > 0:

            # if more than necessary amount of food, increase consumption and reproduction
            if self.food >= self.energy_level_optimal:
                self.bite += 1
                self.reproduction_rate += 0.1

            else:
                self.bite = 1
                self.reproduction_rate = 0.1
