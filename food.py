from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd
import math


class Food(Agent):
    def __init__(self, id, model, pos, util):
        super().__init__(id, model)
        self.id = id
        self.model = model
        self.pos = pos
        self.util = util

    def step(self):
        print(f'current location: {self.pos}')
        print(f'current utility: {self.util}')

    def get_eaten(self):
        self.util -= 1

class Hive(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos

    def step(self):
        print(f'The Hive is alive')

class Bee(Agent):

    def __init__(self, unique_id, model, type_bee):
        super().__init__(unique_id, model)
        self.id = id
        self.loaded = False
        self.food_loc = []
        self.hive_loc = (0, 0)
        self.type_bee = type_bee

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        
        # get neighborhood
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True)
        
        # select random cell in neighbourhood
        select_coor = rd.randint(0, len(neighborhood) - 1)
        
        # move to cell
        self.model.grid.move_agent(self, neighborhood[select_coor])

    def move(self, loc):

        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True)

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


    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''

        # random search bee
        if self.type_bee == "scout":

            # bee is going to random search
            if self.loaded == False:
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
                            self.food_loc.append(self.pos)

            # if he has found a food source, return to hive
            else:

                # check if destination is reached
                if self.pos == self.hive_loc:
                    self.loaded = False

                else:
                    self.move(self.hive_loc)
