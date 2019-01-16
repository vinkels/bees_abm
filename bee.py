from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd
import math

from food import Food
from obstacle import Obstacle
from hive import Hive


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

        accessible_neighbourhood = [
            loc
            for loc in neighbourhood
            if loc not in obstacles
        ]
        return accessible_neighbourhood
    
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

        if self.age > 40:
            self.type_bee = "scout"

        # Kill random bees, TODO make this depend on energy
        if rd.random() > 0.99:
            self.model.remove_agent(self)
            return

        # random search bee
        if self.type_bee == "scout":

            # bee is going to random search
            if self.loaded is False:
                self.random_move()

                # check for food on current cell    
                neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
                for nb in neighbors:
                    if type(nb) == Food:

                        # if the source is not yet empty
                        if nb.util > 0:
                            nb.get_eaten()

                            # take food and remember location
                            self.loaded = True
                            self.food_loc = self.pos


            # if he has found a food source, return to hive
            else:

                # check if destination is reached
                env = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
                for loc in env:
                    if type(loc) == Hive:
                        self.arrive_at_hive(loc)

                    else:
                        self.move(self.hive_loc)

        elif self.type_bee == "rester":
            '''
            This type of bees stays at the hive, until a location for food is known and then he becomes a foraging bee
            '''

            env = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
            for loc in env:
                if type(loc) == Hive:
                    if loc.food_locs:
                        self.type_bee = "foraging"
                        print("Aantal food locs: ", len(loc.food_locs))
                        chosen_loc = rd.randint(0, len(loc.food_locs) - 1)
                        self.food_loc= loc.food_locs[chosen_loc]

        elif self.type_bee == "foraging":
            '''
            This type of bee goes to a given food location, takes the food and return to the hive
            '''
            
            # if not yet arrived at food location
            if self.loaded is False:

                # check if arrived, then take food
                if self.food_loc == self.pos:
                    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
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
                    self.move(self.food_loc)

            # if loaded, return to hive
            else:
                self.move(self.hive_loc)

                if self.hive_loc == self.pos:
                    self.type_bee = "rester"

        else:
            raise Exception("Dat is geen bij!")
