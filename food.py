from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd


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

class Bee(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.id = id
        self.loaded = False
        self.food_loc = []

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        
        # get neighborhood
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True)
        print(neighborhood)
        
        # select random cell in neighbourhood
        select_coor = rd.randint(0, len(neighborhood) - 1)
        
        # move to cell
        self.model.grid.move_agent(self, neighborhood[select_coor])


    def step(self):
        '''
        Move the bee, look around for a food source and take food source
        '''

        if self.loaded == False:
            self.random_move()

            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=0)
            print(neighbors)
            for nb in neighbors:
                if type(nb) == Food:
                    print(nb.util)
                    self.loaded = True
                    self.food_loc.append(self.pos)

        # else:




# if __name__ == '__main__':
#     FoodModel = HiveModel(10, 10)
#     FoodModel.step()
