from mesa import Model
from mesa import Agent
from mesa.space import MultiGrid
import random as rd

from food import Bee, Food
from schedule import RandomActivationBeeWorld

class BeeForagingModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = width
        self.width = height

        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.schedule = RandomActivationBeeWorld(self)

        # # Food Info
        # self.start_food = 5
        # self.n_food = 0
        # self.foods = []

        # Init bees
        bee = Bee(unique_id=self.next_id(), model=self)
        self.grid.place_agent(bee, (0, 0))
        self.schedule.add(bee)

        food = Food(id = self.next_id(), model = self, pos = (3,3), util = 5)
        self.grid.place_agent(food, (3, 3))

    def step(self):
        self.schedule.step()

        # self.init_food()

    # def new_food(self, pos):
    #     self.n_food += 1
    #     new_food = agent_type(Food, self.model, pos)
    #     self.grid.place_agent(new_food, pos)
    #     self.foods.append(new_food)

    # def remove_food(self, food):
    #     '''
    #     Method that enables us to remove passed agents.
    #     '''
    #     self.n_food -= 1

    #     # Remove agent from grid
    #     self.grid.remove_agent(food)

    #     # Remove agent from model
    #     self.agents.remove(food)

    # def step(self):
    #     for food in list(self.foods):
    #         food.step()

    # def init_food(self):
    #     for i in range(self.start_food):
    #         pos = (rd.randrange(self.width), rd.randrange(self.height))
    #         util = rd.randint(0, 10)
    #         food = Food(i, self, pos, util)
    #         self.foods.append(food)
