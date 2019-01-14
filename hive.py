from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import random as rd



class Bee(Agent):

    def __init__(self,id, pos):
        self.pos = pos
        pass
    # subclasses with different bee types or variables that show bee type

class Food(Agent):
    def __init__(self, model, id, pos, util):
        super().__init__(name, model)
        self.id = id
        self.pos = pos
        self.util = util

    def step(self):
        print(f'current utility: {self.util}')


class Area(Model):

    def __init__(self, wt, ht, n_food):
        super().__init__()
        self.width = wt
        self.height = ht
        self.MultiGrid = Grid(self.width, self.height, torus=true)
        self.nf = n_food
        self.schedule = RandomActivation(self)
        self.foods = []

        # Create sheep and wolves
        self.init_food(Food, self.nf)

        # This is required for the datacollector to work
        self.running = True
        self.datacollector.collect(self)

    def init_food(self, n_food):
        for i in range(n_food):
            pos = (rd.randrange(self.width), rd.randrange(self.height))
            util = rd.randint(0, 10)
            self.new_food(pos, util)

    def new_food(self, pos, util):
        food = Food(i, self)
        self.schedule.add(food)
        coords = pos
        self.grid.place_agent(a, coords)

    def step(self):
        self.schedule.step()









    def step(self):
