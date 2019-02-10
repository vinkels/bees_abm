import random as rd

from mesa import Agent

from config import CARRYING_CAPACITY


class Hive(Agent):
    def __init__(self, model, pos, color, bee_color):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.food_locations = []
        self.food = 0
        self.n_bees = 0
        self.hungry = False

        # The optimal energy level is used to balance the hive.
        self.energy_level_optimal = 0

        # bite is the bite size that bees will take from the food supply.
        self.bite = 1

        # Colors are used in the vizualisation
        self.color = color
        self.bee_color = bee_color

        # The rate at which new bees are produced
        self.reproduction_rate = 0.1

    def receive_food(self, info):
        """
        Add food to foodsupply, and save food location.
        """
        self.food_locations.append(info)
        self.food += CARRYING_CAPACITY
        self.model.load_count += 1

    def step(self):
        """
        The hive step consists of 5 steps.
        1. Determine the current number of bees in the hive.
        2. Determine the current optimal energy level.
        3. Reproduce with a certain chance.
        4. Cleanup food locations.
        5. Balance hive if necessary.
        """
        self.n_bees = self.model.schedule.count_hive_bees(self.pos)

        self.energy_level_optimal = self.n_bees * 5

        if rd.random() < self.reproduction_rate:
            self.model.add_bee(self, "babee", color=self.bee_color)
            self.n_bees += 1

        if len(self.food_locations) > 10:
            to_discard = rd.randint(1, 10)
            self.food_locations = self.food_locations[to_discard:]

        self.balance_hive()

    def get_food_stat(self):
        """
        Returns the current amount of food in the hive.
        """
        return self.food

    def balance_hive(self):
        """
        If food is available, adjust parameters of hive based on food in hive
        """
        if self.food > 0:

            # if enough food, increase consumption and reproduction
            if self.food >= self.energy_level_optimal:
                self.bite += self.bite/10
                self.reproduction_rate += self.reproduction_rate/100

            else:
                self.bite = 1
                self.reproduction_rate = 0.1
