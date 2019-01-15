from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd
import math


class Food(Agent):
    def __init__(self, model, pos, util):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.util = util

    def step(self):
        print(f'current location: {self.pos}, current utility: {self.util}')

    def get_eaten(self):
        self.util -= 1

class Hive(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)

        self.pos = pos
        self.food_locs = []

        self.food = 0

    def receive_info(self, info):
        self.food_locs.append(info)

    def step(self):
        # Make random new bees
        # TODO make this actually depend on queen, drones and food resources.
        if rd.random() > 0.99:
            bee = Bee(self.model, self.pos, self, "scout")
            self.model.add_agent(bee, self.pos)

    def unload_food(self, food=1):
        self.food += 1

    def get_food_stat(self):
        return self.food

class Bee(Agent):
    def __init__(self, model, pos, hive, type_bee):
        super().__init__(model.next_id(), model)

        self.loaded = False
        self.food_loc = []
        self.hive_loc = hive.pos
        self.pos = pos
        self.type_bee = type_bee

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        print("random moved")
        
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

    def give_hive_info(self):
        pass

    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''

        # Kill random bees, TODO make this depend on energy
        if rd.random() > 0.99:
            self.model.remove_agent(self)
            return

        # random search bee
        print(self.__dict__)

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
                            self.food_loc.append(self.pos)

            # if he has found a food source, return to hive
            else:

                # check if destination is reached
                if self.pos == self.hive_loc:
                    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
                    for nb in neighbors:
                        if type(nb) == Hive:
                            self.loaded = False
                            nb.unload_food()
                else:
                    self.move(self.hive_loc)

        elif self.type_bee == "foraging":
            pass
