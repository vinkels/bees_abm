from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd
import math

from food import Food
from obstacle import Obstacle
from hive import Hive


class BeeStrategy:
    """
    Base Class to create a bee strategy
    """

    def __init__(self, Bee):
        self.bee = Bee

    def step(self):
        raise NotImplementedError


class Rester(BeeStrategy):
    '''
    This type of bees stays at the hive, until a location for food is known and then he becomes a foraging bee
    '''

    def step(self):
        bee = self.bee

        # Resting bees can only be at the hive.
        assert bee.pos == bee.hive_loc

        hive = [
            nb 
            for nb in bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0) 
            if type(nb) == Hive
        ][0]

        if hive.food_locs:
            bee.type_bee = "foraging"
            chosen_loc = rd.randint(0, len(hive.food_locs) - 1)
            bee.food_loc = hive.food_locs[chosen_loc]


class Scout(BeeStrategy):

    def step(self):
        bee = self.bee
        # bee is going to random search
        if bee.loaded is False:
            bee.random_move()

            # check for food on current cell    
            neighbors = bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0)
            for nb in neighbors:
                if type(nb) == Food:

                    # if the source is not yet empty
                    if nb.util > 0:
                        nb.get_eaten()

                        # take food and remember location
                        bee.loaded = True
                        bee.food_loc = bee.pos


        # if he has found a food source, return to hive
        else:

            # check if destination is reached
            env = bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0)
            for loc in env:
                if type(loc) == Hive:
                    bee.arrive_at_hive(loc)

                else:
                    bee.move(bee.hive_loc)


class Foraging(BeeStrategy):
    '''
    This type of bee goes to a given food location, takes the food and return to the hive
    '''

    def step(self):   
        bee = self.bee

        # if not yet arrived at food location
        if bee.loaded is False:

            # check if arrived, then take food
            if bee.food_loc == bee.pos:
                neighbors = bee.model.grid.get_neighbors(bee.pos, moore=True, include_center=True, radius=0)
                for nb in neighbors:
                    if type(nb) == Food:

                        # if the source is not yet empty
                        if nb.util > 0:
                            nb.get_eaten()

                            # take food and remember location
                            self.loaded = True

                        else:
                            self.type_bee = "scout"

            # else, move to location

            else:
                bee.move(bee.food_loc)

        # if loaded, return to hive
        else:
            bee.move(bee.hive_loc)

            if bee.hive_loc == bee.pos:
                bee.type_bee = "rester"


bee_strategies = {
    'rester': Rester,
    'foraging': Foraging,
    'scout': Scout
}


class Bee(Agent):
    def __init__(self, model, pos, hive, type_bee):
        super().__init__(model.next_id(), model)

        self.loaded = False
        self.food_loc = []
        self.hive_loc = hive.pos
        self.pos = pos
        self.type_bee = type_bee
        self.age = 0

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
        
        obstacles = [
            nb.pos 
            for nb in self.model.grid.get_neighbors(self.pos, moore=True)
            if type(nb) == Obstacle
        ]
        
        neighbourhood = self.model.grid.get_neighborhood(self.pos, moore=True)

        return [
            loc
            for loc in neighbourhood
            if loc not in obstacles
        ]
    
    def move(self, loc):

        neighborhood = self.get_accessible_neighbourhood()

        # determine distance of current position to goal
        min_dist = math.sqrt( ((self.pos[0]-loc[0])**2)+((self.pos[1]-loc[1])**2))
        go_to = self.pos
        
        # select neighbouring cell with smallest distance to goal
        for cell in neighborhood:
            
            # determine for each cell the distance to the goal
            dist = math.sqrt( ((cell[0]-loc[0])**2)+((cell[1]-loc[1])**2))
            
            if dist < min_dist:
                min_dist = dist
                go_to = cell

        # move to neighbour cell
        self.model.grid.move_agent(self, go_to)

    def arrive_at_hive(self, hive):
        ''' 
        A scouting bee arrives back at the hive
        '''
        self.loaded = False
        hive.receive_info(self.food_loc)
        hive.unload_food()


    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''

        self.age += 1

        # Kill random bees, TODO make this depend on energy
        if rd.random() > 0.99:
            self.model.remove_agent(self)
            return
        
        # strategy(self).step()

        if self.age > 40:
            self.type_bee = "scout"

        strategy = bee_strategies[self.type_bee]
        strategy(self).step()
