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


    def new_food(self, pos):
        self.n_food += 1
        new_food = agent_type(Food, self.model, pos)
        self.grid.place_agent(new_food, pos)
        self.foods.append(new_food)

class Bee(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.id = id
        self.loaded = False

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
        self.random_move()


# if __name__ == '__main__':
#     FoodModel = HiveModel(10, 10)
#     FoodModel.step()
