from mesa import Agent
import random

from config import BABYTIME, LIFESPAN

from food import Food
import util

# TODO remove
import time

import numpy as np

from strategy.babee import Babee
from strategy.rester import Rester
from strategy.foraging import Foraging
from strategy.scout import Scout


BEE_STRATEGIES = {
    'babee': Babee,
    'rester': Rester,
    'foraging': Foraging,
    'scout': Scout
}


class Bee(Agent):
    def __init__(self, model, pos, hive, type_bee, hive_id,color,age=0, energy_pars=(20, 5)):
        super().__init__(model.next_id(), model)

        self.loaded = False
        self.food_loc = []
        self.hive_loc = hive.pos
        self.hive_id = hive_id
        self.pos = pos
        self.type_bee = type_bee
        self.age = age
        self.color = color

        # random threshold of energy required per bee to go foraging

        self.max_energy = np.random.normal(energy_pars[0], energy_pars[1])
        self.energy = self.max_energy

        self.plan_course = []

        # self.mental_map = Grid(height=self.model.height, width=self.model.width)
        self.mental_map = np.zeros((self.model.height, self.model.width))

        self.neighbourhood_memory = set()

    def get_accessible_neighbourhood(self):
        '''
        Determine with cells in neighbourhood are not with obstacles
        '''
        neighbourhood, obstacles = self.model.grid.get_accessible_neighborhood(self.pos, moore=True)

        # If a bee enters a space for the first time, it needs to save obstacles on that position.
        if self.pos not in self.neighbourhood_memory:
            for obstacle in obstacles:
                self.mental_map[obstacle[0]][obstacle[1]] = 1

            self.neighbourhood_memory.add(self.pos)

        return neighbourhood

    def move(self, loc):
        '''
        Move to specified location.
        '''
        neighborhood = self.get_accessible_neighbourhood()

        if not self.plan_course or not self.plan_course[0] in neighborhood:
            self.plan_course = util.path_finder(cur_loc=self.pos,
                                            target_loc=loc,
                                            grid=self.mental_map,
                                            grid_width=self.model.width,
                                            grid_height=self.model.height)

        nxt_loc = self.plan_course.pop(0)
        self.model.grid.move_agent(self, nxt_loc)

    def arrive_at_hive(self, hive):
        '''
        A scouting bee arrives back at the hive
        '''

        # unload food
        if self.loaded:
            self.loaded = False
            hive.receive_info(self.food_loc)
            hive.unload_food()
            hive.bring_back_the_foooddzzz += 1

        # become rester to gain energy
        self.type_bee = "rester"

    def relax_at_hive(self, hive):
        '''
        Eat while at hive and gain energy
        '''

        # if hive.food > hive.energy_level_critical:
        if hive.food > hive.bite:
            if self.type_bee == "babee":
                self.energy += 0.5
                hive.food -= 0.5
            else:
                self.energy += hive.bite
                hive.food -= hive.bite



        # if no food is available, go search
        # TODO ENERGY DECAY OVER TIME

        # BABEES are not allowed to change to scouters, only by age
        elif self.type_bee != "babee":
            self.type_bee = "scout"


    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''
        # TODO TYPE OF ENERGY DECAY FOR BEE AND AGE SPAN
        self.age += 1

        # lose energy proportional to age
        # TODO This should probably be a larger age_penalty
        age_penalty = (self.age / LIFESPAN) / 10
        self.energy -= min(age_penalty, 1)
        # if no more energy, die
        if self.energy <= 0:
            self.model.remove_agent(self)
            return

        bee_type = self.type_bee
        strategy = BEE_STRATEGIES[self.type_bee]
        strategy(self).step()
