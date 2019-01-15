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

class Bee(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.id = id

    def step(self):
        print("stepped")

# if __name__ == '__main__':
#     FoodModel = HiveModel(10, 10)
#     FoodModel.step()
