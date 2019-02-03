from mesa import Agent
import random

from config import BABYTIME, LIFESPAN

from food import Food
import util

# TODO remove
import time

import numpy as np


class BeeStrategy:
    """
    Base Class to create a bee strategy
    """

    def __init__(self, bee):
        self.bee = bee

    def step(self):
        raise NotImplementedError

class Babee(BeeStrategy):
    '''
    This type of bee stays at the hive until a certain age
    '''

    def step(self):
        bee = self.bee

        hive = bee.model.get_hive(bee.hive_id)

        # gain strength until old enough
        bee.relax_at_hive(hive)

        # age is arbitrary
        # print("Bee age: ", bee.age, "BABYTIME: ", BABYTIME)
        if bee.age > BABYTIME:
            # raise Exception("Binnen")
            bee.type_bee = "rester"


class Rester(BeeStrategy):
    '''
    This type of bee stays at the hive, until a location for food is known and then he becomes a foraging bee
    '''

    def step(self):
        bee = self.bee

        # Resting bees can only be at the hive.
        assert bee.pos == bee.hive_loc

        hive = bee.model.get_hive(bee.hive_id)

        # check if bee has enough energy for foraging
        if bee.energy >= bee.max_energy:

            # check if food locations are known
            if hive.food_locs:

                # become forager at random food location
                bee.type_bee = "foraging"
                bee.food_loc = random.choice(hive.food_locs)

            # otherwise, stay at hive and gain energy
            else:
                # become scout if no food has been found
                bee.type_bee = "scout"

        else:
            bee.relax_at_hive(hive)


class Scout(BeeStrategy):
    '''
    This type of bee does a random walk, searching for food, and return to hive if he has found this.
    '''

    def step(self):
        """
        No food found yet, do random walk
        """
        bee = self.bee

        if bee.loaded is False:
            if bee.energy < 0.5 * bee.max_energy and bee.pos != bee.hive_loc:
                s = time.time()
                bee.move(bee.hive_loc)

                # check if destination is reached
                if bee.pos == bee.hive_loc:
                    hive = bee.model.get_hive(bee.hive_id)
                    assert hive
                    bee.arrive_at_hive(hive)
                e = time.time()
                bee.model.timings_scout['move home'] += e - s
            else:
                s = time.time()
                food_neighbours = [
                    nb
                    for nb in bee.model.grid.get_neighbors_by_breed(Food, bee.pos, moore=True, include_center=False, radius=1)
                    if nb.can_be_eaten()
                ]
                e = time.time()
                bee.model.timings_scout['look for food'] += e - s

                # If you see food that is uneaten, move there.
                if food_neighbours:
                    s = time.time()

                    food = random.choice(food_neighbours)

                    bee.model.grid.move_agent(bee, food.pos)
                    food.get_eaten()

                    # Become a forager take food and remember location
                    bee.type_bee = 'foraging'
                    bee.loaded = True
                    bee.food_loc = bee.pos

                    e = time.time()
                    bee.model.timings_scout['move to food neighbour'] += e - s

                # otherwise, move randomly
                else:
                    self.random_move()

        else:
            raise Exception("Scouts should be unloaded.")

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        bee = self.bee

        # get neighboorhood
        s = time.time()
        neighbourhood = bee.get_accessible_neighbourhood()
        e = time.time()
        bee.model.timings_scout['random_neighbourhood'] += e - s

        # select random cell in neighbourhood
        s = time.time()
        target = random.choice(neighbourhood)
        e = time.time()
        bee.model.timings_scout['random_target'] += e - s

        # move to cell
        s = time.time()
        bee.model.grid.move_agent(bee, target)
        e = time.time()
        bee.model.timings_scout['random_move'] += e - s


class Foraging(BeeStrategy):
    '''
    This type of bee goes to a given food location, takes the food and return to the hive
    '''

    def step(self):
        bee = self.bee

        # if not yet arrived at food location
        if bee.loaded is False:
            bee.move(bee.food_loc)

            # check if arrived, then take food
            if bee.food_loc == bee.pos:
                food_neighbors = [
                    nb
                    for nb in bee.model.grid.get_neighbors_by_breed(Food, bee.pos, moore=True, include_center=True, radius=0)
                    if nb.can_be_eaten()
                ]

                bee.plan_course = []
                if food_neighbors:
                    food = food_neighbors[0]
                    food.get_eaten()
                    bee.loaded = True

                # if there was no food at the promised location become a scout
                else:
                    bee.type_bee = "scout"

        # if loaded, return to hive
        else:
            bee.move(bee.hive_loc)

            # check if destination is reached
            if bee.pos == bee.hive_loc:
                hive = bee.model.get_hive(bee.hive_id)
                assert hive
                bee.arrive_at_hive(hive)


bee_strategies = {
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
        self.car_cap = self.model.car_cap
        self.color = color

        # random threshold of energy required per bee to go foraging

        self.max_energy = np.random.normal(energy_pars[0], energy_pars[1])
        self.energy = self.max_energy

        self.plan_course = []

        # self.mental_map = Grid(height=self.model.height, width=self.model.width)
        self.mental_map = np.zeros((self.model.height, self.model.width))

    def get_accessible_neighbourhood(self):
        '''
        Determine with cells in neighbourhood are not with obstacles
        '''

        neighbourhood, obstacles = self.model.grid.get_accessible_neighborhood(self.pos, moore=True)

        for obstacle in obstacles:
            # self.mental_map.node(obstacle[0], obstacle[1]).walkable = False
            # self.mental_map.node(obstacle[0], obstacle[1]).weight = 0
            self.mental_map[obstacle[0]][obstacle[1]] = 1

        return neighbourhood

    def move(self, loc):
        '''
        Move to specified location.
        '''
        neighborhood = self.get_accessible_neighbourhood()

        if not self.plan_course or not self.plan_course[0] in neighborhood:
            plan_start = time.time()
            self.plan_course = util.path_finder(cur_loc=self.pos,
                                            target_loc=loc,
                                            grid=self.mental_map,
                                            grid_width=self.model.width,
                                            grid_height=self.model.height)
            plan_end = time.time()
            self.model.planning_time += plan_end - plan_start

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
        strat_start = time.time()
        strategy = bee_strategies[self.type_bee]
        strategy(self).step()
        strat_end = time.time()
        self.model.time_by_strategy[bee_type] += strat_end - strat_start
