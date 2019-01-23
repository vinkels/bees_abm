from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd
import math

from config import *

from food import Food
from hive import Hive
import util

# TODO remove
import time as tm

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
        if bee.age > BABYTIME:
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
                chosen_loc = rd.randint(0, len(hive.food_locs) - 1)
                bee.food_loc = hive.food_locs[chosen_loc]


            # otherwise, stay at hive and gain energy
            else:
                bee.relax_at_hive(hive)

        else:
            bee.relax_at_hive(hive)


class Scout(BeeStrategy):
    '''
    This type of bee does a random walk, searching for food, and return to hive if he has found this.
    '''

    def step(self):
        bee = self.bee

        # no food found yet, do random walk
        if bee.loaded is False:

            # search for food (vision is 1)
            neighbors = bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=False, radius=1)
            food_neighbours = [nb.pos for nb in neighbors if type(nb) == Food and nb.util]

            # If you see food that is uneaten, move there.
            if food_neighbours:
                go_to = food_neighbours[rd.randrange(0, len(food_neighbours))]
                bee.model.grid.move_agent(bee, go_to)

            # otherwise, move randomly
            else:
                bee.random_move()

            # take the food on current cell
            for nb in bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0):

                # if the source is not yet empty
                #TODO add carrying capacity
                if type(nb) == Food and nb.util % 5 > 0:

                    # decrease utility of food
                    nb.get_eaten()

                    # take food and remember location
                    bee.loaded = True
                    bee.food_loc = bee.pos

                    # Become a forager if you found food.
                    bee.type_bee = 'foraging'

        else:
            assert bee.loaded == False


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
                neighbors = bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0)
                #TODO CHECK DEPENDENCY CARRYING CAPACITY
                food_neighbors = [nb for nb in neighbors if type(nb) == Food and nb.util % 5 > 0]
                #TODO DEFINE PLAN COURSE
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
    def __init__(self, model, pos, hive, type_bee, hive_id):
        super().__init__(model.next_id(), model)

        self.loaded = False
        self.food_loc = []
        self.hive_loc = hive.pos
        self.hive_id = hive_id
        self.pos = pos
        self.type_bee = type_bee
        self.age = 0


        # random threshold of energy required per bee to go foraging
        #TODO SHOULD DEPEND ON ENERGY LEVEL OF HIVE
        self.max_energy = rd.randint(10, 30)
        self.energy = self.max_energy

        self.known_obstacles = set()
        self.plan_course = []

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''

        #get neighboorhood
        neighbourhood = self.get_accessible_neighbourhood()

        # select random cell in neighbourhood
        select_coords = rd.randint(0, len(neighbourhood) - 1)

        # move to cell
        self.model.grid.move_agent(self, neighbourhood[select_coords])

    def get_accessible_neighbourhood(self):
        '''
        Determine with cells in neighbourhood are not with obstacles
        '''

        neighbourhood, obstacles = self.model.grid.get_accessible_neighborhood(self.pos, moore=True)
        self.known_obstacles.update(obstacles)

        return list(neighbourhood)

    def move(self, loc):
        '''
        Move to specified location.
        '''
        neighborhood = self.get_accessible_neighbourhood()

        if not self.plan_course or not self.plan_course[0] in neighborhood:
            self.plan_course = util.path_finder(cur_loc=self.pos,
                                               target_loc=loc,
                                               obstacles=self.known_obstacles,
                                               grid_width=self.model.width,
                                               grid_height=self.model.height)

        nxt_loc = self.plan_course[0]
        self.model.grid.move_agent(self, nxt_loc)
        self.plan_course.pop(0)

    def arrive_at_hive(self, hive):
        '''
        A scouting bee arrives back at the hive
        '''

        # unload food
        
        self.loaded = False
        hive.receive_info(self.food_loc)
        hive.unload_food()

        # become rester to gain energy
        self.type_bee = "rester"

    def relax_at_hive(self, hive):
        '''
        Eat while at hive and gain energy
        '''

        if hive.food > hive.bite:
            self.energy += hive.bite
            hive.food -= hive.bite

        # if no food is available, go search
        #TODO ENERGY DECAY OVER TIME
        else:
            self.energy -= 1
            self.type_bee = "scout"

    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''
        # TODO TYPE OF ENERGY DECAY FOR BEE AND AGE SPAN
        self.age += 1

        # if outside of hive, lose energy proportional to age
        if self.pos != self.hive_loc:
            self.energy -= (self.age / 100)

        # if no more energy, die
        if self.energy <= 0:
            self.model.remove_agent(self)
            return

        # if bee is a rester at 40, become scout
        #TODO AGE TO BECOME SCOUTER DECISION
        if self.age > 40 and self.type_bee == "rester":
            self.type_bee = "scout"

        strategy = bee_strategies[self.type_bee]
        strategy(self).step()